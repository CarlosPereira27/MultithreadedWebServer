#!/bin/bash

echo "Executando o servidor ..."

sudo su - carloshpereira27
cd MultithreadedWebServer/dist
echo "nohup java -jar multithreaded-web-server.jar -p 80 -s 10 -c 1000 >> web_server.log &"
sudo nohup java -jar multithreaded-web-server.jar -p 80 -s 10 -c 1000 >> web_server.log &
