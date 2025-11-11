FROM python:3.9
WORKDIR usr/local/app
EXPOSE 8080

RUN apt-get update && apt-get install -y \
    libglu1-mesa \
    libgl1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY AI ./AI
COPY Utils ./Utils
COPY backend ./backend
COPY MoveNet ./MoveNet
COPY OlympicAi.sln ./

RUN mkdir ProcessedVideos

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
