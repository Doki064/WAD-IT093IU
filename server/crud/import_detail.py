from sqlalchemy.orm import Session

from models import ImportDetail
from schemas import ImportationCreate


def create(db: Session, importation_detail: ImportationCreate, importation_uid: int,
           item_uid: int):
    db_importation_detail = ImportDetail(**importation_detail.dict(),
                                         importation_uid=importation_uid,
                                         item_uid=item_uid)
    db.add(db_importation_detail)
    db.commit()
    db.refresh(db_importation_detail)
    return db_importation_detail


def get_by_importation(db: Session, importation_uid: int):
    return db.query(ImportDetail).filter(
        ImportDetail.importation_uid == importation_uid).all()
