print("welcome new user, please enter your name and age: ")
username = input("Name: ")
user_age = input("Age: ")

user_secrets = input(f"Tell me a secret {username}... ")
print_secret = input("Would you like me to repeat your secret back to you?: (Y/N)")
new_user_info = (username, user_age, user_secrets)

try:
    if print_secret == "Y" or print_secret == "y":
        print(print_secret)

    else:
        print ("your secret is safe with me")
except TypeError:
    print("Please enter a valid input (Y/N): ")
