import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_tiktok_page_exists(username):
    url = f"https://www.tiktok.com/@{username}"
    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 200:
            return username, True
        elif response.status_code == 404:
            return username, False
        else:
            return username, False  
    except requests.RequestException as e:
        print(f"Erreur de réseau pour l'utilisateur @{username}: {e}")
        return username, False

def read_usernames_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            usernames = [line.strip() for line in file.readlines()]
        return usernames
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé")
        return []

def write_hits_to_file(hits, file_path):
    with open(file_path, 'w') as file:
        for hit in hits:
            file.write(hit + '\n')

def main():
    usernames = read_usernames_from_file('username.txt')
    hits = []

    if usernames:  # Check if there are any usernames to process
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(check_tiktok_page_exists, username) for username in usernames]

            for future in as_completed(futures):
                username, page_exists = future.result()
                if page_exists:
                    print(f"Ce nom '@{username}' existe.")
                    hits.append(username)
                else:
                    print(f"Ce nom '@{username}' n'existe pas")

        write_hits_to_file(hits, 'hits.txt')

if __name__ == "__main__":
    main()
