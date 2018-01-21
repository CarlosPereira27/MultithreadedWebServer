# Quantidade de threads do poll de threads do servidor web
# O teste de carga é feito sempre com o dobro de clientes em relação as
# threads do servidor
threads=(1 2 3 4 6 8 10 12 16 20 24 28 32 40 48 56 64 72 80 88 96)
# threads=(1 2 4)

# Quantidade de números de threads testados
qty_threads_cen=21
# qty_threads_cen=3

# Quantidade de vezes que serão realizadas as request da base de dados
# de teste
qty_req=(10 50 100)

# Quantidade de requisições diferentes testadas
qty_req_cen=3

# Capacidade da fila de tarefas do servidor web
cap_queue=(20 100 1000)

# Quantidade de capacidade de fila diferente testadas
qty_queue_cen=3

# Quantidade de vezes que executará cada cenário de teste
# qty_test=10
qty_test=1

# Nome do arquivo, onde o relatório será escrito
report_file="report.csv"

# Nome do arquivo que contém as informações sobre as requisições
request_file="dist/resources_request.txt"

# Nome do arquivo que armazenará o log do servidor
log_file_server="web_server.log"

echo "time,errors,qty_req,n_clients,nthreads,cap_queue,test_index" > $report_file
for i in $(seq 0 $((qty_threads_cen-1))); do
    for j in $(seq 0 $((qty_queue_cen-1))); do
        cd dist
        echo "Executando o servidor ..."
        echo "nohup java -jar multithreaded-web-server.jar -s ${threads[$i]} -c ${cap_queue[$j]}  >> $log_file_server &"
        nohup java -jar multithreaded-web-server.jar -s ${threads[$i]} -c ${cap_queue[$j]}  >> $log_file_server &
        server_pid=$!
        cd ..
        sleep 2
        for k in $(seq 0 $((qty_req_cen-1))); do
            for l in $(seq 0 $((qty_test-1))); do
                echo "python3 loadTest.py -n ${qty_req[$k]} -c $((${threads[$i]}*2)) -r $request_file >> $report_file"
                python3 loadTest.py -n ${qty_req[$k]} -c $((${threads[$i]}*2)) -r $request_file >> $report_file
                echo ",${cap_queue[$j]},$l" >> $report_file
            done
        done
        echo "kill -9 $server_pid"
        kill -9 $server_pid
        # Tentando matar de todo jeito possível
        process=$(ps aux | grep 'java -jar multithreaded-web-server.jar' | awk '{print $2}')
        arr_process=(`echo $process | cut -d " "  --output-delimiter=" " -f 1-`)
        while [[ ${#arr_process[@]} > 1 ]]; do
            echo "kill ${arr_process[0]}"
            kill -9 ${arr_process[0]}
            sleep 1
            process=$(ps aux | grep 'java -jar multithreaded-web-server.jar' | awk '{print $2}')
            arr_process=(`echo $process | cut -d " "  --output-delimiter=" " -f 1-`)
        done
        echo "-------------------------------------------------------------------------"
    done
done