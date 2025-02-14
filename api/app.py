from fastapi import FastAPI, HTTPException
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

# URL du service modèle
MODEL_URL = "http://model:5001"

# Configuration de la base de données
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "predictions")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# Fonction pour se connecter à la base de données
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor
    )
    return conn

@app.get("/predict")
async def predict():
    """Endpoint to get the prediction for the first row of test.csv and save it to the database"""
    try:
        # Envoyer une requête au service modèle
        response = requests.get(f"{MODEL_URL}/predict")
        response.raise_for_status()
        prediction = response.json()["prediction"]

        # Message à afficher
        message = f"La prédiction pour la première ligne du fichier test.csv est : {prediction}"

        # Sauvegarder la prédiction dans la base de données
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO predictions (input_data, prediction) VALUES (%s, %s)",
            ("First row of test.csv", prediction)
        )
        conn.commit()
        cur.close()
        conn.close()

        return {"message": message}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))