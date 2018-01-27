#!/bin/bash

# --------------------------------------------------------
# ---------------- BEGIN Parâmetros ----------------------
# --------------------------------------------------------

# IP do host em que servidor estará executando
host_ip="localhost"

# Porta em que servidor estará escutando
port=80

# Quantidade de threads do poll de threads do servidor web
# O teste de carga é feito sempre com o dobro de clientes em relação as
# threads do servidor
threads=(1 2 3 4 6 8 10 12 16 20 24 32 40)
# threads=(2 4)

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

# Aplicação python para teste de carga.
python_load_test_app=load_test.py

# --------------------------------------------------------
# ---------------- END Parâmetros ------------------------
# --------------------------------------------------------

echo "time,errors,qty_req,n_clients,nthreads,cap_queue,test_index" > $report_file
for i in $(seq 0 $((${#threads[@]}-1))); do
    for j in $(seq 0 $((${#cap_queue[@]}-1))); do
        cd dist
        echo "Executando o servidor ..."
        echo "sudo nohup java -jar multithreaded-web-server.jar -p $port -s ${threads[$i]} -c ${cap_queue[$j]} >> $log_file_server &"
        sudo nohup java -jar multithreaded-web-server.jar -p $port -s ${threads[$i]} -c ${cap_queue[$j]} >> $log_file_server &
        server_pid=$!
        cd ..
        echo "sleep 2"
        sleep 2
        echo "sleep 2 FIM"
        for k in $(seq 0 $((${#qty_req[@]}-1))); do
            for l in $(seq 0 $((qty_test-1))); do
                echo "python3 $python_load_test_app -o http://$host_ip -p $port -n ${qty_req[$k]} -c $((${threads[$i]})) -r $request_file >> $report_file"
                python3 $python_load_test_app -o http://$host_ip -p $port -n ${qty_req[$k]} -c $((${threads[$i]})) -r $request_file >> $report_file
                echo ",${threads[$i]},${cap_queue[$j]},$l" >> $report_file
            done
        done
        echo "Matando o servidor web ..."
        echo "sudo kill -9 $server_pid"
        sudo kill -9 $server_pid
        # Tentando matar de todo jeito possível
        process=$(ps aux | grep 'java -jar multithreaded-web-server.jar' | awk '{print $2}')
        arr_process=(`echo $process | cut -d " "  --output-delimiter=" " -f 1-`)
        while [[ ${#arr_process[@]} > 1 ]]; do
            echo "sudo kill -9 ${arr_process[0]}"
            sudo kill -9 ${arr_process[0]}
            sleep 1
            process=$(ps aux | grep 'java -jar multithreaded-web-server.jar' | awk '{print $2}')
            arr_process=(`echo $process | cut -d " "  --output-delimiter=" " -f 1-`)
        done
        echo "Servidor web finalizado."
        echo ""
        echo "-------------------------------------------------------------------------"
        echo ""
    done
done
