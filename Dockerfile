# Dockerfile
FROM python:3.10.4

# Install Chrome
RUN apt-get update && apt-get install -y wget gnupg2
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

ENV DB_HOST=host.docker.internal
ENV DB_NAME=gruppi
ENV DB_USER=root
ENV DB_PASSWORD=password

# Installa le dipendenze necessarie
RUN apt-get update && apt-get install -y \
    python3-pyqt5 \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Copia il codice dell'applicazione nel container
COPY . /app
WORKDIR /app

# Installa le dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando per eseguire l'applicazione
CMD ["python", "main.py"]