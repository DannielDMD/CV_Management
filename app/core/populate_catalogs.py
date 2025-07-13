# app/core/populate_catalogs.py
import csv
import os
from app.core.database import SessionLocal
from app.models.catalogs import (
    Departamento,
    Ciudad,
    CargoOfrecido,
    CentroCostos,
    NivelEducacion,
    TituloObtenido,
    InstitucionAcademica,
    NivelIngles,
    RangoExperiencia,
)  # y los demás catálogos...
from app.models import (
    MotivoSalida,
    HabilidadBlanda,
    HabilidadTecnica,
    Herramienta,
    Disponibilidad,
    RangoSalarial,
)

# Rutas de archivos
BASE_DIR = os.path.dirname(__file__)
DEPTOS_CSV = os.path.join(BASE_DIR, "../data/departamentos.csv")
CIUDADES_CSV = os.path.join(BASE_DIR, "../data/ciudades.csv")
CARGOS_CSV = os.path.join(BASE_DIR, "../data/cargos-ofrecidos.csv")
CENTROS_CSV = os.path.join(BASE_DIR, "../data/centros-costos.csv")
MOTIVOS_CSV = os.path.join(BASE_DIR, "../data/motivos-salida.csv")
NIVEL_EDU_CSV = os.path.join(BASE_DIR, "../data/nivel-educacion.csv")
TITULOS_CSV = os.path.join(BASE_DIR, "../data/titulos.csv")
INSTITUCION_CSV = os.path.join(BASE_DIR, "../data/instituciones.csv")
NIVE_INGLES_CSV = os.path.join(BASE_DIR, "../data/nivel-ingles.csv")
RANGOS_EXP_CSV = os.path.join(BASE_DIR, "../data/rangos-experiencia.csv")
HAB_TEC_CSV = os.path.join(BASE_DIR, "../data/habilidades-tecnicas.csv")
HAB_BLAN_CSV = os.path.join(BASE_DIR, "../data/habilidades-blandas.csv")
HERRAMIENTAS_CSV = os.path.join(BASE_DIR, "../data/herramientas.csv")
DISPONIBILIDAD_CSV = os.path.join(BASE_DIR, "../data/disponibilidad.csv")
RANGO_SALARIAL_CSV = os.path.join(BASE_DIR, "../data/rangos-salariales.csv")

"""
Función que inserta los catalogos (Son 15 catálogos)
"""
def cargar_catalogos():
    db = SessionLocal()
    try:
        insertar_departamentos(db)
        insertar_ciudades(db)
        insertar_cargos_ofrecidos(db)
        insertar_centros_costos(db)
        insertar_motivos_salida(db)
        insertar_nivel_educacion(db)
        insertar_titulos_obtenidos(db)
        insertar_instituciones(db)
        insertar_niveles_ingles(db)
        insertar_rangos_experiencia(db)
        insertar_habilidades_blandas(db)
        insertar_habilidades_tecnicas(db)
        insertar_herramientas(db)
        insertar_disponibilidades(db)
        insertar_rangos_salariales(db)
    finally:
        db.close()


# -----------------------------
# FUNCIONES MODULARES POR CATÁLOGO
# -----------------------------


def insertar_departamentos(db):
    if db.query(Departamento).count() == 0:
        print("✅ Insertando departamentos desde CSV...")
        with open(DEPTOS_CSV, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            departamentos = [
                Departamento(nombre_departamento=row["nombre_departamento"])
                for row in reader
            ]
        db.add_all(departamentos)
        db.commit()
        print(f"✅ {len(departamentos)} departamentos insertados.")
    else:
        print("ℹ️ Departamentos ya existen. No se insertó nada.")


def insertar_ciudades(db):
    if db.query(Ciudad).count() == 0:
        print("✅ Insertando ciudades desde CSV...")
        with open(CIUDADES_CSV, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=";")
            ciudades = []
            for row in reader:
                departamento = (
                    db.query(Departamento)
                    .filter_by(nombre_departamento=row["nombre_departamento"])
                    .first()
                )
                if departamento:
                    ciudad = Ciudad(
                        nombre_ciudad=row["nombre_ciudad"],
                        id_departamento=departamento.id_departamento,
                    )
                    ciudades.append(ciudad)
                else:
                    print(
                        f"⚠️ Departamento no encontrado: {row['nombre_departamento']} (ciudad: {row['nombre_ciudad']})"
                    )
        db.add_all(ciudades)
        db.commit()
        print(f"✅ {len(ciudades)} ciudades insertadas.")
    else:
        print("ℹ️ Ciudades ya existen. No se insertó nada.")


def insertar_cargos_ofrecidos(db):
    if db.query(CargoOfrecido).count() == 0:
        print("✅ Insertando cargos ofrecidos desde CSV...")

        with open(CARGOS_CSV, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=";")  # o "," si usaste coma
            cargos = [
                CargoOfrecido(nombre_cargo=row["nombre_cargo"].strip())
                for row in reader
            ]

        db.add_all(cargos)
        db.commit()
        print(f"✅ Se insertaron {len(cargos)} cargos ofrecidos.")
    else:
        print("ℹ️ La tabla 'cargos_ofrecidos' ya contiene datos. No se insertó nada.")


def insertar_centros_costos(db):
    if db.query(CentroCostos).count() == 0:
        print("✅ Insertando centros de costos desde CSV...")

        with open(CENTROS_CSV, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=";")  # o "," si usaste coma
            centros = [
                CentroCostos(nombre_centro_costos=row["nombre_centro_costos"].strip())
                for row in reader
            ]

        db.add_all(centros)
        db.commit()
        print(f"✅ Se insertaron {len(centros)} Centros de Costos.")
    else:
        print("ℹ️ La tabla 'centros_costos' ya contiene datos. No se insertó nada.")


def insertar_motivos_salida(db):
    if db.query(MotivoSalida).count() == 0:
        print("✅ Insertando motivos de salida desde CSV...")

        with open(MOTIVOS_CSV, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=";")  # o "," si usaste coma
            motivos = [
                MotivoSalida(descripcion_motivo=row["descripcion_motivo"].strip())
                for row in reader
            ]

        db.add_all(motivos)
        db.commit()
        print(f"✅ Se insertaron {len(motivos)} Motivos de Salida.")
    else:
        print("ℹ️ La tabla 'motivos_salida' ya contiene datos. No se insertó nada.")


# -----------------------------
# CATÁLOGOS DE EDUCACIÓN
# -----------------------------
def insertar_nivel_educacion(db):
    if db.query(NivelEducacion).count() == 0:
        print("✅ Insertando niveles de educación desde CSV...")

        with open(NIVEL_EDU_CSV, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=";")  # o "," si usaste coma
            nivel = [
                NivelEducacion(descripcion_nivel=row["descripcion_nivel"].strip())
                for row in reader
            ]

        db.add_all(nivel)
        db.commit()
        print(f"✅ Se insertaron {len(nivel)} niveles de educación.")
    else:
        print("ℹ️ La tabla 'nivel_educacion' ya contiene datos. No se insertó nada.")


def insertar_titulos_obtenidos(db):
    if db.query(TituloObtenido).count() == 0:
        print("✅ Insertando títulos obtenidos desde CSV...")

        with open(TITULOS_CSV, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=";")
            titulos = []
            print("Encabezados detectados:", reader.fieldnames)
            for row in reader:
                nivel = (
                    db.query(NivelEducacion)
                    .filter_by(descripcion_nivel=row["descripcion_nivel"])
                    .first()
                )
                if nivel:
                    titulo = TituloObtenido(
                        nombre_titulo=row["nombre_titulo"].strip(),
                        id_nivel_educacion=nivel.id_nivel_educacion,
                    )
                    titulos.append(titulo)
                else:
                    print(
                        f"⚠️ Nivel educativo no encontrado: {row['descripcion_nivel']} (título: {row['nombre_titulo']})"
                    )

        db.add_all(titulos)
        db.commit()
        print(f"✅ {len(titulos)} títulos insertados.")
    else:
        print("ℹ️ La tabla 'titulos_obtenidos' ya contiene datos. No se insertó nada.")


def insertar_instituciones(db):
    if db.query(InstitucionAcademica).count() == 0:
        print("✅ Insertando instituciones desde CSV...")

        with open(INSTITUCION_CSV, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=";")  # o "," si usaste coma
            institucion = [
                InstitucionAcademica(
                    nombre_institucion=row["nombre_institucion"].strip()
                )
                for row in reader
            ]

        db.add_all(institucion)
        db.commit()
        print(f"✅ Se insertaron {len(institucion)} instituciones.")
    else:
        print(
            "ℹ️ La tabla 'instituciones_academicas' ya contiene datos. No se insertó nada."
        )


def insertar_niveles_ingles(db):
    if db.query(NivelIngles).count() == 0:
        print("✅ Insertando niveles de ingles desde CSV...")

        with open(NIVE_INGLES_CSV, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=";")  # o "," si usaste coma
            niveles = [NivelIngles(nivel=row["nivel"].strip()) for row in reader]

        db.add_all(niveles)
        db.commit()
        print(f"✅ Se insertaron {len(niveles)} niveles de ingles.")
    else:
        print("ℹ️ La tabla 'nivel_ingles' ya contiene datos. No se insertó nada.")


# -----------------------------
# CATÁLOGOS DE EXPERIENCIA
# -----------------------------


def insertar_rangos_experiencia(db):
    if db.query(RangoExperiencia).count() == 0:
        print("✅ Insertando rangos de experiencia desde CSV...")

        with open(RANGOS_EXP_CSV, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=";")  # o "," si usaste coma
            rangos = [
                RangoExperiencia(descripcion_rango=row["descripcion_rango"].strip())
                for row in reader
            ]

        db.add_all(rangos)
        db.commit()
        print(f"✅ Se insertaron {len(rangos)} rangos de experiencia.")
    else:
        print("ℹ️ La tabla 'rangos_experiencia' ya contiene datos. No se insertó nada.")


# -----------------------------
# CATÁLOGOS DE CONOCIMIENTOS
# -----------------------------

def insertar_habilidades_tecnicas(db):
    if db.query(HabilidadTecnica).count() == 0:
        print("✅ Insertando habilidades técnicas desde CSV...")

        with open(HAB_TEC_CSV, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=";")  # o "," si usaste coma
            habilidades = [
                HabilidadTecnica(nombre_habilidad_tecnica=row["nombre_habilidad_tecnica"].strip())
                for row in reader
            ]

        db.add_all(habilidades)
        db.commit()
        print(f"✅ Se insertaron {len(habilidades)} habilidades técnicas.")
    else:
        print("ℹ️ La tabla 'habilidades_tecnicas' ya contiene datos. No se insertó nada.")


def insertar_habilidades_blandas(db):
    if db.query(HabilidadBlanda).count() == 0:
        print("✅ Insertando habilidades blandas desde CSV...")

        with open(HAB_BLAN_CSV, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=";")  # o "," si usaste coma
            habilidades = [
                HabilidadBlanda(nombre_habilidad_blanda=row["nombre_habilidad_blanda"].strip())
                for row in reader
            ]

        db.add_all(habilidades)
        db.commit()
        print(f"✅ Se insertaron {len(habilidades)} habilidades blandas.")
    else:
        print("ℹ️ La tabla 'habilidades_blandas' ya contiene datos. No se insertó nada.")
        
        
def insertar_herramientas(db):
    if db.query(Herramienta).count() == 0:
        print("✅ Insertando herramientas desde CSV...")

        with open(HERRAMIENTAS_CSV, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=";")  # o "," si usaste coma
            herramientas = [
                Herramienta(nombre_herramienta=row["nombre_herramienta"].strip())
                for row in reader
            ]

        db.add_all(herramientas)
        db.commit()
        print(f"✅ Se insertaron {len(herramientas)} herramientas.")
    else:
        print("ℹ️ La tabla 'herramientas' ya contiene datos. No se insertó nada.")

# -----------------------------
# CATÁLOGOS DE PREFERENCIAS
# -----------------------------

def insertar_disponibilidades(db):
    if db.query(Disponibilidad).count() == 0:
        print("✅ Insertando disponibilidades desde CSV...")

        with open(DISPONIBILIDAD_CSV, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=";")  # o "," si usaste coma
            disponibilidad = [
                Disponibilidad(descripcion_disponibilidad=row["descripcion_disponibilidad"].strip())
                for row in reader
            ]

        db.add_all(disponibilidad)
        db.commit()
        print(f"✅ Se insertaron {len(disponibilidad)} disponibilidades.")
    else:
        print("ℹ️ La tabla 'disponibilidades' ya contiene datos. No se insertó nada.")
        
        

def insertar_rangos_salariales(db):
    if db.query(RangoSalarial).count() == 0:
        print("✅ Insertando rangos salariales desde CSV...")

        with open(RANGO_SALARIAL_CSV, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=";")  # o "," si usaste coma
            rangos = [
                RangoSalarial(descripcion_rango=row["descripcion_rango"].strip())
                for row in reader
            ]

        db.add_all(rangos)
        db.commit()
        print(f"✅ Se insertaron {len(rangos)} rangos salarialess.")
    else:
        print("ℹ️ La tabla 'rangos_salariales' ya contiene datos. No se insertó nada.")
