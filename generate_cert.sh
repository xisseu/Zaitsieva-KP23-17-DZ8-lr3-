#!/bin/bash
if [ ! -f /etc/nginx/server.crt ] || [ ! -f /etc/nginx/server.key ]; then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/nginx/server.key \
        -out /etc/nginx/server.crt \
        -subj "/CN=localhost"
fi