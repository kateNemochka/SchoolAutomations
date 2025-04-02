# 🧹 clean_pycharm.py — Скрипт для очищення PyCharm та Roblox

## 📌 Що робить скрипт?

1. Видаляє все з папки `PycharmProjects` поточного користувача.
2. Видаляє всі файли та папки, що містять `Roblox` у назві, у типових локаціях.
3. Створює `run_clean.cmd` — для запуску вручну або через Task Scheduler.
4. Логує всі дії у `C:\Logs\clean_log.txt`.

---

## 🗂 Структура логів

- Логи зберігаються у `C:\Logs\clean_log.txt`
- Формат:
  ```
  [2025-04-02 08:30:00] ✅ Видалено: C:\Users\Name\PycharmProjects\test
  ```

---

## ⚙ Як встановити

1. Збережіть файл `clean_pycharm.py` у зручну директорію (наприклад: `C:\Users\Name\CleanPyCharm\`).
2. Запустіть скрипт — він:
   - запустить себе з правами адміністратора,
   - видалить непотрібні файли,
   - створить `run_clean.cmd`.

---

## 🗓 Додавання в Task Scheduler (ручне)

1. Відкрий Task Scheduler (`Win + R → taskschd.msc`)
2. Створи нове завдання:
   - **Name:** `Clean_PyCharm_Projects`
   - **Run with highest privileges:** ✅
   - **Trigger:** Weekly → Monday, Tuesday → 08:30 AM
   - **Action:**
     - **Program:** `cmd.exe`
     - **Arguments:**
       ```
       /c "C:\Users\Name\CleanPyCharm\run_clean.cmd"
       ```
     - **Start in:** `C:\Users\Name\CleanPyCharm`

---

## 🔐 Вимоги

- Права адміністратора.
- Встановлений Python.
- Скрипт сам піднімає привілеї при потребі (`ShellExecuteW → runas`).

---

## 🔄 Оновлення run_clean.cmd

- Кожен запуск створює актуальний `run_clean.cmd`.

---

## ✅ Безпечне використання

Видаляються лише файли/папки, що містять `roblox` у назві з локацій:

- `C:\Users\...`
- `C:\Program Files`
- `C:\Program Files (x86)`
- `C:\ProgramData`
- `AppData\Local`

---

## 📄 Автор

Автоматизовано за допомогою Python ✨
