import pytest
import subprocess
import ssl
import socket
import requests

class TestSecureTrustHTTPS:

    def test_http_redirect_to_https(self):
        """Проверка: HTTP-запрос должен перенаправляться на HTTPS"""
        result = subprocess.run(
            ["curl", "-I", "-s", "http://localhost:80"],
            capture_output=True, text=True
        )
        assert "301" in result.stdout
        assert "Location: https://" in result.stdout

    def test_https_accessible(self):
        """Проверка: HTTPS-порт должен быть доступен и отвечать кодом 200"""
        result = subprocess.run(
            ["curl", "-k", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "https://localhost:443/api/health"],
            capture_output=True, text=True
        )
        assert result.stdout == "200"

    def test_ssl_certificate_exists(self):
        """Проверка: SSL-сертификат должен быть установлен"""
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with socket.create_connection(("localhost", 443)) as sock:
            with context.wrap_socket(sock, server_hostname="localhost") as ssock:
                cert = ssock.getpeercert()
                assert cert is not None
                assert "subject" in cert

    def test_api_transfer_over_https(self):
        """Проверка: API перевода должен работать через HTTPS"""
        response = requests.post(
            "https://localhost:443/api/transfer",
            json={"from": "ACC1", "to": "ACC2", "amount": 100},
            verify=False
        )
        assert response.status_code == 200
        assert response.json().get("success") is True
