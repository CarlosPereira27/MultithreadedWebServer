#!/bin/bash

# Tentando matar de todo jeito possível
echo "Matando o servidor web ..."
process=$(ps aux | grep 'java -jar multithreaded-web-server.jar' | awk '{print $2}')
arr_process=(`echo $process | cut -d " "  --output-delimiter=" " -f 1-`)
while [[ ${#arr_process[@]} > 1 ]]; do
    echo "sudo kill -9 ${arr_process[0]}"
    sudo kill -9 ${arr_process[0]}
    sleep 1
    process=$(ps aux | grep 'java -jar multithreaded-web-server.jar' | awk '{print $2}')
    arr_process=(`echo $process | cut -d " "  --output-delimiter=" " -f 1-`)
done
