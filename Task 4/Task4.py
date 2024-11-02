import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_rules():
    print("\n=== ROCK PAPER SCISSORS ===")
    print("\nRules:")
    print("🪨  Rock crushes Scissors")
    print("📄  Paper covers Rock")
    print("✂️   Scissors cuts Paper")
    print("\nType 'q' to quit anytime")

def get_user_choice():
    while True:
        print("\nMake your choice:")
        print("1. Rock 🪨")
        print("2. Paper 📄")
        print("3. Scissors ✂️")
        
        choice = input("\nEnter your choice (1-3): ").lower()
        
        if choice == 'q':
            return 'quit'
        
        if choice in ['1', '2', '3']:
            return ['rock', 'paper', 'scissors'][int(choice) - 1]
        
        print("\n❌ Invalid choice! Please try again.")

def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return 'tie'
    
    winning_combinations = {
        'rock': 'scissors',
        'paper': 'rock',
        'scissors': 'paper'
    }
    
    return 'user' if winning_combinations[user_choice] == computer_choice else 'computer'

def display_choices(user_choice, computer_choice):
    symbols = {
        'rock': '🪨',
        'paper': '📄',
        'scissors': '✂️'
    }
    
    print(f"\nYour choice: {user_choice.title()} {symbols[user_choice]}")
    print("Computer thinking", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print(f"\nComputer's choice: {computer_choice.title()} {symbols[computer_choice]}")

def display_result(result):
    messages = {
        'user': '🎉 You win! 🎉',
        'computer': '😔 Computer wins!',
        'tie': '🤝 It\'s a tie!'
    }
    print(f"\n{messages[result]}")

def display_score(user_score, computer_score):
    print("\n=== SCORE ===")
    print(f"You: {user_score}")
    print(f"Computer: {computer_score}")

def play_again():
    while True:
        choice = input("\nPlay again? (y/n): ").lower()
        if choice in ['y', 'n']:
            return choice == 'y'
        print("Please enter 'y' or 'n'")

def main():
    user_score = 0
    computer_score = 0
    rounds_played = 0
    
    while True:
        clear_screen()
        display_rules()
        
        if rounds_played > 0:
            display_score(user_score, computer_score)
        
        user_choice = get_user_choice()
        if user_choice == 'quit':
            break
        
        computer_choice = get_computer_choice()
        display_choices(user_choice, computer_choice)
        
        result = determine_winner(user_choice, computer_choice)
        display_result(result)
        
        if result == 'user':
            user_score += 1
        elif result == 'computer':
            computer_score += 1
        
        rounds_played += 1
        
        if not play_again():
            break
    
    if rounds_played > 0:
        print("\n=== FINAL SCORE ===")
        display_score(user_score, computer_score)
        
        if user_score > computer_score:
            print("\n🏆 Congratulations! You're the overall winner! 🏆")
        elif computer_score > user_score:
            print("\n🤖 Computer is the overall winner!")
        else:
            print("\n🤝 The game ends in a tie!")
        
        print(f"\nThanks for playing! You played {rounds_played} rounds.")

if __name__ == "__main__":
    main()