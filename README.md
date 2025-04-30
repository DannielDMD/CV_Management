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
