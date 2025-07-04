from .db import SessinLocal

# Dependencies

def get_db():
    db = SessinLocal()
    try:
        yield db
    finally:
        db.close()