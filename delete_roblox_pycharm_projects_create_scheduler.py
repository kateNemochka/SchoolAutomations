import os
import sys
import ctypes
import subprocess
import shutil
from datetime import datetime, timedelta


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"❌ Помилка перевірки прав адміністратора: {e}")
        return False


def log(message):
    try:
        log_dir = r"C:\Logs"
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "clean_log.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        print(f"❌ Не вдалося записати лог: {e}")


def clean_pycharm_projects():
    home_dir = os.path.expanduser("~")
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


def delete_roblox_files():
    log("🧹 Пошук і видалення 'Roblox' файлів/папок...")
    paths_to_check = [
        os.path.expanduser("~"),
        os.path.join(os.environ.get("APPDATA", ""), "Local"),
        os.environ.get("PROGRAMDATA", ""),
        os.path.join("C:\\", "Program Files"),
        os.path.join("C:\\", "Program Files (x86)")
    ]

    for base_path in paths_to_check:
        if not base_path or not os.path.exists(base_path):
            continue

        for root, dirs, files in os.walk(base_path, topdown=True):
            # Виключаємо системні папки
            dirs[:] = [d for d in dirs if "windows" not in d.lower() and "microsoft" not in d.lower()]
            for dir_name in dirs:
                if "roblox" in dir_name.lower():
                    full_path = os.path.join(root, dir_name)
                    try:
                        shutil.rmtree(full_path)
                        log(f"✅ Видалено папку: {full_path}")
                    except Exception as e:
                        log(f"❌ Помилка видалення папки {full_path}: {e}")

            for file_name in files:
                if "roblox" in file_name.lower():
                    full_path = os.path.join(root, file_name)
                    try:
                        os.remove(full_path)
                        log(f"✅ Видалено файл: {full_path}")
                    except Exception as e:
                        log(f"❌ Помилка видалення файлу {full_path}: {e}")


def create_cmd_launcher():
    """
    Створює CMD-файл, який запускає цей скрипт з прапорцем --delete-only.
    При запуску через Планувальник буде виконуватись лише видалення.
    """
    script_path = os.path.abspath(__file__)
    python_path = sys.executable
    cmd_path = os.path.join(os.path.dirname(script_path), "run_clean.cmd")
    content = f'@echo off\n"{python_path}" "{script_path}" --delete-only\n'
    try:
        with open(cmd_path, "w", encoding="utf-8") as f:
            f.write(content)
        log(f"⚙️ Створено CMD-лаунчер: {cmd_path}")
    except Exception as e:
        log(f"❌ Помилка створення CMD-файлу: {e}")
    return cmd_path


def create_scheduler_task_with_xml(cmd_path):
    """
    Створює завдання в Планувальнику через XML, яке:
    - Виконується щопонеділка та щовівторка о 08:30.
    - Має опцію "Запустити одразу, якщо було пропущено час виконання".
    """
    task_name = "MyCleanupTask"
    now = datetime.now()

    # Обчислюємо наступний запуск: якщо зараз після 08:30 у понеділок чи вівторок, переносимо на наступний.
    # Знаходимо наступний день, який є понеділком або вівторком.
    # Для простоти встановимо StartBoundary на найближчий понеділок.
    weekday = now.weekday()  # Monday = 0, Tuesday = 1, ..., Sunday = 6
    days_until_monday = (0 - weekday) % 7
    if days_until_monday == 0 and (now.hour > 8 or (now.hour == 8 and now.minute >= 30)):
        days_until_monday = 7
    next_start = now + timedelta(days=days_until_monday)
    start_boundary = next_start.replace(hour=8, minute=30, second=0, microsecond=0).isoformat()

    xml_content = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>{datetime.now().isoformat()}</Date>
    <Author>{os.getlogin()}</Author>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>{start_boundary}</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByWeek>
        <WeeksInterval>1</WeeksInterval>
        <DaysOfWeek>
          <Monday/>
          <Tuesday/>
        </DaysOfWeek>
      </ScheduleByWeek>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{cmd_path}</Command>
    </Exec>
  </Actions>
</Task>
'''
    xml_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_task.xml")
    try:
        with open(xml_file, "w", encoding="utf-16") as f:
            f.write(xml_content)
        schtasks_command = f'schtasks /Create /TN "{task_name}" /XML "{xml_file}" /F'
        subprocess.run(schtasks_command, shell=True, check=True)
        log(f"⚙️ Завдання '{task_name}' створено з XML: {xml_file}")
    except Exception as e:
        log(f"❌ Помилка створення завдання через XML: {e}")
    finally:
        try:
            os.remove(xml_file)
        except Exception as e:
            log(f"❌ Не вдалося видалити тимчасовий XML: {e}")


def perform_deletions():
    clean_pycharm_projects()
    delete_roblox_files()


if __name__ == "__main__":
    # Зміна робочої теки на директорію скрипта
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    log("🚀 Старт скрипта")

    # Якщо запускаємо з прапорцем --delete-only, виконуємо лише видалення
    if "--delete-only" in sys.argv:
        log("▶ Запуск у режимі тільки видалення (без створення Scheduler та CMD)")
        perform_deletions()
    else:
        log("▶ Запуск у звичайному режимі (створення Scheduler, CMD, а потім видалення)")
        if not is_admin():
            log("🔐 Немає прав адміністратора. Перезапускаємо скрипт з підвищенням прав...")
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{os.path.abspath(__file__)}"', None, 1
            )
            sys.exit()

        # Створення CMD-файлу для запуску скрипта в режимі --delete-only
        cmd_launcher_path = create_cmd_launcher()
        # Створення завдання в Планувальнику через XML із налаштуваннями:
        # - Щопонеділка та щовівторка о 08:30.
        # - Запустити одразу, якщо було пропущено час виконання.
        create_scheduler_task_with_xml(cmd_launcher_path)
        # Виконання операцій видалення
        perform_deletions()
