import secrets
import string


def get_password_length():
    while True:
        try:
            length = int(input("Enter desired password length (8-64): "))
            if length < 8:
                print("Too short. Minimum is 8 characters.")
            elif length > 64:
                print("Too long. Maximum is 64 characters.")
            else:
                return length
        except ValueError:
            print("Please enter a valid whole number.")


def build_character_pool():
    return string.ascii_letters + string.digits


def generate_password(length):
    pool = build_character_pool()
    password_chars = [secrets.choice(pool) for _ in range(length)]
    return ''.join(password_chars)


def main():
    print("=== DecodeLabs Secure Password Generator ===")
    length = get_password_length()
    password = generate_password(length)
    print(f"\nYour secure password: {password}")


if __name__ == "__main__":
    main()
