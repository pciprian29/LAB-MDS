# Folosim o versiune oficială și ușoară de Python
FROM python:3.9-slim

# Setăm un folder de lucru în interiorul containerului
WORKDIR /app

# Copiem fișierul cu pachetele necesare
COPY requirements.txt .

# Instalăm pachetele
RUN pip install --no-cache-dir -r requirements.txt

# Copiem doar aplicația meteo (așa cum cere laboratorul 2)
COPY meteo_app.py .

# Comanda care rulează aplicația la pornirea containerului
CMD ["python", "meteo_app.py"]
