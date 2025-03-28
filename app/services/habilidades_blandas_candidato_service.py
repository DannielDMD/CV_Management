"""from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.habilidades_blandas import HabilidadBlandaCandidato, HabilidadBlanda
from app.schemas.habilidades_blandas import HabilidadBlandaCandidatoCreate, HabilidadBlandaCandidatoListResponse, HabilidadBlandaResponse

def assign_habilidades_blandas(db: Session, habilidad_data: HabilidadBlandaCandidatoCreate):
    habilidades_asignadas = []
    
    for id_habilidad in habilidad_data.id_habilidades_blandas:
        existing_record = (
            db.query(HabilidadBlandaCandidato)
            .filter(
                HabilidadBlandaCandidato.id_candidato == habilidad_data.id_candidato,
                HabilidadBlandaCandidato.id_habilidad_blanda == id_habilidad,
            )
            .first()
        )

        if existing_record:
            continue  

        new_habilidad = HabilidadBlandaCandidato(
            id_candidato=habilidad_data.id_candidato,
            id_habilidad_blanda=id_habilidad
        )
        db.add(new_habilidad)
        habilidades_asignadas.append(new_habilidad)

    db.commit()

    # Convertir la respuesta al formato adecuado
    return [
        HabilidadBlandaCandidatoListResponse(
            id_candidato=h.id_candidato,
            habilidades_blandas=[
                HabilidadBlandaResponse(
                    id_habilidad_blanda=h.id_habilidad_blanda,
                    nombre_habilidad=db.query(HabilidadBlanda)
                    .filter(HabilidadBlanda.id_habilidad_blanda == h.id_habilidad_blanda)
                    .first()
                    .nombre_habilidad
                )
            ]
        ) for h in habilidades_asignadas
    ]

def get_habilidades_blandas_by_candidato(db: Session, id_candidato: int):
    habilidades = (
        db.query(HabilidadBlandaCandidato)
        .join(HabilidadBlanda, HabilidadBlanda.id_habilidad_blanda == HabilidadBlandaCandidato.id_habilidad_blanda)
        .filter(HabilidadBlandaCandidato.id_candidato == id_candidato)
        .all()
    )

    if not habilidades:
        raise HTTPException(
            status_code=404,
            detail="El candidato no tiene habilidades blandas registradas",
        )

    # Transformar la respuesta
    return HabilidadBlandaCandidatoListResponse(
        id_candidato=id_candidato,
        habilidades_blandas=[
            HabilidadBlandaResponse(
                id_habilidad_blanda=h.id_habilidad_blanda,
                nombre_habilidad=h.habilidad_blanda.nombre_habilidad
            ) for h in habilidades
        ]
    )


# Eliminar una habilidad blanda de un candidato
def remove_habilidad_blanda(db: Session, id_candidato: int, id_habilidad_blanda: int):
    habilidad = (
        db.query(HabilidadBlandaCandidato)
        .filter(
            HabilidadBlandaCandidato.id_candidato == id_candidato,
            HabilidadBlandaCandidato.id_habilidad_blanda == id_habilidad_blanda,
        )
        .first()
    )

    if not habilidad:
        raise HTTPException(
            status_code=404,
            detail="La habilidad blanda no está asignada a este candidato",
        )

    db.delete(habilidad)
    db.commit()

    return {"message": "Habilidad blanda eliminada correctamente"}
"""