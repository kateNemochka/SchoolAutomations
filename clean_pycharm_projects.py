import os
import shutil
import subprocess

# 🧹 1. Очищення PyCharmProjects
def clean_pycharm_projects():
    current_user = os.environ.get('USERNAME')
    projects_path = rf"C:\Users\{current_user}\PycharmProjects"

    if os.path.exists(projects_path):
        for item in os.listdir(projects_path):
            item_path = os.path.join(projects_path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                print(f"✅ Видалено: {item_path}")
            except Exception as e:
                print(f"❌ Помилка видалення {item_path}: {e}")
    else:
        print("ℹ️ Папка відсутня, очищення не потрібне.")

# 🕒 2. Налаштування Task Scheduler для щоденного виконання
def schedule_task():
    print("🔹 Створення завдання в Task Scheduler для щоденного очищення PyCharm...")
    task_name = "Clean_PyCharm_Projects"
    script_path = os.path.abspath(__file__)

    try:
        subprocess.run(
            f'schtasks /create /tn "{task_name}" /tr "python {script_path}" /sc daily /st 07:00 /f',
            shell=True, check=True
        )
        print(f"✅ Завдання '{task_name}' створено, скрипт буде виконуватись щоденно о 07:00.")
    except subprocess.CalledProcessError:
        print("❌ Помилка створення завдання. Спробуйте запустити скрипт від імені адміністратора.")

if __name__ == "__main__":
    clean_pycharm_projects()
    schedule_task()
