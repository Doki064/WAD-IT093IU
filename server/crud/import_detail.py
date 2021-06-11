from sqlalchemy.orm import Session

from models import ImportDetail
from schemas import ImportationCreate


async def create(db: Session, importation_detail: ImportationCreate, importation_uid: int,
                 item_uid: int) -> ImportDetail:
    db_importation_detail = ImportDetail(**importation_detail.dict(),
                                         importation_uid=importation_uid,
                                         item_uid=item_uid)
    db.add(db_importation_detail)
    await db.commit()
    return db_importation_detail
