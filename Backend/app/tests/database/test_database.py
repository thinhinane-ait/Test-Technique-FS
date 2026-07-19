from sqlalchemy import text 

from app.database.session import engine

try : 
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print('Connexion réussi : ', result.scalar())

except Exception as error :
    print('erreur de connexion : ', error)