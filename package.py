def check_package(nom_package):
    if check_installed(nom_package):
        print(f"Le package {nom_package} est déjà installé.")
    else:
        install_package(nom_package)
        

def check_installed(package_name):
    import pkg_resources
    installed_packages = [pkg.key for pkg in pkg_resources.working_set]
    return package_name.lower() in installed_packages

def install_package(nom_package):
    import subprocess
    import sys
    print(f"Installation de {nom_package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", nom_package])
    print(f"{nom_package} a été installé avec succès.")

# Use the function to check and install psutil and upgrade pip if necessary
check_package("psutil")
import psutil

def close_existing_chromedrivers():
    # Trouver tous les processus chromedriver en cours d'exécution
    chromedriver_processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'chromedriver':
            chromedriver_processes.append(proc)

    # Terminer tous les processus chromedriver en cours d'exécution
    for proc in chromedriver_processes:
        proc.terminate()

def terminate_existing_chrome_processes():
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if 'chrome.exe' in proc.info['name']:
                #print(f"Terminating Chrome process with PID {proc.info['pid']}")
                psutil.Process(proc.info['pid']).terminate()
        # Fermer toutes les autres instances WebDriver déjà lancées
        close_existing_chromedrivers()
        #print("Existing Chrome processes terminated.")
    except Exception as e:
        print(f"Error terminating Chrome processes: {e}")

