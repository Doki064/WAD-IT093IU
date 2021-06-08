# from database.config import SessionLocal as _SessionLocal

# def get_db():
#     db = _SessionLocal()
#     try:
#         yield db
#     except Exception:
#         db.rollback()
#     finally:
#         db.close()
