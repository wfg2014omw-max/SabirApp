FROM python:3.10-slim

WORKDIR /app

# ====== نصب المتطلبات الأساسية ======
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ====== نصب متصفح Chrome ======
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# الطريقة الصحيحة لتحميل Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y google-chrome-stable

COPY . .

CMD ["python", "bot.py"]
