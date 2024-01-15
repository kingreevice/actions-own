import time
def main():
    localtime = time.asctime( time.localtime(time.time()) )
    print("Hello, GitHub Actions!")
    print("运行时间为：",localtime)
if __name__ == "__main__":
    main()
