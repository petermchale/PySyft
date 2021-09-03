#!/bin/bash
chsum1=""

while [[ true ]]
do
    chsum2=`find packages/ -name "*.py" -type f -exec md5 {} \;`
    if [[ $chsum1 != $chsum2 ]] ; then
        pre-commit run --all-files
        chsum1=$chsum2
    fi
    sleep 120
done

