#!/bin/bash

# --------------------------------------------------------
# ---------------- BEGIN Parâmetros ----------------------
# --------------------------------------------------------

# Porta em que servidor web deverá ser executado
port=$1

# Quantidade de threads do poll de threads do servidor web
threads=$2

# Capacidade da fila de tarefas do servidor web
cap_queue=$3

# Nome do arquivo que armazenará o log do servidor
log_file_server=$4

# Usuário que instalou o servidor web em seu diretório
user_server=$5

# Nome do arquivo onde será escrito o script para ligar o servidor web
turn_on_server=$6

# --------------------------------------------------------
# ---------------- END Parâmetros ----------------------
# --------------------------------------------------------



echo "Escrevendo script para ligar o servidor '$turn_on_server'"

echo "#!/bin/bash" > $turn_on_server
echo "" >> $turn_on_server
echo 'echo "Executando o servidor ..."' >> $turn_on_server
echo "" >> $turn_on_server
echo "sudo su - $user_server" >> $turn_on_server
echo "cd MultithreadedWebServer/dist" >> $turn_on_server
echo "echo \"nohup java -jar multithreaded-web-server.jar -p $port -s $threads -c $cap_queue >> $log_file_server &\"" >> $turn_on_server
echo "sudo nohup java -jar multithreaded-web-server.jar -p $port -s $threads -c $cap_queue >> $log_file_server &" >> $turn_on_server

sudo chmod +x $turn_on_server
