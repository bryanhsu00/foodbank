import os,sys
#os.system("ps aux | grep uwsgi | awk '{print $2}' | xargs | awk '{print $1}' | xargs kill -9")
#os.system("ps aux | grep uwsgi")
# os.system("kill -9 "+sys.stdin.readline())
os.system("killall -9 uwsgi")
os.system("killall -9 python3")
print("Server stopped")