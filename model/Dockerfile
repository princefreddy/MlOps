# Utilisez une image de base Python
FROM python:3.11-slim

# Définissez le répertoire de travail
WORKDIR /app

# Copiez les fichiers nécessaires
COPY . .

# Installez les dépendances
RUN pip install -r requirements.txt

# Commande pour exécuter le modèle avec FastAPI
CMD ["uvicorn", "deploy:app", "--host", "0.0.0.0", "--port", "5001"]