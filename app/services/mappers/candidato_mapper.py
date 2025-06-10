from app.models.candidato_model import Candidato
from app.schemas.candidato_schema import CandidatoDetalleResponse, CandidatoResumenResponse


def mapear_candidato_detalle(candidato: Candidato) -> CandidatoDetalleResponse:
    educacion = candidato.educaciones[0] if candidato.educaciones else None
    experiencia = candidato.experiencias[0] if candidato.experiencias else None
    preferencias = candidato.preferencias[0] if candidato.preferencias else None

    habilidades_blandas = [
        c.habilidad_blanda.nombre_habilidad_blanda
        for c in candidato.conocimientos
        if c.tipo_conocimiento == "blanda" and c.habilidad_blanda
    ]
    habilidades_tecnicas = [
        c.habilidad_tecnica.nombre_habilidad_tecnica
        for c in candidato.conocimientos
        if c.tipo_conocimiento == "tecnica" and c.habilidad_tecnica
    ]
    herramientas = [
        c.herramienta.nombre_herramienta
        for c in candidato.conocimientos
        if c.tipo_conocimiento == "herramienta" and c.herramienta
    ]

    return CandidatoDetalleResponse(
        id_candidato=candidato.id_candidato,  # 🔴 AGREGA ESTA LÍNEA
        nombre_completo=candidato.nombre_completo,
        correo_electronico=candidato.correo_electronico,
        cc=candidato.cc,
        fecha_nacimiento=candidato.fecha_nacimiento,
        telefono=candidato.telefono,
        departamento=candidato.ciudad.departamento.nombre_departamento if candidato.ciudad and candidato.ciudad.departamento else None,
        ciudad=candidato.ciudad.nombre_ciudad,
        descripcion_perfil=candidato.descripcion_perfil,
        cargo=candidato.cargo.nombre_cargo,
        nombre_cargo_otro=candidato.nombre_cargo_otro,
        trabaja_actualmente_joyco=candidato.trabaja_actualmente_joyco,
        centro_costos=candidato.centro_costos.nombre_centro_costos if candidato.centro_costos else None,
        nombre_centro_costos_otro=candidato.nombre_centro_costos_otro,
        ha_trabajado_joyco=candidato.ha_trabajado_joyco,
        motivo_salida=candidato.motivo_salida.descripcion_motivo if candidato.motivo_salida else None,
        otro_motivo_salida_candidato=candidato.otro_motivo_salida,
        tiene_referido=candidato.tiene_referido,
        nombre_referido=candidato.nombre_referido,
        fecha_registro=candidato.fecha_registro,
        estado=candidato.estado,
        nivel_educacion=educacion.nivel_educacion.descripcion_nivel if educacion and educacion.nivel_educacion else None,
        titulo=educacion.titulo.nombre_titulo if educacion and educacion.titulo else None,
        nombre_titulo_otro=educacion.nombre_titulo_otro if educacion else None,
        institucion=educacion.institucion.nombre_institucion if educacion and educacion.institucion else None,
        nombre_institucion_otro=educacion.nombre_institucion_otro if educacion else None,
        anio_graduacion=educacion.anio_graduacion if educacion else None,
        nivel_ingles=educacion.nivel_ingles.nivel if educacion and educacion.nivel_ingles else None,
        rango_experiencia=experiencia.rango_experiencia.descripcion_rango if experiencia and experiencia.rango_experiencia else None,
        ultima_empresa=experiencia.ultima_empresa if experiencia else None,
        ultimo_cargo=experiencia.ultimo_cargo if experiencia else None,
        funciones=experiencia.funciones if experiencia else None,
        fecha_inicio=experiencia.fecha_inicio if experiencia else None,
        fecha_fin=experiencia.fecha_fin if experiencia else None,
        habilidades_blandas=habilidades_blandas,
        habilidades_tecnicas=habilidades_tecnicas,
        herramientas=herramientas,
        disponibilidad_viajar=preferencias.disponibilidad_viajar if preferencias else None,
        disponibilidad_inicio=preferencias.disponibilidad.descripcion_disponibilidad if preferencias and preferencias.disponibilidad else None,
        rango_salarial=preferencias.rango_salarial.descripcion_rango if preferencias and preferencias.rango_salarial else None,
        trabaja_actualmente=preferencias.trabaja_actualmente if preferencias else None,
        motivo_salida_laboral=preferencias.motivo_salida.descripcion_motivo if preferencias and preferencias.motivo_salida else None,
        otro_motivo_salida_preferencia=preferencias.otro_motivo_salida if preferencias else None,
        razon_trabajar_joyco=preferencias.razon_trabajar_joyco if preferencias else None
    )

def mapear_candidato_resumen(candidato):
    educacion = candidato.educaciones[0] if candidato.educaciones else None
    experiencia = candidato.experiencias[0] if candidato.experiencias else None
    preferencias = candidato.preferencias[0] if candidato.preferencias else None

    habilidades_blandas = [
        c.habilidad_blanda.nombre_habilidad_blanda
        for c in candidato.conocimientos
        if c.tipo_conocimiento == "blanda" and c.habilidad_blanda
    ]
    habilidades_tecnicas = [
        c.habilidad_tecnica.nombre_habilidad_tecnica
        for c in candidato.conocimientos
        if c.tipo_conocimiento == "tecnica" and c.habilidad_tecnica
    ]
    herramientas = [
        c.herramienta.nombre_herramienta
        for c in candidato.conocimientos
        if c.tipo_conocimiento == "herramienta" and c.herramienta
    ]

    return CandidatoResumenResponse(
        id_candidato=candidato.id_candidato,
        nombre_completo=candidato.nombre_completo,
        correo_electronico=candidato.correo_electronico,
        telefono=candidato.telefono,
        ciudad=candidato.ciudad.nombre_ciudad if candidato.ciudad else None,
        cargo_ofrecido=candidato.cargo.nombre_cargo if candidato.cargo else None,
        nivel_educativo=(
            educacion.nivel_educacion.descripcion_nivel if educacion and educacion.nivel_educacion else None
        ),
        titulo_obtenido=(
            educacion.titulo.nombre_titulo if educacion and educacion.titulo else None
        ),
        rango_experiencia=(
            experiencia.rango_experiencia.descripcion_rango if experiencia and experiencia.rango_experiencia else None
        ),
        habilidades_blandas=habilidades_blandas,
        habilidades_tecnicas=habilidades_tecnicas,
        herramientas=herramientas,
        disponibilidad_inicio=(
            preferencias.disponibilidad.descripcion_disponibilidad if preferencias and preferencias.disponibilidad else None
        ),
        trabaja_actualmente_joyco=candidato.trabaja_actualmente_joyco,
        fecha_postulacion=candidato.fecha_registro,
        estado=candidato.estado,
    )
