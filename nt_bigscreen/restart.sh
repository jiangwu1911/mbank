ps -ef|grep ntserver.py | grep -v grep | awk '{print $2}' | xargs kill -9
nohup python ntserver.py &
