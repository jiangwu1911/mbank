ps -ef|grep ntserver.py | grep -v grep | awk '{print $2}' | xargs kill -9
git pull
nohup python ntserver.py &
