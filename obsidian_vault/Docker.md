# Docker - Notatka

## 1. Czym jest Docker?
Docker to platforma do tworzenia, uruchamiania i zarządzania kontenerami. Kontenery umożliwiają uruchamianie aplikacji w izolowanych środowiskach, co zapewnia ich przenośność i spójność niezależnie od infrastruktury.

## 2. Podstawowe pojęcia
- **Obraz (Image)** – gotowy pakiet aplikacji z zależnościami.
- **Kontener (Container)** – uruchomiona instancja obrazu.
- **Dockerfile** – plik definiujący sposób budowania obrazu.
- **Docker Compose** – narzędzie do zarządzania wieloma kontenerami.
- **Registry** – repozytorium obrazów (np. Docker Hub).

## 3. Podstawowe komendy
### Zarządzanie obrazami
```bash
# Pobranie obrazu
docker pull <nazwa_obrazu>

# Wyświetlenie listy obrazów
docker images

# Usunięcie obrazu
docker rmi <id_obrazu>
```

### Zarządzanie kontenerami
```bash
# Uruchomienie kontenera
docker run -d --name <nazwa> <obraz>

# Lista uruchomionych kontenerów
docker ps

# Zatrzymanie kontenera
docker stop <id_kontenera>

# Usunięcie kontenera
docker rm <id_kontenera>
```

### Docker Compose
```bash
# Uruchomienie kontenerów na podstawie docker-compose.yml
docker-compose up -d

# Zatrzymanie kontenerów
docker-compose down
```

## 4. Tworzenie własnego obrazu
1. Utwórz plik `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```
2. Zbuduj obraz:
```bash
docker build -t myapp .
```
1. Uruchom kontener:
```bash
docker run -d -p 5000:5000 myapp
```

## 5. Praca z woluminami
```bash
# Tworzenie woluminu
docker volume create myvolume

# Uruchomienie kontenera z woluminem
docker run -v myvolume:/data myapp
```

## 6. Sieci w Dockerze
```bash
# Wyświetlenie listy sieci
docker network ls

# Tworzenie sieci
docker network create mynetwork

# Uruchomienie kontenera w sieci
docker run --network mynetwork myapp
```

## 7. Debugowanie
```bash
# Wejście do działającego kontenera
docker exec -it <id_kontenera> /bin/sh

# Logi kontenera
docker logs <id_kontenera>
```


#docker #containers