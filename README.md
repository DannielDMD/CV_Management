---

# 📂 Backend - Gestión de Candidatos

Este es el backend del sistema de **Gestión de Candidatos**, una aplicación diseñada para registrar, almacenar y analizar hojas de vida. Se estructura mediante una API REST que permite el registro y administración de candidatos, su información académica, laboral, habilidades y preferencias.

## 🚀 Tecnologías utilizadas

- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL 17
- Alembic (migraciones)
- Pydantic
- Uvicorn
- APScheduler (Automatizaciones de Instrucciones)
- openpyxslx (Excels)
- Pdoc (Documentación de la Aplicación)

## 📦 Estructura del proyecto

```
/app
  ├── main.py                # Entry point de la app FastAPI
  ├── models/                # Modelos SQLAlchemy
  ├── schemas/               # Esquemas Pydantic
  ├── routers/               # Rutas organizadas por recurso
  ├── services/              # CRUD 
  └── core.py            # Conexión a la base de datos

/alembic                     # Migraciones
.env                        # Variables de entorno
requirements.txt            # Dependencias
README.md                   # Este archivo
```

## 📋 Funcionalidades principales

### 👤 Candidatos

- Registro de información personal
- Control de duplicados
- Consulta individual y listado

### 🎓 Educación

- Registro de niveles educativos por candidato
- Relación con catálogo `NivelEducacion`, `TituloObtenido`, `Instituciones`, `NivelIngles`,  
- Endpoint para distribución estadística por nivel

### 💼 Experiencia

- Registro de experiencias laborales por candidato
- Asociación con nombre del cargo y empresa

### 🧠 Habilidades

- Registro de habilidades por candidato
- Estadísticas de habilidades más comunes

### ⚙️ Preferencias

- Registro de área deseada, salario y ciudad preferida
- Consulta individual por candidato

### 📊 Dashboard (en progreso)

- Total de candidatos registrados
- Nuevos esta semana
- Habilidades más frecuentes
- Nivel educativo más común
- Ciudad con más postulantes
- Cargo más solicitado

## 🛠️ Instalación y configuración

1. Clona el repositorio:

```bash
git clone https://github.com/DannielDMD/CV_Management.git
cd backend-candidatos
```

2. Crea un entorno virtual y activa:

```bash
python -m venv venv
source venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Crea un archivo `.env` con tus variables de entorno:

```
DATABASE_URL=postgresql://user:password@localhost:5432/candidatos_db
```


5. Corre el servidor:

```bash
uvicorn app.main:app --reload
```

## 🧪 Endpoints principales

Puedes explorar los endpoints desde la documentación interactiva que ofrece FastAPI en:

```
http://localhost:8000/docs
```

---

## ✍️ Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas para nuevas métricas, validaciones o endpoints, no dudes en proponerlas.

---

```
Cv_Managments_Backend
├─ alembic
│  ├─ env.py
│  ├─ README
│  └─ script.py.mako
├─ alembic.ini
├─ app
│  ├─ core
│  │  ├─ azure_auth.py
│  │  ├─ database.py
│  │  ├─ dependencies.py
│  │  └─ __init__.py
│  ├─ jobs
│  │  ├─ limpieza_candidatos.py
│  │  └─ _init__.py
│  ├─ main.py
│  ├─ models
│  │  ├─ candidato_model.py
│  │  ├─ catalogs
│  │  │  ├─ cargo_ofrecido.py
│  │  │  ├─ centro_costos.py
│  │  │  ├─ ciudad.py
│  │  │  ├─ instituciones.py
│  │  │  ├─ nivel_educacion.py
│  │  │  ├─ nivel_ingles.py
│  │  │  ├─ rango_experiencia.py
│  │  │  ├─ titulo.py
│  │  │  └─ __init__.py
│  │  ├─ conocimientos_model.py
│  │  ├─ educacion_model.py
│  │  ├─ experiencia_model.py
│  │  ├─ preferencias.py
│  │  ├─ solicitud_eliminacion_model.py
│  │  ├─ usuario.py
│  │  └─ __init__.py
│  ├─ routes
│  │  ├─ candidato_route.py
│  │  ├─ catalogs
│  │  │  ├─ cargos_ofrecidos.py
│  │  │  ├─ centro_costos.py
│  │  │  ├─ ciudades.py
│  │  │  ├─ conocimientos_routes.py
│  │  │  ├─ departamentos.py
│  │  │  ├─ disponibilidad.py
│  │  │  ├─ instituciones.py
│  │  │  ├─ motivo_salida.py
│  │  │  ├─ nivel_educacion.py
│  │  │  ├─ nivel_ingles.py
│  │  │  ├─ rangos_experiencia.py
│  │  │  ├─ rangos_salariales.py
│  │  │  ├─ titulo.py
│  │  │  └─ __init__.py
│  │  ├─ conocimientos_candidato_route.py
│  │  ├─ Dashboard
│  │  │  ├─ export_pdf.py
│  │  │  ├─ export_report.py
│  │  │  ├─ stats_conocimientos.py
│  │  │  ├─ stats_educacion.py
│  │  │  ├─ stats_experiencia.py
│  │  │  ├─ stats_general.py
│  │  │  ├─ stats_personal.py
│  │  │  ├─ stats_preferencias.py
│  │  │  ├─ stats_proceso.py
│  │  │  ├─ stats_routes.py
│  │  │  └─ __init__.py
│  │  ├─ educacion_route.py
│  │  ├─ experiencia_route.py
│  │  ├─ preferencias_route.py
│  │  ├─ solicitudes_eliminacion_route.py
│  │  ├─ usuario_route.py
│  │  └─ __init__.py
│  ├─ schemas
│  │  ├─ candidato_schema.py
│  │  ├─ catalogs
│  │  │  ├─ cargo_ofrecido.py
│  │  │  ├─ centro_costos.py
│  │  │  ├─ ciudad.py
│  │  │  ├─ conocimientos_schema.py
│  │  │  ├─ instituciones.py
│  │  │  ├─ motivo_salida.py
│  │  │  ├─ nivel_educacion.py
│  │  │  ├─ nivel_ingles.py
│  │  │  ├─ rango_experiencia.py
│  │  │  ├─ titulo.py
│  │  │  └─ __init__.py
│  │  ├─ conocimientos_candidato_schema.py
│  │  ├─ dashboard
│  │  │  ├─ stats_conocimientos_schema.py
│  │  │  ├─ stats_educacion_schema.py
│  │  │  ├─ stats_experiencia_schema.py
│  │  │  ├─ stats_general_schema.py
│  │  │  ├─ stats_personal_schema.py
│  │  │  ├─ stats_preferencias_schema.py
│  │  │  └─ stats_proceso_schema.py
│  │  ├─ educacion_schema.py
│  │  ├─ experiencia_schema.py
│  │  ├─ preferencias_schema.py
│  │  ├─ solicitud_eliminacion_schema.py
│  │  ├─ usuario_schema.py
│  │  └─ __init__.py
│  ├─ services
│  │  ├─ candidato_service.py
│  │  ├─ catalogs
│  │  │  ├─ cargos_ofrecidos_service.py
│  │  │  ├─ centro_costos_service.py
│  │  │  ├─ ciudades_service.py
│  │  │  ├─ conocimientos_service.py
│  │  │  ├─ departamentos_service.py
│  │  │  ├─ disponibilidad_service.py
│  │  │  ├─ instituciones_service.py
│  │  │  ├─ motivo_salida_service.py
│  │  │  ├─ nivel_educacion_service.py
│  │  │  ├─ nivel_ingles_service.py
│  │  │  ├─ rangos_salariales_service.py
│  │  │  ├─ rango_experiencia_service.py
│  │  │  ├─ titulo_service.py
│  │  │  └─ __init__.py
│  │  ├─ conocimientos_candidato_service.py
│  │  ├─ dashboard
│  │  │  ├─ export_pdf_service.py
│  │  │  ├─ export_service.py
│  │  │  ├─ stats_conocimientos_service.py
│  │  │  ├─ stats_educacion_service.py
│  │  │  ├─ stats_experiencia_service.py
│  │  │  ├─ stats_general_service.py
│  │  │  ├─ stats_personal_service.py
│  │  │  ├─ stats_preferencias_service.py
│  │  │  ├─ stats_proceso_service.py
│  │  │  └─ stats_service.py
│  │  ├─ educacion_service.py
│  │  ├─ experiencia_service.py
│  │  ├─ mappers
│  │  │  ├─ candidato_mapper.py
│  │  │  └─ __init__.py
│  │  ├─ preferencias_service.py
│  │  ├─ solicitudes_eliminacion_service.py
│  │  ├─ usuario_service.py
│  │  └─ __init__.py
│  ├─ static
│  │  └─ LogoJoyco.png
│  ├─ utils
│  │  ├─ orden_catalogos.py
│  │  └─ __init__.py
│  └─ __init__.py
├─ docs
├─ README.md
├─ requirements.txt
└─ test
   └─ __init__.py

```