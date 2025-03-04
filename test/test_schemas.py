from app.schemas.candidato import *
from app.schemas.educacion import *
from app.schemas.experiencia import *
from app.schemas.habilidades_blandas import *
from app.schemas.habilidades_tecnicas import *
from app.schemas.herramientas import *
from app.schemas.preferencias import *
from fastapi import FastAPI
from app.core.database import engine
from test import test_db
from fastapi import FastAPI

""""
PRUEBA DE LA RUTA DE LOS CANDIDATOS
"""
"""
CÓDIGO DE PRUEBA DE COMO PROBAR EN EL MAIN LAS RUTAS CON POSTMAN Y SWAGGER 
"""
"""  
# Endpoint de prueba para validar el schema
@app.post("/candidato")
async def test_schema(candidato: CandidatoCreate):
    return {"message": "✅ Datos validados correctamente", "data": candidato}


@app.put("/candidato/{id}")
async def update_candidato(id: int, candidato: CandidatoUpdate):
    return {"message": f"✅ Candidato {id} actualizado correctamente", "data": candidato}


# Simulación de la base de datos
fake_db = {
    1: {
        "id_candidato": 1,
        "nombre_completo": "Daniel Méndez",
        "correo_electronico": "daniel.mendez@example.com",
        "cc": "1003632723",
        "fecha_nacimiento": "2002-08-27",
        "telefono": "32082214761",
        "ciudad": {"id_ciudad": 1, "nombre_ciudad": "Bogotá"},
        "descripcion_perfil": "Ingeniero de Sistemas muy bueno.",
        "categoria_cargo": {"id_categoria": 4, "nombre_categoria": "Profesionales Especializados"},
        "cargo": {"id_cargo": 59, "nombre_cargo": "Desarrollador de Innovación y Estrategia"},
        "motivo_salida": {"id_motivo_salida": 9, "nombre_motivo": "Problemas de salud"},
        "trabaja_actualmente_joyco": False,
        "ha_trabajado_joyco": True,
        "tiene_referido": True,
        "nombre_referido": "Jenny",
        "fecha_registro": "2024-02-29T12:00:00"
    }
}

@app.get("/candidato/{id}", response_model=CandidatoResponse)
async def get_candidato(id: int):
    candidato = fake_db.get(id)
    if not candidato:
        return {"message": f"❌ Candidato con ID {id} no encontrado"}
    return candidato

"""
"""PRUEBA DE LA EDUCACION"""
"""

# Simulación de la base de datos
fake_db_educacion = {
    1: {
        "id_educacion": 1,
        "nivel_educacion": {"id_nivel_educacion": 2, "descripcion_nivel": "Universitario"},
        "nombre_titulo": {"id_titulo": 5, "titulo": "Ingeniería Civil"},
        "institucion": {"id_institucion": 3, "nombre_institucion": "Universidad Nacional"},
        "anio_graduacion": 2020,
        "nivel_ingles": {"id_nivel_ingles": 2, "nivel": "Intermedio"}
    }
}

# Endpoint de prueba para validar el schema
@app.post("/educacion")
async def test_schema(educacion: EducacionCreate):
    return {"message": "✅ Datos validados correctamente", "data": educacion}

# ✅ Endpoint para actualizar educación
@app.put("/educacion/{id}")
async def update_educacion(id: int, educacion: EducacionUpdate):
    if id not in fake_db_educacion:
        return {"message": f"❌ Educación con ID {id} no encontrada"}
    for key, value in educacion.model_dump().items():
        if value is not None:
            fake_db_educacion[id][key] = value
    return {"message": f"✅ Educación {id} actualizada correctamente", "data": fake_db_educacion[id]}


# ✅ Endpoint para obtener información de educación
@app.get("/educacion/{id}", response_model=EducacionResponse)
async def get_educacion(id: int):
    educacion = fake_db_educacion.get(id)
    if not educacion:
        return {"message": f"❌ Educación con ID {id} no encontrada"}
    return educacion



"""

"""
PRUEBA DE LA EXPERIENCIA
"""
"""
#POST
# Endpoint de prueba para validar el schema
@app.post("/experiencia")
async def test_schema(experiencia: ExperienciaLaboralCreate):
    return {"message": "✅ Datos validados correctamente", "data": experiencia}

# PUT
@app.put("/experiencia/{id}")
async def update_experiencia(id: int, experiencia: ExperienciaLaboralCreate):
    return {"message": f"✅ Candidato {id} actualizado correctamente", "data": experiencia}

#GET
# Simulación de la base de datos de experiencia laboral
fake_db_experiencia = {
    1: {
        "id_experiencia": 1,
        "rango_experiencia": {
            "id_rango_experiencia": 3,
            "descripcion_rango": "3-5 años"
        },
        "ultima_empresa": "Constructora XYZ",
        "ultimo_cargo": "Ingeniero Residente",
        "funciones": "Supervisión de obra y coordinación de equipos de trabajo.",
        "fecha_inicio": "2018-06-15",
        "fecha_fin": "2022-07-30"
    }
}
@app.get("/experiencia/{id}")
async def get_experiencia(id: int):
    experiencia = fake_db_experiencia.get(id)
    if not experiencia:
        return {"message": f"❌ Experiencia con ID {id} no encontrada"}
    return experiencia



"""
"""PRUEBA DE LAS HAB BLANDAS"""
"""

#GET
# Simulación de la base de datos de habilidades blandas
# Simulación de la base de datos de habilidades blandas
fake_db_habilidades_blandas = {
    1: {
        "id": 1,
        "habilidad_blanda": {
            "id_habilidad_blanda": 3,
            "nombre_habilidad": "Trabajo en equipo"
        }
    },
    2: {
        "id": 2,
        "habilidad_blanda": {
            "id_habilidad_blanda": 5,
            "nombre_habilidad": "Liderazgo"
        }
    }
}

@app.get("/habilidad-blanda/{id}", response_model=HabilidadBlandaCandidatoResponse)
async def get_habilidad_blanda(id: int):
    habilidad = fake_db_habilidades_blandas.get(id)
    if not habilidad:
        return {"message": f"❌ Habilidad blanda con ID {id} no encontrada"}
    return habilidad

@app.post("/habilidad-blanda")
async def test_schema(habilidad_blanda: HabilidadBlandaCandidatoCreate):
    return {"message": "✅ Datos validados correctamente", "data": habilidad_blanda}

# PUT
@app.put("/habilidad-blanda/{id}")
async def update_experiencia(id: int, habilidad_blanda: HabilidadBlandaCandidatoCreate):
    return {"message": f"✅ Candidato {id} actualizado correctamente", "data": habilidad_blanda}



"""
"""PRUEBA DE LAS HAB TECNICAS"""
"""
# Simulación de la base de datos de habilidades técnicas
fake_db_habilidades_tecnicas = {
    1: {
        "id": 1,
        "habilidad_tecnica": {
            "id_habilidad_tecnica": 7,
            "nombre_habilidad": "Programación en Python",
            "categoria": {
                "id_categoria_habilidad": 2,
                "nombre_categoria": "Desarrollo de Software"
            }
        }
    },
    2: {
        "id": 2,
        "habilidad_tecnica": {
            "id_habilidad_tecnica": 12,
            "nombre_habilidad": "Análisis estructural",
            "categoria": {
                "id_categoria_habilidad": 4,
                "nombre_categoria": "Ingeniería Civil"
            }
        }
    }
}
@app.get("/habilidad-tecnica/{id}", response_model=HabilidadTecnicaCandidatoResponse)
async def get_habilidad_tecnica(id: int):
    habilidad = fake_db_habilidades_tecnicas.get(id)
    if not habilidad:
        return {"message": f"❌ Habilidad técnica con ID {id} no encontrada"}
    return habilidad

@app.post("/habilidad-tecnica")
async def test_schema(habilidad_tecnica: HabilidadTecnicaCandidatoCreate):
    return {"message": "✅ Datos validados correctamente", "data": habilidad_tecnica}

# PUT
@app.put("/habilidad-tecnica/{id}")
async def update_experiencia(id: int, habilidad_tecnica: HabilidadTecnicaCandidatoCreate):
    return {"message": f"✅ Candidato {id} actualizado correctamente", "data": habilidad_tecnica}





"""
"""PRUEBA DE LAS HERRAMIENTAS"""
"""



# Simulación de la base de datos de herramientas
fake_db_herramientas = {
    1: {
        "id": 1,
        "herramienta": {
            "id_herramienta": 10,
            "nombre_herramienta": "AutoCAD",
            "categoria": {
                "id_categoria_herramienta": 1,
                "nombre_categoria": "Diseño y Modelado"
            }
        }
    },
    2: {
        "id": 2,
        "herramienta": {
            "id_herramienta": 15,
            "nombre_herramienta": "Revit",
            "categoria": {
                "id_categoria_herramienta": 1,
                "nombre_categoria": "Diseño y Modelado"
            }
        }
    }
}


@app.get("/herramienta/{id}", response_model=HerramientaCandidatoResponse)
async def get_herramienta(id: int):
    herramienta = fake_db_herramientas.get(id)
    if not herramienta:
        return {"message": f"❌ Herramienta con ID {id} no encontrada"}
    return herramienta


@app.post("/herramientas")
async def test_schema(herramientas: HerramientaCandidatoCreate):
    return {"message": "✅ Datos validados correctamente", "data": herramientas}

# PUT
@app.put("/herramientas/{id}")
async def update_experiencia(id: int, herramientas: HerramientaCandidatoCreate):
    return {"message": f"✅ Candidato {id} actualizado correctamente", "data": herramientas}





"""
"""PRUEBA DE LAS PREFERENCIAS"""
"""
# Simulación de la base de datos de preferencias y disponibilidad
fake_db_preferencias = {
    1: {
        "id_preferencia": 1,
        "disponibilidad_viajar": True,
        "disponibilidad": {
            "id_disponibilidad": 2,
            "descripcion_disponibilidad": "Inmediata"
        },
        "rango_salarial": {
            "id_rango_salarial": 3,
            "descripcion_rango": "$3,000,000 - $4,000,000"
        },
        "trabaja_actualmente": False,
        "motivo_salida": {
            "id_motivo_salida": 5,
            "descripcion_motivo": "Crecimiento profesional"
        },
        "razon_trabajar_joyco": "Me interesa la innovación en ingeniería civil"
    },
    2: {
        "id_preferencia": 2,
        "disponibilidad_viajar": False,
        "disponibilidad": {
            "id_disponibilidad": 3,
            "descripcion_disponibilidad": "1 mes"
        },
        "rango_salarial": {
            "id_rango_salarial": 4,
            "descripcion_rango": "$4,000,000 - $5,000,000"
        },
        "trabaja_actualmente": True,
        "motivo_salida": None,
        "razon_trabajar_joyco": "Quiero aportar mi experiencia en grandes proyectos"
    }
}
@app.get("/preferencias/{id}", response_model=PreferenciaDisponibilidadResponse)
async def get_preferencias(id: int):
    preferencias = fake_db_preferencias.get(id)
    if not preferencias:
        return {"message": f"❌ Preferencias con ID {id} no encontradas"}
    return preferencias

@app.post("/preferencias")
async def test_schema(preferencias: PreferenciaDisponibilidadCreate):
    return {"message": "✅ Datos validados correctamente", "data": preferencias}

# PUT
@app.put("/preferencias/{id}")
async def update_experiencia(id: int, preferencias: PreferenciaDisponibilidadUpdate):
    return {"message": f"✅ Candidato {id} actualizado correctamente", "data": preferencias}

"""


