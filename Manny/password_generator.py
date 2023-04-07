import random
import string

def generate_password():
    lowercase = random.choice(string.ascii_lowercase)
    uppercase = random.choice(string.ascii_uppercase)
    number = random.choice(string.digits)
    symbol = random.choice(string.punctuation)

    remaining_chars = 6
    remaining_random_chars = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=remaining_chars))

    password = lowercase + uppercase + number + symbol + remaining_random_chars
    password = ''.join(random.sample(password, len(password)))

    return password

generated_password = generate_password()
print(generated_password)

