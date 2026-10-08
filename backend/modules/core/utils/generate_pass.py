import random, string

def generate_password(max_length=16):
    r = [random.randint(2, max_length//4) for _ in range(4)]
    random_chars = random.choices(
        string.ascii_uppercase, k=r[0]) + random.choices(
            string.punctuation.replace('$',''), k=r[1]) + random.choices(
                string.ascii_lowercase, k=r[2]) + random.choices(
                    string.digits, k=r[3])
    random.shuffle(random_chars)
    return ''.join(random_chars)
