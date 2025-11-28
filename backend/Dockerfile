# ===========================
# BASE IMAGE
# ===========================
FROM python:3.10-slim

# Prevent prompts
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# ===========================
# SYSTEM DEPENDENCIES
# ===========================
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1 libsm6 libxext6 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ===========================
# COPY PROJECT
# ===========================
COPY . .

# ===========================
# PYTHON DEPENDENCIES
# ===========================
RUN pip install --no-cache-dir -r requirements.txt

# ===========================
# EXPOSE API PORT
# ===========================
EXPOSE 8000

# ===========================
# DOWNLOAD MODELS
# ===========================
RUN python app/models_data/download_models.py


# ===========================
# RUN APPLICATION
# ===========================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
