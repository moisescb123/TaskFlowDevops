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

Los modelos siguen la semana 5: contexto, casos de uso, clases, secuencia, actividad, estados y flujo de datos. Cada uno muestra una vista del mismo sistema y omite el resto.

TaskFlow es una aplicación web: el navegador habla con un proceso Flask y las tareas quedan en SQLite. GitHub Actions y Render están fuera de la frontera del producto; verifican y publican el sistema.

### Modelo de contexto

Muestra el sistema en su entorno y marca la frontera con actores y sistemas externos.

```mermaid
flowchart LR
  admin[Administrador]
  dev[Desarrollador]
  vis[Visualizador]
  gh[GitHub Actions]
  render[Render]
  sys[TaskFlow DevOps]

  admin --- sys
  dev --- sys
  vis --- sys
  gh --- sys
  render --- sys
```

| Elemento externo | Relación con el sistema |
|------------------|-------------------------|
| Administrador, Desarrollador, Visualizador | Usan el tablero según su rol |
| GitHub Actions | Ejecuta Pytest y, si `main` queda verde, pide el despliegue |
| Render | Publica la demo; no participa en las reglas del tablero |

### Diagrama de casos de uso

Los actores son roles externos. La elipse es una función que el usuario percibe. La línea continua es la interacción del actor. `<<include>>` es una función que el caso siempre utiliza. `<<extend>>` es un comportamiento opcional: el asignado no es obligatorio al crear o editar.

```mermaid
flowchart LR
  admin((Administrador))
  dev((Desarrollador))
  vis((Visualizador))

  login([Iniciar sesión])
  logout([Cerrar sesión])
  board([Consultar tablero])
  create([Crear tarea])
  edit([Editar tarea])
  remove([Eliminar tarea])
  status([Cambiar estado])
  assign([Asignar responsable])
  register([Registrar usuario])

  admin --- login
  admin --- logout
  admin --- board
  admin --- register
  dev --- login
  dev --- logout
  dev --- board
  dev --- create
  dev --- edit
  dev --- remove
  dev --- status
  vis --- login
  vis --- logout
  vis --- board

  logout -.->|include| login
  board -.->|include| login
  create -.->|include| login
  edit -.->|include| login
  remove -.->|include| login
  status -.->|include| login
  register -.->|include| login
  create -.->|extend| assign
  edit -.->|extend| assign
```

### Diagrama de clases

Estructura estática del negocio. Los atributos van con visibilidad privada, como en el ejemplo de la materia. Las multiplicidades van en los extremos de la asociación.

`Usuario` y `Tarea` corresponden a `User` y `Task`. El ejemplo de clase de la materia usa generalización (Persona y Personal). Aquí no hay subclases: Administrador, Desarrollador y Visualizador comparten los mismos datos y se distinguen por el atributo `rol`.

```mermaid
classDiagram
  class Usuario {
    -id
    -correo
    -hashContrasena
    -nombreCompleto
    -rol
  }
  class Tarea {
    -id
    -titulo
    -estado
    -prioridad
    -fechaLimite
    -idAsignado
    -idCreador
  }

  Usuario "1" --> "*" Tarea : crea
  Usuario "0..1" --> "*" Tarea : asignado
```

| Concepto | Valores | Regla |
|----------|---------|--------|
| Rol | `admin`, `developer`, `viewer` | Define qué casos de uso puede iniciar |
| Estado | `todo`, `in_progress`, `done` | Columna del tablero |
| Prioridad | `high`, `medium`, `low` | Obligatoria (RN02) |
| Asignado | como máximo un usuario | RN01 |
| Sesión | cookie firmada con `SECRET_KEY` | No es una clase persistida |

Detalle de campos y contratos: [`docs/data-model.md`](docs/data-model.md) y [`docs/api-spec.yml`](docs/api-spec.yml).

### Diagrama de secuencia

Agrega el detalle del caso de uso **Cambiar estado**: los objetos que participan y el orden de los mensajes. La respuesta vuelve con línea discontinua.

```mermaid
sequenceDiagram
  actor Dev as Desarrollador
  participant UI as Interfaz
  participant Gestor as GestorTareas
  participant DB as Base de datos

  Dev->>UI: 1. cambiarEstado(id, estado)
  UI->>Gestor: 2. cambiarEstado(id, estado)
  Gestor->>DB: 3. leerTarea(id)
  DB-->>Gestor: 4. tarea
  Gestor->>Gestor: 5. validarTransicion
  Gestor->>DB: 6. actualizarEstado(id, estado)
  DB-->>Gestor: 7. tareaActualizada
  Gestor-->>UI: 8. tarea
  UI-->>Dev: 9. mostrarTablero
```

Si el actor no es Desarrollador, `GestorTareas` corta la secuencia y la interfaz muestra el rechazo. Si el salto es de Por hacer a Terminada, el mensaje 5 no llega al mensaje 6.

### Diagramas de actividad

Cada nodo es una acción en verbo. El rombo no lleva la pregunta dentro: la guarda va en la flecha, entre corchetes. El círculo negro es el inicio y el doble círculo es el fin.

#### Iniciar sesión

```mermaid
flowchart TD
  inicio((inicio)) --> autenticar[Autenticar usuario]
  autenticar --> decisionAut{ }
  decisionAut -->|aut = OK| acceso[Acceder a la aplicacion]
  decisionAut -->|aut distinto de OK| error[Mostrar error]
  acceso --> interfaz[Mostrar interfaz segun el rol]
  error --> fin(((fin)))
  interfaz --> fin
```

#### Registrar usuario

```mermaid
flowchart TD
  inicio((inicio)) --> rol{ }
  rol -->|rol = admin| datos[Anadir informacion de registro]
  rol -->|rol distinto de admin| denegado[Mostrar acceso denegado]
  datos --> valid{ }
  valid -->|datosValidos y usuarioExiste = false| guardar[Guardar usuario]
  valid -->|datos invalidos o usuarioExiste = true| error[Mostrar error]
  guardar --> fin(((fin)))
  denegado --> fin
  error --> fin
```

#### Crear tarea

```mermaid
flowchart TD
  inicio((inicio)) --> rol{ }
  rol -->|rol = developer| datos[Anadir titulo, prioridad y fecha limite]
  rol -->|rol distinto de developer| denegado[Mostrar acceso denegado]
  datos --> valid{ }
  valid -->|datosValidos| guardar[Guardar tarea en Por hacer]
  valid -->|datos invalidos| error[Mostrar error]
  guardar --> tablero[Mostrar tarea en el tablero]
  denegado --> fin(((fin)))
  error --> fin
  tablero --> fin
```

#### Cambiar estado

```mermaid
flowchart TD
  inicio((inicio)) --> rol{ }
  rol -->|rol = developer| leer[Leer tarea]
  rol -->|rol distinto de developer| denegado[Mostrar acceso denegado]
  leer --> existe{ }
  existe -->|tareaExiste = false| noExiste[Mostrar tarea inexistente]
  existe -->|tareaExiste = true| transicion{ }
  transicion -->|transicionValida| actualizar[Actualizar estado]
  transicion -->|salto de Por hacer a Terminada| rechazar[Rechazar transicion]
  actualizar --> mover[Mover tarjeta de columna]
  denegado --> fin(((fin)))
  noExiste --> fin
  rechazar --> fin
  mover --> fin
```

### Diagrama de estados

Modelo de comportamiento de la tarea. Una tarea nueva entra en Por hacer. Puede retroceder. El salto directo a Terminada no es una transición del modelo.

```mermaid
stateDiagram-v2
  [*] --> PorHacer: crear
  PorHacer --> EnProgreso: iniciar
  EnProgreso --> Terminada: terminar
  Terminada --> EnProgreso: reabrir
  EnProgreso --> PorHacer: devolver
```

En la base de datos esos estados se guardan como `todo`, `in_progress` y `done`.

### Diagrama de flujo de datos

Muestra qué datos circulan, sin el detalle de la lógica. El nivel 0 es el sistema completo. El nivel 1 abre los procesos y los almacenes.

#### Nivel 0

```mermaid
flowchart LR
  admin[Administrador]
  dev[Desarrollador]
  vis[Visualizador]
  p0((0 TaskFlow))

  admin -->|datos de usuario| p0
  p0 -->|listado de usuarios| admin
  dev -->|credenciales y datos de tarea| p0
  p0 -->|tablero| dev
  vis -->|credenciales| p0
  p0 -->|tablero| vis
```

#### Nivel 1

```mermaid
flowchart LR
  admin[Administrador]
  dev[Desarrollador]
  vis[Visualizador]
  p1((1 Autenticar))
  p2((2 Gestionar usuarios))
  p3((3 Gestionar tareas))
  d1[(D1 Usuarios)]
  d2[(D2 Tareas)]

  admin -->|credenciales| p1
  dev -->|credenciales| p1
  vis -->|credenciales| p1
  p1 -->|consulta de usuario| d1
  d1 -->|usuario| p1
  p1 -->|sesion| admin
  p1 -->|sesion| dev
  p1 -->|sesion| vis

  admin -->|datos de usuario| p2
  p2 -->|usuario| d1
  d1 -->|listado| p2
  p2 -->|listado de usuarios| admin

  dev -->|datos de tarea| p3
  p3 -->|tarea| d2
  d2 -->|tareas| p3
  p3 -->|tablero| dev
  p3 -->|tablero| vis
```

### Publicación del sistema

Este flujo no sustituye a los modelos anteriores. Describe el entorno DevOps: `main` exige el check Pytest y el despliegue solo ocurre si ese CI terminó en éxito.

```mermaid
flowchart LR
  pr[Pull request] --> ci[GitHub Actions CI]
  ci -->|Pytest en verde| main[rama main]
  main --> ci2[CI en main]
  ci2 -->|CI exitoso| cd[Disparar despliegue]
  cd --> render[Render]
  render --> app[Aplicacion publicada]
  app --> db[(SQLite)]
```

| Pieza | Rol |
|-------|-----|
| `.github/workflows/ci.yml` | Instala dependencias y ejecuta Pytest en push y pull request |
| Protección de `main` | Impide el merge sin el check Pytest (RN03) |
| `.github/workflows/cd.yml` | Dispara el deploy hook de Render |
| `render.yaml` | Servicio Python: build con pip, arranque con Gunicorn, health check en `/login` |
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
