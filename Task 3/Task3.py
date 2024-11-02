import random
import string

def generate_password(length, use_lowercase=True, use_uppercase=True, use_digits=True, use_special=True):
    if length < 4:
        raise ValueError("Password length must be at least 4 characters")
    
    characters = ""
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not characters:
        raise ValueError("At least one character type must be selected")
    
    password = []
    
    if use_lowercase:
        password.append(random.choice(string.ascii_lowercase))
    if use_uppercase:
        password.append(random.choice(string.ascii_uppercase))
    if use_digits:
        password.append(random.choice(string.digits))
    if use_special:
        password.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
    
    while len(password) < length:
        password.append(random.choice(characters))
    
    random.shuffle(password)
    return ''.join(password)

def main():
    print("\n=== Password Generator ===")
    
    try:
        length = int(input("\nEnter desired password length: "))
        
        print("\nSelect character types to include:")
        lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
        uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
        digits = input("Include numbers? (y/n): ").lower() == 'y'
        special = input("Include special characters? (y/n): ").lower() == 'y'
        
        password = generate_password(
            length,
            use_lowercase=lowercase,
            use_uppercase=uppercase,
            use_digits=digits,
            use_special=special
        )
        
        print(f"\nGenerated Password: {password}")
        
        password_strength = len(set(password)) / len(password) * 100
        print(f"Password Strength: {password_strength:.1f}%")
        
    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()