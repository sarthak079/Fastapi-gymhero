from sqlmodel import SQLModel, create_engine, Session
from .models import Hero ,Workout, Exercise

# sqlite_file_name="database.db"
# sqlite_url=f"sqlite:///database.db"
DATABASE_URL = f"sqlite:///gymhero.db"

engine=create_engine(DATABASE_URL,echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session