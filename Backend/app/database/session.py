#Backend/app/database/session.py


#connexion à la BD 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings




engine = create_engine(

        settings.database_url,
        echo=settings.debug

)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)