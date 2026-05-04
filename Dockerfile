FROM python:3.11-slim

RUN apt-get update && apt-get install -y nginx openssl

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY generate_cert.sh /generate_cert.sh
RUN chmod +x /generate_cert.sh && /generate_cert.sh

COPY . .

EXPOSE 80 443

CMD ["sh", "-c", "nginx && python main.py"]
