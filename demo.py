import time,sys
username = sys.argv[0] # 变量测试
#password = sys.argv[2] # 登录密码
def main():
    localtime = time.asctime( time.localtime(time.time()) )
    print("Hello, GitHub Actions!")
    print("运行时间为：",localtime)
    print('账号：',username)
    #print('密码: ',password)
if __name__ == "__main__":
    main()
