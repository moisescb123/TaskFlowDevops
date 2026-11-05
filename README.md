# TaskFlow DevOps

Tablero web de tareas académico para practicar **DevOps** (CI, pruebas automatizadas, protección de rama y entrega continua) con un flujo Spec-Driven (OpenSpec / Specboot).

## Stack

| Capa | Tecnología |
|------|------------|
| Backend | Python 3.11+, Flask, SQLite |
| Frontend | HTML, CSS, JavaScript (tablero Kanban) |
| Pruebas | Pytest |
| CI/CD | GitHub Actions (`CI` → Pytest; `CD` → Render tras CI verde en `main`) |

## Roles

| Rol | Capacidades |
|-----|-------------|
| **Admin** | Registro y gestión de usuarios |
| **Developer** | CRUD de tareas, transiciones de estado, asignado, prioridad y fecha límite |
| **Viewer** | Solo lectura del tablero |

Reglas de negocio: un solo asignado (RN01); título, fecha límite y prioridad obligatorios (RN02); `main` protegida por pruebas verdes antes de merge/despliegue (RN03); no se permite saltar de To Do a Done (RN04).

## Diseño y modelado del sistema

TaskFlow es una aplicación web monolítica: el navegador habla con un solo proceso Flask, que persiste usuarios y tareas en SQLite y se publica en Render solo después de que CI pase en `main`.

### Arquitectura de contexto

Actores y sistemas externos. El tablero no depende de otros servicios de negocio; GitHub y Render cubren verificación y publicación.

```mermaid
flowchart LR
  admin[Admin]
  developer[Developer]
  viewer[Viewer]
  app[TaskFlow DevOps]
  gh[GitHub Actions]
  render[Render]

  admin -->|gestiona usuarios| app
  developer -->|crea y mueve tareas| app
  viewer -->|consulta el tablero| app
  gh -->|Pytest en cada push y PR| app
  gh -->|hook solo si CI en main es verde| render
  render -->|sirve la demo| app
```

### Arquitectura lógica

Cuatro capas dentro del mismo proceso. Las páginas HTML no acceden a la base: el JavaScript del tablero llama a la API JSON.

```mermaid
flowchart TB
  subgraph cliente [Cliente]
    pages[Paginas HTML<br/>login, tablero, usuarios]
    js[JavaScript del tablero]
  end

  subgraph aplicacion [Aplicacion Flask]
    routes[Rutas<br/>pages, auth, users, tasks]
    authz[Sesion y autorizacion por rol]
    services[Servicios<br/>auth, usuarios, tareas]
    models[Modelos User y Task]
  end

  db[(SQLite<br/>users y tasks)]

  pages --> routes
  js -->|JSON /api| routes
  routes --> authz
  authz --> services
  services --> models
  models --> db
```

| Capa | Responsabilidad | Ubicación |
|------|-----------------|-----------|
| Presentación | Login, tablero Kanban y pantalla de usuarios | `templates/`, `static/` |
| API y páginas | HTTP, códigos de estado y redirecciones | `app/routes/` |
| Autorización | Cookie de sesión firmada; decoradores por rol | `app/auth/`, `app/services/auth_service.py` |
| Dominio | Validación RN01–RN04 y casos de uso | `app/services/`, `app/models/` |
| Persistencia | Tablas `users` y `tasks`, claves foráneas | `app/db.py` |

Puntos de entrada: en local, `flask --app app run`; en producción, Gunicorn carga `wsgi:app`, que llama a `create_app()`.

### Flujo de una petición

Ejemplo: un Developer mueve una tarea de To Do a In progress.

```mermaid
sequenceDiagram
  actor Dev as Developer
  participant UI as Tablero
  participant API as PATCH /api/tasks/id/status
  participant Svc as task_service
  participant DB as SQLite

  Dev->>UI: Cambia el estado
  UI->>API: Cookie de sesion y nuevo estado
  API->>API: Exige rol developer
  API->>Svc: Valida la transicion RN04
  Svc->>DB: Actualiza tasks.status
  DB-->>UI: Tarea en in_progress
```

Admin y Viewer que llamen a un endpoint de escritura reciben `403`. Sin sesión, las páginas protegidas redirigen a `/login`.

### Modelo de dominio

Dos entidades persistidas. El tablero no es una tabla: es la vista que agrupa tareas por `status`.

```mermaid
erDiagram
  USER ||--o{ TASK : "assignee_id"
  USER ||--o{ TASK : "created_by_id"
  USER {
    int id PK
    string email UK
    string password_hash
    string full_name
    string role
    datetime created_at
  }
  TASK {
    int id PK
    string title
    string status
    string priority
    date due_date
    int assignee_id FK
    int created_by_id FK
    datetime created_at
    datetime updated_at
  }
```

| Concepto | Valores | Regla |
|----------|---------|--------|
| Rol | `admin`, `developer`, `viewer` | Define qué pantallas y endpoints puede usar |
| Estado | `todo`, `in_progress`, `done` | Columna del tablero |
| Prioridad | `high`, `medium`, `low` | Obligatoria (RN02) |
| Asignado | como máximo un `assignee_id` | RN01 |
| Sesión | cookie firmada con `SECRET_KEY` | No se guarda en SQLite |

Detalle de campos y contratos: [`docs/data-model.md`](docs/data-model.md) y [`docs/api-spec.yml`](docs/api-spec.yml).

### Diagrama de clases

El rol no es una subclase: vive en `User.role`. `Task` conoce a su creador y, como máximo, a un asignado. Los servicios aplican las reglas de negocio; las rutas HTTP solo delegan.

```mermaid
classDiagram
  class User {
    +int id
    +string email
    +string passwordHash
    +string fullName
    +string role
    +toPublicDict() dict
  }
  class Task {
    +int id
    +string title
    +string status
    +string priority
    +string dueDate
    +int assigneeId
    +int createdById
    +string createdAt
    +string updatedAt
    +toPublicDict() dict
  }
  class AuthService {
    +authenticate(email, password) User
    +establishSession(user) void
    +clearSession() void
    +currentUser() User
  }
  class UserService {
    +registerUser(payload) User
    +listPublicUsers() list
  }
  class TaskService {
    +getTasksForBoard() list
    +createTaskFromPayload(payload, createdById) dict
    +updateTaskFromPayload(taskId, payload) dict
    +changeTaskStatus(taskId, status) dict
    +removeTask(taskId) void
  }

  User "1" --> "0..*" Task : createdBy
  User "0..1" --> "0..*" Task : assignee
  AuthService --> User : autentica
  UserService --> User : registra
  TaskService --> Task : persiste
  TaskService --> User : valida asignado
```

| Clase | Dónde vive | Qué decide |
|-------|------------|------------|
| `User`, `Task` | `app/models/` | Forma de los datos y mapeo a SQLite |
| `AuthService` | `app/services/auth_service.py` | Credenciales y cookie de sesión |
| `UserService` | `app/services/user_service.py` | Alta de usuarios (solo Admin) |
| `TaskService` | `app/services/task_service.py` | RN01, RN02 y RN04 |

### Diagramas de actividad

#### Inicio de sesión

```mermaid
flowchart TD
  inicio([Inicio]) --> form[Ingresar correo y contraseña]
  form --> formato{Formato válido?}
  formato -->|No| e400[Responder 400]
  formato -->|Sí| cred{Usuario y contraseña correctos?}
  cred -->|No| e401[Responder 401]
  cred -->|Sí| sesion[Guardar user_id y role en la sesión]
  sesion --> rol{Rol}
  rol -->|admin| admin[Abrir gestión de usuarios]
  rol -->|developer o viewer| board[Abrir tablero]
  e400 --> fin([Fin])
  e401 --> fin
  admin --> fin
  board --> fin
```

#### Alta de una tarea

Solo el Developer llega a crear. La tarea nace en `todo`.

```mermaid
flowchart TD
  inicio([Inicio]) --> sesion{Sesión de developer?}
  sesion -->|No autenticado| e401[Responder 401]
  sesion -->|Admin o Viewer| e403[Responder 403]
  sesion -->|Developer| datos[Enviar título, prioridad, fecha y asignado opcional]
  datos --> valid{RN02 y RN01 válidos?}
  valid -->|No| e400[Responder 400]
  valid -->|Sí| guardar[Insertar tarea con estado todo]
  guardar --> ok[Devolver la tarea y mostrarla en To Do]
  e401 --> fin([Fin])
  e403 --> fin
  e400 --> fin
  ok --> fin
```

#### Cambio de estado

```mermaid
flowchart TD
  inicio([Inicio]) --> sesion{Sesión de developer?}
  sesion -->|No| denegado[Responder 401 o 403]
  sesion -->|Sí| existe{La tarea existe?}
  existe -->|No| e404[Responder 404]
  existe -->|Sí| salto{Transición permitida?}
  salto -->|todo a done| e400[Rechazar por RN04]
  salto -->|Sí| actualizar[Actualizar status y updated_at]
  actualizar --> ok[Mover la tarjeta de columna]
  denegado --> fin([Fin])
  e404 --> fin
  e400 --> fin
  ok --> fin
```

#### Registro de usuario

```mermaid
flowchart TD
  inicio([Inicio]) --> sesion{Sesión de admin?}
  sesion -->|No| denegado[Responder 401 o 403]
  sesion -->|Sí| datos[Enviar correo, contraseña, nombre y rol]
  datos --> valid{Datos válidos y correo libre?}
  valid -->|No| e400[Responder 400]
  valid -->|Sí| hash[Guardar password_hash y el rol]
  hash --> ok[Devolver el usuario sin la contraseña]
  denegado --> fin([Fin])
  e400 --> fin
  ok --> fin
```

### Modelo de estados de una tarea

Una tarea nueva nace en `todo`. Se puede retroceder; no se puede saltar de To Do a Done (RN04).

```mermaid
stateDiagram-v2
  [*] --> todo: alta
  todo --> in_progress: iniciar
  in_progress --> done: terminar
  done --> in_progress: reabrir
  in_progress --> todo: devolver
```

El salto `todo` → `done` no forma parte del modelo: el servicio lo rechaza.

### Arquitectura de despliegue

`main` está protegida: el merge exige el check **Pytest**. El workflow de CD no tiene disparo manual; solo corre si ese CI terminó en éxito y la rama es `main`.

```mermaid
flowchart LR
  pr[Pull request] --> ci[GitHub Actions CI<br/>Pytest]
  ci -->|check obligatorio| main[rama main]
  main --> ci2[CI en main]
  ci2 -->|conclusion success| cd[Workflow CD]
  cd -->|POST RENDER_DEPLOY_HOOK| render[Render web service]
  render --> gunicorn[Gunicorn wsgi:app]
  gunicorn --> sqlite[(taskflow.db)]
```

| Pieza | Rol |
|-------|-----|
| `.github/workflows/ci.yml` | Instala dependencias y ejecuta Pytest en push y pull request |
| Protección de `main` | Impide el merge sin el check Pytest (RN03) |
| `.github/workflows/cd.yml` | Dispara el deploy hook de Render |
| `render.yaml` | Servicio Python free: build con pip, arranque con Gunicorn, health check en `/login` |
| `SECRET_KEY` | Variable de entorno en Render; la app no arranca en producción con el valor de desarrollo |

## Inicio rápido (local)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env   # define un SECRET_KEY real
python scripts/seed_users.py
pytest
flask --app app run
```

Aplicación: [http://localhost:5000](http://localhost:5000) — inicio de sesión en `/login`.

### Usuarios de demostración

| Correo | Contraseña | Rol |
|--------|------------|-----|
| `admin@taskflow.local` | `Admin123!` | admin |
| `dev@taskflow.local` | `Dev123!` | developer |
| `viewer@taskflow.local` | `Viewer123!` | viewer |

En arranques que no son de prueba, la aplicación también crea estos usuarios si faltan (útil en demos alojadas).

## CI / CD

- **CI** (`.github/workflows/ci.yml`): ejecuta Pytest en push y pull requests. Check obligatorio en `main`: **`Pytest`**.
- **CD** (`.github/workflows/cd.yml`): tras un **CI exitoso en `main`**, dispara el deploy hook de Render (secreto `RENDER_DEPLOY_HOOK`).
- Guías operativas: [`docs/branch-protection.md`](docs/branch-protection.md), [`docs/continuous-delivery.md`](docs/continuous-delivery.md).

## Estructura del proyecto

```
app/                 # Aplicación Flask
templates/ static/   # Interfaz
tests/               # Suite Pytest
scripts/             # Utilidades de seed
.github/workflows/   # CI + CD
docs/                # Estándares, API, modelo de datos, guías
openspec/            # Especificaciones e historial de cambios
US/                  # Historias de usuario (us01–us15)
```

## Documentación

| Documento | Propósito |
|-----------|-----------|
| [`docs/development_guide.md`](docs/development_guide.md) | Setup local, API, pasos de CI/CD |
| [`docs/api-spec.yml`](docs/api-spec.yml) | Contratos HTTP |
| [`docs/data-model.md`](docs/data-model.md) | Modelo de dominio |
| [`docs/base-standards.md`](docs/base-standards.md) | Reglas de desarrollo (TDD, etc.) |
| [`README_specboot.md`](README_specboot.md) | Configuración Specboot / agentes |

## Flujo Spec-Driven

Las historias están en `US/us01.md` … `US/us15.md`. Los cambios se planifican y archivan con OpenSpec (`openspec/`). Consulta la guía de desarrollo para el flujo recomendado (`/apply` → `/verify` → `/adversarial-review` → `/archive` → `/commit`).

## Licencia

Proyecto académico — TaskFlow DevOps.
