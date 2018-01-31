#!/bin/bash

# --------------------------------------------------------
# ---------------- BEGIN Parâmetros ----------------------
# --------------------------------------------------------

# IP do host em que servidor estará executando
host_ip="35.196.147.187"

# Porta em que servidor estará escutando
port=80

# Usuário que entrará no servidor via ssh
user_ssh="carlos"

# Caminho ssh chave privada
ssh_private_key="~/.ssh/gcloud_ppd"

# Usuário que instalou o servidor web em seu diretório
user_server="carloshpereira27"

# Quantidade de threads do poll de threads do servidor web
# O teste de carga é feito sempre com o dobro de clientes em relação as
# threads do servidor
threads=(1 2 3 4 6 8 10 12 16 20 24 32 40)

# Quantidade de vezes que serão realizadas as request da base de dados
# de teste
qty_req=(100)

# Capacidade da fila de tarefas do servidor web
cap_queue=(1000)

# Quantidade de vezes que executará cada cenário de teste
qty_test=10

# Nome do arquivo, onde o relatório será escrito
report_file="report.csv"

# Nome do arquivo que contém as informações sobre as requisições
request_file="dist/resources_request.txt"

# Nome do arquivo que armazenará o log do servidor
log_file_server="web_server.log"

# Quantos clientes que serão simulados no script que realiza as requisições
clients=8

# Nome do script gerado para ligar o servidor web
turn_on_server_script="turn_on_server.sh"

# Aplicação python para teste de carga.
python_load_test_app=load_test.py

# --------------------------------------------------------
# ---------------- END Parâmetros ------------------------
# --------------------------------------------------------



echo "time,errors,qty_req,n_clients,nthreads,cap_queue,test_index" > $report_file
for i in $(seq 0 $((${#threads[@]}-1))); do
    for j in $(seq 0 $((${#cap_queue[@]}-1))); do
	    echo "./writer_turn_on_server.sh $port ${threads[$i]} ${cap_queue[$j]} $log_file_server $user_server $turn_on_server_script"
        ./writer_turn_on_server.sh $port ${threads[$i]} ${cap_queue[$j]} $log_file_server $user_server $turn_on_server_script
        echo "ssh -i $ssh_private_key $user_ssh@$host_ip 'bash -s' < $turn_on_server_script"
	    ssh -i $ssh_private_key $user_ssh@$host_ip 'bash -s' < $turn_on_server_script
        sleep 2
        for k in $(seq 0 $((${#qty_req[@]}-1))); do
            for l in $(seq 0 $((qty_test-1))); do
                echo "python3 $python_load_test_app -o http://$host_ip -p $port -n ${qty_req[$k]} -c $clients -r $request_file >> $report_file"
                python3 $python_load_test_app -o http://$host_ip -p $port -n ${qty_req[$k]} -c $clients -r $request_file >> $report_file
                echo ",${threads[$i]},${cap_queue[$j]},$l" >> $report_file
            done
        done
	    echo "ssh -i $ssh_private_key $user_ssh@$host_ip 'bash -s' < turn_off_server.sh"
        ssh -i $ssh_private_key $user_ssh@$host_ip 'bash -s' < turn_off_server.sh
        echo "Servidor web finalizado."
        echo ""
        echo "-------------------------------------------------------------------------"
        echo ""
    done
done
