"""
Ручное приёмочное тестирование контейнера SecureTrust Container
Выполняется в интерактивном режиме оператором
"""

import os
import json
import hashlib

from main import CryptoEnclave, SecureLogger, BankMicroservice, Calculator, TablePresenter, Visualizer

print("=" * 70)
print(" РУЧНОЕ ПРИЁМОЧНОЕ ТЕСТИРОВАНИЕ")
print(" SecureTrust Container - Защита от угрозы УБИ.021")
print("=" * 70)

results = {}

# ============================================================
# ТЕСТ 1: АТТЕСТАЦИЯ АНКЛАВА
# ============================================================
print("\n[ТЕСТ 1] АТТЕСТАЦИЯ АНКЛАВА")
enclave = CryptoEnclave()
attest = enclave.attest(hashlib.sha256(b"banking_app").hexdigest())
print(f"  Статус: {attest['status']}")
print(f"  Подпись: {attest['signature'][:32]}...")
if attest['status'] == 'trusted' and attest['signature']:
    results["1. Аттестация анклава"] = "ПРОЙДЕН"
    print("  РЕЗУЛЬТАТ: Аттестация пройдена")
else:
    results["1. Аттестация анклава"] = "НЕ ПРОЙДЕН"
    print("  РЕЗУЛЬТАТ: Аттестация не пройдена")

# ============================================================
# ТЕСТ 2: РАСЧЁТ СТАТИСТИКИ
# ============================================================
print("\n[ТЕСТ 2] РАСЧЁТ СТАТИСТИКИ")
logger = SecureLogger()
bank = BankMicroservice(enclave, logger)
calc = Calculator()

transactions = bank.get_all_transactions()
stats = calc.calculate_stats(transactions)

print(f"  Доходы:   {stats['total_income']:>10,.2f} руб")
print(f"  Расходы:  {stats['total_expense']:>10,.2f} руб")
print(f"  Баланс:   {stats['balance']:>10,.2f} руб")

expected_income = 1000 + 1500 + 2000 + 800
expected_expense = 200 + 50 + 100 + 300 + 150 + 250 + 500 + 300

if stats['total_income'] == expected_income and stats['total_expense'] == expected_expense:
    results["2. Расчёт статистики"] = "ПРОЙДЕН"
    print("  РЕЗУЛЬТАТ: Расчёты корректны")
else:
    results["2. Расчёт статистики"] = "НЕ ПРОЙДЕН"
    print("  РЕЗУЛЬТАТ: Расчёты некорректны")

# ============================================================
# ТЕСТ 3: ТАБЛИЧНОЕ ПРЕДСТАВЛЕНИЕ
# ============================================================
print("\n[ТЕСТ 3] ТАБЛИЧНОЕ ПРЕДСТАВЛЕНИЕ")
presenter = TablePresenter()
df = presenter.to_dataframe(transactions)
print(f"  Количество транзакций: {len(df)}")
print(f"  Колонки: {list(df.columns)}")

grouped = presenter.group_by_category(transactions)
if grouped.get('expenses') or grouped.get('incomes'):
    results["3. Табличное представление"] = "ПРОЙДЕН"
    print("  РЕЗУЛЬТАТ: Таблицы и группировка работают")
else:
    results["3. Табличное представление"] = "НЕ ПРОЙДЕН"
    print("  РЕЗУЛЬТАТ: Ошибка в табличном представлении")

# ============================================================
# ТЕСТ 4: СОХРАНЕНИЕ ГРАФИКОВ
# ============================================================
print("\n[ТЕСТ 4] СОХРАНЕНИЕ ГРАФИКОВ")
viz = Visualizer()

pie_file = viz.save_pie_chart(transactions, "manual_pie.png")
bar_file = viz.save_bar_chart(transactions, "manual_bar.png")
trend_file = viz.save_trend_chart(transactions, "manual_trend.png")

charts_ok = True
if pie_file and os.path.exists(pie_file):
    print("  Круговая диаграмма сохранена")
else:
    print("   Круговая диаграмма НЕ сохранена")
    charts_ok = False

if bar_file and os.path.exists(bar_file):
    print("  Столбчатая диаграмма сохранена")
else:
    print("   Столбчатая диаграмма НЕ сохранена")
    charts_ok = False

if trend_file and os.path.exists(trend_file):
    print("  График динамики сохранён")
else:
    print("  График динамики НЕ сохранён")
    charts_ok = False

results["4. Сохранение графиков"] = "ПРОЙДЕН" if charts_ok else "НЕ ПРОЙДЕН"

# ============================================================
# ТЕСТ 5: ЗАЩИТА ОТ УБИ.021 (шифрование данных)
# ============================================================
print("\n[ТЕСТ 5] ЗАЩИТА ОТ УБИ.021 - ШИФРОВАНИЕ ДАННЫХ")

if os.path.exists("bank.encrypted"):
    with open("bank.encrypted", "r") as f:
        content = f.read()

    if '"transactions"' not in content:
        print("   Файл bank.encrypted зашифрован (не читается как обычный текст)")
        results["5. Шифрование данных"] = "ПРОЙДЕН"
    else:
        print("   Файл bank.encrypted не зашифрован")
        results["5. Шифрование данных"] = "НЕ ПРОЙДЕН"
else:
    print("  Файл bank.encrypted не найден")
    results["5. Шифрование данных"] = "НЕ ПРОЙДЕН"

# ============================================================
# ТЕСТ 6: ЗАЩИТА ОТ УБИ.021 (расшифровка чужим ключом)
# ============================================================
print("\n[ТЕСТ 6] ЗАЩИТА ОТ УБИ.021 - РАСШИФРОВКА ЧУЖИМ КЛЮЧОМ")
try:
    new_enclave = CryptoEnclave()

    with open("bank.encrypted", "rb") as f:
        encrypted_data = json.loads(f.read().decode())

    # Преобразуем hex-строки обратно в байты
    encrypted_bytes = {
        "salt": bytes.fromhex(encrypted_data["salt"]),
        "ciphertext": bytes.fromhex(encrypted_data["ciphertext"])
    }

    decrypted = new_enclave.decrypt_data(encrypted_bytes)
    try:
        json.loads(decrypted.decode())
        decoded_success = True
    except:
        decoded_success = False

    if not decoded_success:
        print("  Расшифровка чужим ключом невозможна (данные защищены)")
        results["6. Расшифровка чужим ключом"] = "ПРОЙДЕН"
    else:
        print("  Данные удалось расшифровать чужим ключом!")
        results["6. Расшифровка чужим ключом"] = "НЕ ПРОЙДЕН"
except Exception as e:
    print(f"  ОШИБКА: {e}")
    results["6. Расшифровка чужим ключом"] = "НЕ ПРОЙДЕН"
# ============================================================
# ТЕСТ 7: ЦЕЛОСТНОСТЬ ЛОГОВ
# ============================================================
print("\n[ТЕСТ 7] ЦЕЛОСТНОСТЬ ЛОГОВ")
try:
    # Создаём новый логгер для чистого теста
    if os.path.exists("secure_audit.log"):
        os.remove("secure_audit.log")

    logger_test = SecureLogger()
    logger_test.log("MANUAL_TEST", "Тестовое сообщение")

    if logger_test.verify_integrity():
        print("  Лог не повреждён, целостность подтверждена")

        with open("secure_audit.log", "a") as f:
            f.write("fake_entry|SIG:fake_signature\n")

        if not logger_test.verify_integrity():
            print("  Подделка лога обнаружена")
            results["7. Целостность логов"] = "ПРОЙДЕН"
        else:
            print("  Подделка лога НЕ обнаружена!")
            results["7. Целостность логов"] = "НЕ ПРОЙДЕН"
    else:
        print("  Целостность лога нарушена (без подделки)!")
        results["7. Целостность логов"] = "НЕ ПРОЙДЕН"
except Exception as e:
    print(f"  ОШИБКА: {e}")
    results["7. Целостность логов"] = "НЕ ПРОЙДЕН"
# ============================================================
# ИТОГОВЫЙ ОТЧЁТ
# ============================================================
print("\n" + "=" * 70)
print(" ИТОГОВЫЙ ОТЧЁТ РУЧНОГО ПРИЁМОЧНОГО ТЕСТИРОВАНИЯ")
print("=" * 70)

all_passed = True
for test_name, status in results.items():
    symbol = "OK" if status == "ПРОЙДЕН" else "NO"
    print(f"  {symbol} {test_name}: {status}")
    if status != "ПРОЙДЕН":
        all_passed = False

print("-" * 70)

if all_passed:
    print(" РЕЗУЛЬТАТ: КОНТЕЙНЕР ПРИНЯТ В ЭКСПЛУАТАЦИЮ")
    print(" Все проверки ручного приёмочного тестирования пройдены успешно.")
else:
    print(" РЕЗУЛЬТАТ: КОНТЕЙНЕР НЕ ПРИНЯТ")
    print(" Требуется устранение выявленных дефектов.")

print("=" * 70)