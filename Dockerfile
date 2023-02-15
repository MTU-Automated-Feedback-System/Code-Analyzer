FROM python:3.10-alpine
WORKDIR /opt/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
WORKDIR src
CMD ["gunicorn", "wsgi:app", "-b 0.0.0.0:8080"]