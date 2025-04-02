import os
import shutil
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


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    log("🚀 Старт з __main__")

    if not is_admin():
        log("🔐 Немає прав адміністратора. Перезапускаємо...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{__file__}"', None, 1
        )
        sys.exit()

    log("▶ Запуск скрипта")
    clean_pycharm_projects()
    delete_roblox_files()
    log("✅ Очищення завершено\n")
