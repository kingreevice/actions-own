import time
username = sys.argv[1] # 变量测试
def main():
    localtime = time.asctime( time.localtime(time.time()) )
    print("Hello, GitHub Actions!")
    print("运行时间为：",localtime)
    print('密码：',username)
if __name__ == "__main__":
    main()
