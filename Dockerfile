FROM python:3.10

# Set port ke 7860 (Standar Hugging Face)
ENV PORT=7860
EXPOSE 7860

WORKDIR /app

# Copy dan install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file project
COPY . .

# Jalankan perintah gunicorn
# Ganti 'Website' dengan nama folder yang berisi wsgi.py kamu
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "Website.wsgi"]