#curl -X POST -d '[{ "headers" :{"a" : "a1","b" : "b1"},"body" : "idoall.org_body"}]' http://localhost:8080

#curl --request POST --data-binary "@httpserver.py"  http://localhost:8080
#curl --request POST --data-binary "@2.bin"  http://localhost:8080

for ((i=0; i<10; i++)); do
    curl --request POST --data-binary "@bottle.pyc"  http://localhost:8080 &
done
