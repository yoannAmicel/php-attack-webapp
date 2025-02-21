import random
import string
import os

PASSWORD_FILE = "passwords-v1.txt"
NUM_PASSWORDS = 10000

def generate_password():
    ''' Génère un mot de passe sécurisé de 12 caractères'''

    length = 12
    special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?/"

    # Format des mots de passes générés
    password = [
        random.choice(string.ascii_uppercase),  # 1 Majuscule
        random.choice(string.ascii_lowercase),  # 1 Minuscule
        random.choice(string.digits),           # 1 Chiffre
        random.choice(special_chars)            # 1 Caractère spécial
    ]

    # Générer le mot de passe sur la base de caractères aléatoires
    all_chars = string.ascii_letters + string.digits + special_chars
    password += random.choices(all_chars, k=length - len(password))
    random.shuffle(password)

    return ''.join(password)



# Charger les mots de passe existants pour éviter les doublons
existing_passwords = set()
if os.path.exists(PASSWORD_FILE):
    with open(PASSWORD_FILE, "r", encoding="utf-8") as f:
        existing_passwords.update(line.strip() for line in f)

# Générer et ajouter les nouveaux mots de passe
new_passwords = []
while len(new_passwords) < NUM_PASSWORDS:
    new_pass = generate_password()
    if new_pass not in existing_passwords:  # Vérifier qu'il n'est pas déjà dans le fichier
        new_passwords.append(new_pass)
        existing_passwords.add(new_pass)

# Ajouter les nouveaux mots de passe au fichier avec une ligne vide entre chaque liste générée
with open(PASSWORD_FILE, "a", encoding="utf-8") as f:
    f.write("\n")  # Ajoute une ligne vide pour séparer chaque batch
    f.write("\n".join(new_passwords) + "\n")

print(f"{len(new_passwords)} nouveaux mots de passe générés et ajoutés à {PASSWORD_FILE}")
