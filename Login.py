def load_secret(path="./secret.txt"):
    with open(path, 'r') as f:
        username = f.readline().strip()
        password = f.readline().strip()
    return username, password