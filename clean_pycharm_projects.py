import os
import shutil
import subprocess
import sys
import ctypes
from datetime import datetime


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"❌ Помилка перевірки прав адміністратора: {e}")
        return False


def log(message):
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clean_log.txt")
    with open(log_path, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")


def clean_pycharm_projects():
    home_dir = os.path.expanduser('~')
    projects_path = os.path.join(home_dir, 'PycharmProjects')

    log(f"🔍 Перевірка теки: {projects_path}")

    if os.path.exists(projects_path):
        for item in os.listdir(projects_path):
            item_path = os.path.join(projects_path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                log(f"✅ Видалено: {item_path}")
            except Exception as e:
                log(f"❌ Помилка видалення {item_path}: {e}")
    else:
        log("ℹ️ Папка відсутня, очищення не потрібне.")


def create_cmd_launcher():
    script_path = os.path.abspath(__file__)
    python_path = sys.executable
    cmd_path = os.path.join(os.path.dirname(script_path), "run_clean.cmd")

    content = f'@echo off\n"{python_path}" "{script_path}"\n'
    with open(cmd_path, "w", encoding="utf-8") as f:
        f.write(content)

    log(f"⚙️ Створено run_clean.cmd: {cmd_path}")
    return cmd_path


def schedule_task():
    print("🔹 Створення завдання в Task Scheduler для очищення PyCharmProjects щопонеділка і щовівторка о 08:30...")
    task_name = "Clean_PyCharm_Projects"
    cmd_path = create_cmd_launcher()

    # Видаляємо старе завдання (ігноруємо помилки)
    subprocess.run(f'schtasks /delete /tn "{task_name}" /f', shell=True)

    user = os.getlogin()
    powershell_command = f'''
$Action = New-ScheduledTaskAction -Execute "{cmd_path}"
$Trigger1 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 08:30AM
$Trigger2 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Tuesday -At 08:30AM
$Principal = New-ScheduledTaskPrincipal -UserId "{user}" -LogonType S4U -RunLevel Highest
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "{task_name}" -Action $Action -Trigger $Trigger1,$Trigger2 -Principal $Principal -Settings $Settings -Force
'''

    try:
        subprocess.run(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", powershell_command],
            check=True
        )
        print(f"✅ Завдання '{task_name}' створено з розкладом: понеділок і вівторок о 08:30.")
        log(f"✅ Створено завдання з розкладом (Пн, Вт 08:30) і правами адміністратора.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Помилка створення завдання через PowerShell: {e}")
        log(f"❌ Помилка створення завдання через PowerShell: {e}")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if not is_admin():
        print("Немає прав адміністратора. Перезапускаємо скрипт з підвищеними правами...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{__file__}"', None, 1
        )
        sys.exit()

    log("▶ Запуск скрипта")
    clean_pycharm_projects()
    schedule_task()
