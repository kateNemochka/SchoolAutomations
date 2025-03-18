import os
import shutil
import subprocess

# 🚫 1. Блокування Roblox
def block_roblox():
    print("🔹 Видалення Roblox...")
    paths = [
        r"C:\Users\%USERNAME%\AppData\Local\Roblox",
        r"C:\Program Files (x86)\Roblox",
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Roblox"
    ]
    for path in paths:
        path = os.path.expandvars(path)
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
            print(f"✅ Видалено: {path}")
        else:
            print(f"❌ Не знайдено: {path}")

    print("🔹 Блокування запуску Roblox через реєстр...")
    try:
        subprocess.run(
            r'reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun" '
            r'/v Roblox /t REG_SZ /d "RobloxPlayerBeta.exe" /f',
            shell=True, check=True
        )
        subprocess.run(
            r'reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun" '
            r'/v RobloxStudio /t REG_SZ /d "RobloxStudioBeta.exe" /f',
            shell=True, check=True
        )
        print("✅ Roblox заблоковано через реєстр.")
    except subprocess.CalledProcessError:
        print("❌ Не вдалося заблокувати Roblox у реєстрі.")

# 🌐 2. Блокування сайтів онлайн-ігор через hosts
def block_game_sites():
    print("🔹 Блокування сайтів онлайн-ігор...")
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    blocked_sites = [
        "roblox.com", "www.roblox.com",
        "y8.com", "www.y8.com",
        "friv.com", "www.friv.com",
        "crazygames.com", "www.crazygames.com",
        "poki.com", "www.poki.com"
    ]

    try:
        with open(hosts_path, "a") as hosts_file:
            for site in blocked_sites:
                hosts_file.write(f"\n127.0.0.1 {site}")
        print("✅ Сайти онлайн-ігор заблоковано.")
    except PermissionError:
        print("❌ Помилка: запустіть скрипт від імені адміністратора!")

# 🔐 3. Увімкнення контролю UAC
def enable_uac():
    print("🔹 Увімкнення максимального рівня UAC...")
    try:
        subprocess.run(
            r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" '
            r'/v ConsentPromptBehaviorUser /t REG_DWORD /d 3 /f',
            shell=True, check=True
        )
        print("✅ UAC встановлено на максимальний рівень (Always notify).")
    except subprocess.CalledProcessError:
        print("❌ Не вдалося змінити налаштування UAC.")

if __name__ == "__main__":
    if os.name == "nt":  # Windows only
        block_roblox()
        block_game_sites()
        enable_uac()
        print("\n✅ Налаштування завершено. Перезавантажте комп'ютер для застосування змін.")
    else:
        print("❌ Цей скрипт працює тільки на Windows.")
