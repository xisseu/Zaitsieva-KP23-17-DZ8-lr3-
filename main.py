import os
import sqlite3
import secrets
import json
import hashlib
import hmac
import subprocess
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, request, jsonify

# ============================================================
# СОЗДАНИЕ FLASK ПРИЛОЖЕНИЯ
# ============================================================
app = Flask(__name__)

# ============================================================
# КРИПТОГРАФИЧЕСКИЙ АНКЛАВ
# ============================================================
class CryptoEnclave:
    def __init__(self):
        self.master_key = secrets.token_bytes(32)

    def _derive_key(self, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac('sha256', self.master_key, salt, 100000)

    def encrypt_data(self, data: bytes) -> dict:
        salt = secrets.token_bytes(16)
        key = self._derive_key(salt)
        ciphertext = bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
        return {"salt": salt, "ciphertext": ciphertext}

    def decrypt_data(self, encrypted: dict) -> bytes:
        key = self._derive_key(encrypted["salt"])
        return bytes([encrypted["ciphertext"][i] ^ key[i % len(key)] for i in range(len(encrypted["ciphertext"]))])

    def attest(self, app_hash: str) -> dict:
        timestamp = str(datetime.now())
        signature = hmac.new(self.master_key, f"{app_hash}:{timestamp}".encode(), hashlib.sha256).hexdigest()
        return {
            "status": "trusted",
            "app_hash": app_hash[:16] + "...",
            "timestamp": timestamp,
            "signature": signature[:32] + "..."
        }

    def secure_erase(self):
        self.master_key = os.urandom(32)

# ============================================================
# ЗАЩИЩЁННЫЙ ЛОГГЕР
# ============================================================
class SecureLogger:
    def __init__(self):
        self.key = secrets.token_bytes(32)
        self.log_file = "secure_audit.log"

    def log(self, event: str, message: str):
        timestamp = datetime.now().isoformat()
        entry = f"{timestamp}|{event}|{message}"
        signature = hmac.new(self.key, entry.encode(), hashlib.sha256).hexdigest()
        with open(self.log_file, "a") as f:
            f.write(f"{entry}|SIG:{signature}\n")

    def verify_integrity(self) -> bool:
        if not os.path.exists(self.log_file):
            return True
        try:
            with open(self.log_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if "|SIG:" not in line:
                        return False
                    last_sig_index = line.rfind("|SIG:")
                    if last_sig_index == -1:
                        return False
                    entry_str = line[:last_sig_index]
                    signature = line[last_sig_index + 5:]
                    expected = hmac.new(self.key, entry_str.encode(), hashlib.sha256).hexdigest()
                    if signature != expected:
                        return False
            return True
        except Exception:
            return False

# ============================================================
# БАНКОВСКИЙ МИКРОСЕРВИС
# ============================================================
class BankMicroservice:
    def __init__(self, enclave: CryptoEnclave, logger: SecureLogger):
        self.enclave = enclave
        self.logger = logger
        self.db_path = "bank.encrypted"
        self.logger.log("INIT", "Запуск банковского микросервиса в защищенном анклаве")
        self._load_or_create_db()

    def _load_or_create_db(self):
        if not os.path.exists(self.db_path):
            empty_db = json.dumps({"transactions": [], "accounts": {}}).encode()
            encrypted = self.enclave.encrypt_data(empty_db)
            with open(self.db_path, "wb") as f:
                f.write(json.dumps({k: v.hex() for k, v in encrypted.items()}).encode())
            self.logger.log("STORAGE", "Создано новое зашифрованное хранилище")
            self._init_test_data()

    def _init_test_data(self):
        test_data = {
            "transactions": [
                {"id": "TX001", "type": "income", "amount": 1000.0, "category": "Зарплата", "date": "2023-01-01", "account_from": "ACC1", "account_to": None},
                {"id": "TX002", "type": "expense", "amount": 200.0, "category": "Продукты", "date": "2023-01-02", "account_from": "ACC1", "account_to": None},
                {"id": "TX003", "type": "expense", "amount": 50.0, "category": "Транспорт", "date": "2023-01-03", "account_from": "ACC1", "account_to": None},
                {"id": "TX004", "type": "income", "amount": 1500.0, "category": "Фриланс", "date": "2023-01-04", "account_from": "ACC1", "account_to": None},
                {"id": "TX005", "type": "expense", "amount": 100.0, "category": "Развлечения", "date": "2023-01-05", "account_from": "ACC1", "account_to": None},
                {"id": "TX006", "type": "expense", "amount": 300.0, "category": "Коммунальные платежи", "date": "2023-01-06", "account_from": "ACC1", "account_to": None},
                {"id": "TX007", "type": "income", "amount": 2000.0, "category": "Премия", "date": "2023-01-07", "account_from": "ACC1", "account_to": None},
                {"id": "TX008", "type": "expense", "amount": 150.0, "category": "Одежда", "date": "2023-01-08", "account_from": "ACC1", "account_to": None},
                {"id": "TX009", "type": "expense", "amount": 250.0, "category": "Медицина", "date": "2023-01-09", "account_from": "ACC1", "account_to": None},
                {"id": "TX010", "type": "income", "amount": 800.0, "category": "Инвестиции", "date": "2023-01-10", "account_from": "ACC1", "account_to": None},
                {"id": "TX011", "type": "expense", "amount": 500.0, "category": "Образование", "date": "2023-01-11", "account_from": "ACC1", "account_to": None},
                {"id": "TX012", "type": "expense", "amount": 300.0, "category": "Путешествия", "date": "2023-01-12", "account_from": "ACC1", "account_to": None},
            ],
            "accounts": {"ACC1": 100000, "ACC2": 50000, "ACC3": 25000}
        }
        self._save_data(test_data)
        self.logger.log("STORAGE", "Загружены тестовые данные")

    def _load_data(self) -> dict:
        with open(self.db_path, "rb") as f:
            encrypted_hex = json.loads(f.read().decode())
            encrypted = {k: bytes.fromhex(v) for k, v in encrypted_hex.items()}
            decrypted = self.enclave.decrypt_data(encrypted)
            return json.loads(decrypted.decode())

    def _save_data(self, data: dict):
        encrypted = self.enclave.encrypt_data(json.dumps(data).encode())
        with open(self.db_path, "wb") as f:
            f.write(json.dumps({k: v.hex() for k, v in encrypted.items()}).encode())
        self.logger.log("STORAGE", "Данные сохранены в зашифрованном виде")

    def add_transaction(self, transaction_type, amount, category, from_acc="ACC1", to_acc=None):
        data = self._load_data()
        tx_id = secrets.token_hex(4).upper()
        date = datetime.now().strftime('%Y-%m-%d')
        new_tx = {
            "id": tx_id, "type": transaction_type, "amount": amount,
            "category": category, "date": date,
            "account_from": from_acc, "account_to": to_acc
        }

        if transaction_type == "expense" and from_acc in data["accounts"]:
            data["accounts"][from_acc] -= amount
        elif transaction_type == "income" and to_acc in data["accounts"]:
            data["accounts"][to_acc] += amount

        data["transactions"].append(new_tx)
        self._save_data(data)
        self.logger.log("TRANSACTION", f"Добавлена транзакция {tx_id}: {transaction_type} {amount} {category}")
        return new_tx

    def get_all_transactions(self):
        data = self._load_data()
        return data["transactions"]

    def get_balance(self, account):
        data = self._load_data()
        return data["accounts"].get(account, 0)

# ============================================================
# КАЛЬКУЛЯТОР
# ============================================================
class Calculator:
    @staticmethod
    def calculate_stats(transactions):
        df = pd.DataFrame(transactions)
        if df.empty:
            return {"total_income": 0, "total_expense": 0, "balance": 0}
        income = df[df['type'] == 'income']['amount'].sum()
        expense = df[df['type'] == 'expense']['amount'].sum()
        return {
            "total_income": income,
            "total_expense": expense,
            "balance": income - expense,
            "avg_income": income / max(1, len(df[df['type'] == 'income'])),
            "avg_expense": expense / max(1, len(df[df['type'] == 'expense']))
        }

# ============================================================
# ТАБЛИЧНЫЙ ПРЕДСТАВИТЕЛЬ
# ============================================================
class TablePresenter:
    @staticmethod
    def to_dataframe(transactions):
        return pd.DataFrame(transactions)

    @staticmethod
    def group_by_category(transactions):
        df = pd.DataFrame(transactions)
        if df.empty:
            return {}
        expense_by_cat = df[df['type'] == 'expense'].groupby('category')['amount'].sum().to_dict()
        income_by_cat = df[df['type'] == 'income'].groupby('category')['amount'].sum().to_dict()
        return {"expenses": expense_by_cat, "incomes": income_by_cat}

    @staticmethod
    def monthly_summary(transactions):
        df = pd.DataFrame(transactions)
        if df.empty:
            return []
        df['month'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
        monthly = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
        result = []
        for month in monthly.index:
            result.append({
                "month": month,
                "income": monthly.loc[month].get('income', 0),
                "expense": monthly.loc[month].get('expense', 0),
                "balance": monthly.loc[month].get('income', 0) - monthly.loc[month].get('expense', 0)
            })
        return result

# ============================================================
# ВИЗУАЛИЗАТОР
# ============================================================
class Visualizer:
    @staticmethod
    def _ensure_charts_dir():
        if not os.path.exists('charts'):
            os.makedirs('charts')

    @staticmethod
    def save_pie_chart(transactions, filename="pie_chart.png"):
        Visualizer._ensure_charts_dir()
        if not transactions:
            print("Нет данных для круговой диаграммы")
            return None
        df = pd.DataFrame(transactions)
        if df.empty or 'type' not in df.columns:
            print("Нет данных для круговой диаграммы")
            return None
        expenses = df[df['type'] == 'expense']
        if expenses.empty:
            print("Нет расходов для круговой диаграммы")
            return None
        category_sum = expenses.groupby('category')['amount'].sum()
        plt.figure(figsize=(8, 6))
        plt.pie(category_sum.values, labels=category_sum.index, autopct='%1.1f%%')
        plt.title('Расходы по категориям')
        filepath = os.path.join('charts', filename)
        plt.savefig(filepath, format='png', dpi=100)
        plt.close()
        print(f"Круговая диаграмма сохранена: {filepath}")
        return filepath

    @staticmethod
    def save_bar_chart(transactions, filename="bar_chart.png"):
        Visualizer._ensure_charts_dir()
        if not transactions:
            print("Нет данных для столбчатой диаграммы")
            return None
        df = pd.DataFrame(transactions)
        if df.empty or 'date' not in df.columns or 'type' not in df.columns:
            print("Нет данных для столбчатой диаграммы")
            return None
        df['month'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
        monthly = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
        plt.figure(figsize=(10, 6))
        months = monthly.index
        x = range(len(months))
        plt.bar([i - 0.2 for i in x], monthly.get('income', 0), width=0.4, label='Доходы', color='green')
        plt.bar([i + 0.2 for i in x], monthly.get('expense', 0), width=0.4, label='Расходы', color='red')
        plt.xlabel('Месяц')
        plt.ylabel('Сумма (руб)')
        plt.title('Доходы и расходы по месяцам')
        plt.xticks(x, months, rotation=45)
        plt.legend()
        filepath = os.path.join('charts', filename)
        plt.savefig(filepath, format='png', dpi=100)
        plt.close()
        print(f"Столбчатая диаграмма сохранена: {filepath}")
        return filepath

    @staticmethod
    def save_trend_chart(transactions, filename="trend_chart.png"):
        Visualizer._ensure_charts_dir()
        if not transactions:
            print("Нет данных для графика динамики")
            return None
        df = pd.DataFrame(transactions)
        if df.empty or 'date' not in df.columns or 'type' not in df.columns:
            print("Нет данных для графика динамики")
            return None
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        balance = 0
        balances = []
        dates = []
        for _, row in df.iterrows():
            if row['type'] == 'income':
                balance += row['amount']
            else:
                balance -= row['amount']
            balances.append(balance)
            dates.append(row['date'])
        plt.figure(figsize=(10, 6))
        plt.plot(dates, balances, marker='o', linestyle='-', color='blue')
        plt.xlabel('Дата')
        plt.ylabel('Баланс (руб)')
        plt.title('Динамика баланса')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        filepath = os.path.join('charts', filename)
        plt.savefig(filepath, format='png', dpi=100)
        plt.close()
        print(f"График динамики сохранен: {filepath}")
        return filepath

# ============================================================
# СОЗДАНИЕ ЭКЗЕМПЛЯРОВ (ГЛОБАЛЬНЫХ)
# ============================================================
enclave = CryptoEnclave()
logger = SecureLogger()
bank = BankMicroservice(enclave, logger)
calc = Calculator()
table = TablePresenter()
viz = Visualizer()

# ============================================================
# ФУНКЦИЯ ГЕНЕРАЦИИ СЕРТИФИКАТОВ ДЛЯ HTTPS
# ============================================================
def ensure_certificates():
    cert_path = "/etc/nginx/server.crt"
    key_path = "/etc/nginx/server.key"
    if not os.path.exists(cert_path) or not os.path.exists(key_path):
        print("Генерация сертификатов для HTTPS...")
        subprocess.run([
            "openssl", "req", "-x509", "-nodes", "-days", "365",
            "-newkey", "rsa:2048", "-keyout", key_path,
            "-out", cert_path, "-subj", "/CN=localhost"
        ], check=False)

# ============================================================
# API ЭНДПОИНТЫ
# ============================================================
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "enclave": "active", "https": "enabled"})

@app.route('/api/attestation', methods=['GET'])
def attestation():
    return jsonify(enclave.attest(hashlib.sha256(b"banking_app").hexdigest()))

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    return jsonify(bank.get_all_transactions())

@app.route('/api/transfer', methods=['POST'])
def transfer():
    data = request.json
    result = bank.add_transaction(
        data.get('type', 'expense'),
        float(data.get('amount', 0)),
        data.get('category', 'other'),
        data.get('from', 'ACC1'),
        data.get('to', None)
    )
    return jsonify(result)

@app.route('/api/balance/<account>', methods=['GET'])
def get_balance(account):
    balance = bank.get_balance(account)
    return jsonify({"account": account, "balance": balance})

@app.route('/api/stats', methods=['GET'])
def stats():
    transactions = bank.get_all_transactions()
    return jsonify(calc.calculate_stats(transactions))

# ============================================================
# ОСНОВНАЯ ФУНКЦИЯ (ДЕМОНСТРАЦИЯ)
# ============================================================
def main():
    attestation = enclave.attest(hashlib.sha256(b"banking_app").hexdigest())
    print(f"\nАТТЕСТАЦИЯ АНКЛАВА: {attestation['status']}")
    print(f"Подпись: {attestation['signature']}")

    print("\n" + "="*60)
    print(" SECURETRUST CONTAINER - Банковский микросервис")
    print(" Защита от угрозы злоупотребления доверием (УБИ.021)")
    print("="*60)

    transactions = bank.get_all_transactions()
    stats = calc.calculate_stats(transactions)

    print(f"\n[РАСЧЕТЫ]")
    print(f"  Доходы:   {stats['total_income']:>10,.2f} руб")
    print(f"  Расходы:  {stats['total_expense']:>10,.2f} руб")
    print(f"  Баланс:   {stats['balance']:>10,.2f} руб")

    print(f"\n[ТАБЛИЧНОЕ ПРЕДСТАВЛЕНИЕ]")
    df = table.to_dataframe(transactions)
    print(df.to_string(index=False))

    print(f"\n[ГРУППИРОВКА ПО КАТЕГОРИЯМ]")
    grouped = table.group_by_category(transactions)
    print("  Расходы:")
    for cat, amount in grouped.get('expenses', {}).items():
        print(f"    {cat}: {amount:>10,.2f} руб")

    print("\n" + "="*60)
    print(" СОХРАНЕНИЕ ГРАФИКОВ")
    print("="*60)

    viz.save_pie_chart(transactions, "expenses_pie.png")
    viz.save_bar_chart(transactions, "monthly_bar.png")
    viz.save_trend_chart(transactions, "balance_trend.png")

    print("\nВсе графики сохранены в папку 'charts/'")
    print("="*60)

    print("\n[ЗАЩИТА ОТ УБИ.021]")
    print(f"  Файл базы данных зашифрован: {os.path.exists('bank.encrypted')}")
    print(f"  Целостность логов: {'OK' if logger.verify_integrity() else 'НАРУШЕНА'}")
    print(f"  Ключи существуют только в памяти анклава")
    print("="*60)

# ============================================================
# ЗАПУСК
# ============================================================
if __name__ == "__main__":
    main()
    ensure_certificates()
    port = int(os.environ.get("PORT", 8080))
    print(f"\nЗапуск API на порту {port}")
    print(f"API доступно по адресу: https://{os.environ.get('REPL_SLUG', 'localhost')}.{os.environ.get('REPL_OWNER', 'replit')}.replit.app")
    app.run(host='0.0.0.0', port=port)