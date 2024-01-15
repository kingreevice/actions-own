import sys,os
def main():
    print("Number of arguments:", len(sys.argv))
    print("Arguments:", sys.argv)
    if len(sys.argv) != 3:
        print("Usage: python demo.py <username> <password>")
        sys.exit(1)

    # Get the username and password from command line arguments
    username = sys.argv[1]
    password = sys.argv[2]
    #获取finde_value.yml提取的变量
    appID = os.environ.get("APP_ID")
    print(f'appid:{appID}')

    # Output the provided username and password
    print(f"Username: {username}")
    print(f"Password: {password}")
if __name__ == "__main__":
    main()
