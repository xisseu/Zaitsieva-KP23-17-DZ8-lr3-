import os
import pytest
import json

from main import CryptoEnclave, SecureLogger, Calculator, TablePresenter, BankMicroservice

class TestCryptoEnclave:
    # 3.1 ST-TEST-001: Шифрование и дешифрование
    def test_encrypt_decrypt(self):
        enclave = CryptoEnclave()
        original = b"secret_banking_data_123"
        encrypted = enclave.encrypt_data(original)
        decrypted = enclave.decrypt_data(encrypted)
        assert original == decrypted

    # 3.2 ST-TEST-002: Аттестация анклава
    def test_attestation(self):
        enclave = CryptoEnclave()
        attest = enclave.attest("test_app_hash_12345678")
        assert attest["status"] == "trusted"
        assert len(attest["signature"]) > 0


class TestSecureLogger:
    # 3.3 ST-TEST-003: Целостность логов (подделка обнаруживается)
    def test_log_integrity_tampered(self):
        logger = SecureLogger()
        logger.log("TEST", "original message")

        assert logger.verify_integrity() == True

        with open("secure_audit.log", "a") as f:
            f.write("fake_entry|SIG:fake_signature\n")

        assert logger.verify_integrity() == False


class TestCalculator:
    # 3.4 ST-TEST-004: Расчёт статистики (пустые данные)
    def test_stats_empty(self):
        calc = Calculator()
        stats = calc.calculate_stats([])
        assert stats["total_income"] == 0
        assert stats["total_expense"] == 0
        assert stats["balance"] == 0

    # 3.5 ST-TEST-005: Расчёт статистики (полные данные)
    def test_stats_valid(self):
        calc = Calculator()
        transactions = [
            {"type": "income", "amount": 1000},
            {"type": "income", "amount": 500},
            {"type": "expense", "amount": 200},
            {"type": "expense", "amount": 300},
        ]
        stats = calc.calculate_stats(transactions)
        assert stats["total_income"] == 1500
        assert stats["total_expense"] == 500
        assert stats["balance"] == 1000
        assert stats["avg_income"] == 750
        assert stats["avg_expense"] == 250


class TestTablePresenter:
    # 3.6 ST-TEST-006: Группировка по категориям
    def test_group_by_category(self):
        presenter = TablePresenter()
        transactions = [
            {"type": "expense", "category": "food", "amount": 500},
            {"type": "expense", "category": "food", "amount": 300},
            {"type": "expense", "category": "transport", "amount": 200},
            {"type": "income", "category": "salary", "amount": 1000},
        ]
        grouped = presenter.group_by_category(transactions)
        assert grouped["expenses"]["food"] == 800
        assert grouped["expenses"]["transport"] == 200
        assert grouped["incomes"]["salary"] == 1000


class TestUB021Protection:
    # 3.7 ST-TEST-007: Защита от УБИ.021 (чтение файла)
    def setup_method(self):
        if os.path.exists("bank.encrypted"):
            os.remove("bank.encrypted")
        if os.path.exists("secure_audit.log"):
            os.remove("secure_audit.log")

    def test_ub021_protection(self):
        enclave1 = CryptoEnclave()
        logger = SecureLogger()
        bank = BankMicroservice(enclave1, logger)

        bank.add_transaction("income", 1000, "test")

        assert os.path.exists("bank.encrypted")

        with open("bank.encrypted", "r") as f:
            content = f.read()

        assert '"transactions"' not in content

        enclave2 = CryptoEnclave()

        with open("bank.encrypted", "r") as f:
            encrypted_data = json.load(f)

        try:
            decrypted = enclave2.decrypt_data(encrypted_data)
            try:
                json.loads(decrypted.decode())
                data_readable = True
            except:
                data_readable = False
        except:
            data_readable = False

        assert data_readable == False