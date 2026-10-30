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
