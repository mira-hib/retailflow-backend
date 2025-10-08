# Étape 1 : Image de base
FROM python:3.11-slim

# Étape 2 : Définir le répertoire de travail
WORKDIR /app

# Étape 3 : Empêcher Python d’écrire des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Étape 4 : Installer les dépendances
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Étape 5 : Copier tout le projet dans le conteneur
COPY . .

# Étape 6 : Exposer le port 8000
EXPOSE 8000

# Étape 7 : Commande de lancement (Gunicorn)
CMD ["gunicorn", "retailflow.wsgi:application", "--bind", "0.0.0.0:8000"]
