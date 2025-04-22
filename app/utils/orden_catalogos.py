# utils/orden_catalogos.py
from sqlalchemy import asc, case


def ordenar_por_nombre(query, campo):
    """
    Recibe un query y el nombre del campo string a ordenar.
    Devuelve el query ordenado alfabéticamente, dejando 'Otro' u 'Otros' de últimos.
    """
    columna = getattr(query.column_descriptions[0]["entity"], campo)

    return query.order_by(
        case((columna.ilike("otro"), 1), (columna.ilike("otros"), 1), else_=0),
        asc(columna),
    )
