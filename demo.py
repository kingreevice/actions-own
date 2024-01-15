# demo.py

import sys

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python demo.py <username> <password>")
        sys.exit(1)

    # Get the username and password from command line arguments
    username = sys.argv[1]
    password = sys.argv[2]

    # Output the provided username and password
    print(f"Username: {username}")
    print(f"Password: {password}")

if __name__ == "__main__":
    main()
