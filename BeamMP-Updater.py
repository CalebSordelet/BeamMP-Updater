import pefile
import sys
import os
import requests
import shutil
import win32com.client

GITHUB_REPO = "https://api.github.com/repos/BeamMP/BeamMP-Launcher/releases"
LAUNCHER_FILENAME = "BeamMP-Launcher.exe"
APPDATA = os.getenv('APPDATA')
BEAMMP_LAUNCHER_DIR = os.path.join(APPDATA, 'BeamMP-Launcher')
BEAMMP_LAUNCHER = os.path.join(BEAMMP_LAUNCHER_DIR, LAUNCHER_FILENAME)
SHORTCUT_PATH = os.path.join(APPDATA, 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'BeamMP-Updater.lnk')

def create_exe_shortcut(target_path, shortcut_path, description=""):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)

    shortcut.Targetpath = target_path
    shortcut.WorkingDirectory = os.path.dirname(target_path)
    shortcut.Description = description

    shortcut.save()

def get_launcher_version():
    try:
        pe = pefile.PE(BEAMMP_LAUNCHER)
        version_info = pe.VS_FIXEDFILEINFO[0]
        major = (version_info.FileVersionMS >> 16) & 0xFFFF
        minor = version_info.FileVersionMS & 0xFFFF
        patch = (version_info.FileVersionLS >> 16) & 0xFFFF
        pe.close()
        return f"v{major}.{minor}.{patch}"
    except Exception as e:
        print(f"Error retrieving installed version: {e}")
        return None
    
def get_latest_version():
    try:
        response = requests.get(f"{GITHUB_REPO}/latest", timeout=10).json()
        latest_version = response['tag_name']
        return latest_version
    except Exception as e:
        print(f"Error retrieving latest version: {e}")
        return None
    
def download_latest_version(latest_version_tag, filename, output_location):
    try:
        url = f"{GITHUB_REPO}/tags/{latest_version_tag}"
        response = requests.get(url, timeout=10).json()
        asset = next((a for a in response["assets"] if a["name"] == filename), None)
        if not asset:
            raise ValueError(f"Asset '{filename}' not found in release '{latest_version_tag}'")
        download_url = asset["browser_download_url"]
        print(f"Downloading from {download_url}...")
        if os.path.exists(output_location):
            os.remove(output_location)
        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(output_location, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded latest version '{latest_version_tag}' to '{output_location}'")
    except Exception as e:
        print(f"Error downloading latest version: {e}")

if __name__ == "__main__":
    if not os.path.exists(BEAMMP_LAUNCHER):
        print("BeamMP Launcher is not installed.")
        input("Press Enter to exit...")
        exit(1)

    if not os.path.exists(SHORTCUT_PATH):
        print("Would you like to install BeamMP Updater and create a Start Menu shortcut? (y/n)")
        choice = input().strip().lower()
        if choice == 'y':
            print("Installing BeamMP Updater...")
            if getattr(sys, 'frozen', False):
                application_path = os.path.abspath(sys.executable)
            else:
                application_path = os.path.abspath(__file__)
            installed_path = os.path.join(BEAMMP_LAUNCHER_DIR, application_path.split(os.sep)[-1])
            shutil.copy(application_path, installed_path)

            print("Creating Start Menu shortcut...")
            if installed_path.split('.')[-1] == 'exe':
                create_exe_shortcut(installed_path, SHORTCUT_PATH, "BeamMP Updater")
            else:
                print("Shortcut creation unavailable in python script mode.")
        else:
            print("Installation and shortcut creation skipped.")

    current_version = get_launcher_version()
    latest_version = get_latest_version()

    print("Current BeamMP Launcher Version:", current_version)
    print("Latest BeamMP Launcher Version:", latest_version)

    if current_version != latest_version:
        print("An update is available!")
        download_latest_version(latest_version, LAUNCHER_FILENAME, BEAMMP_LAUNCHER)
        if get_launcher_version() == latest_version:
            print("Update successful!")
        else:
            print("Update failed.")
    else:
        print("You are using the latest version.")

    input("Press Enter to exit...")
