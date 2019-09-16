#!/usr/bin/sh

urlencodepipe() {
    local LANG=C; local c; while IFS= read -r c; do
        case $c in [a-zA-Z0-9.~_-]) printf "$c"; continue ;; esac
        printf "$c" | od -An -tx1 | tr ' ' % | tr -d '\n'
    done <<EOF
$(fold -w1)
EOF
    echo
}

urlencode() { 
    printf "$*" | urlencodepipe ;
} 

uid=ws030
pwd=123456
jybh=062834
msg=$1

echo $msg 
exit

encoded_msg=`urlencode $msg`
curl -s -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "uid=$uid&pwd=$pwd&jybh=$jybh&smscontent=$encoded_msg" \
    http://10.36.11.166/webservice.asmx/sendsms 
