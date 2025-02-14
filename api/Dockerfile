# Utilisez une image de base Python
FROM python:3.9-slim

# Définissez le répertoire de travail
WORKDIR /app

# Copiez les fichiers nécessaires
COPY . .

# Installez les dépendances
RUN pip install -r requirements.txt

# Commande pour exécuter l'API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]