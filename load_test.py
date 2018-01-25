import urllib.request
import os.path
import sys, getopt
import time
import threading
import multiprocessing

class Configuration:
    """
    Represent a configuração de um teste de carga.
    """

    def __init__(self):
        self.requests = []
        self.host = "http://localhost"
        self.port = 8008
        self.qty_request = 1
        self.num_clients = 1
        self.leftover_request = 0

    def getURL(self):
        """
        Recupera a URL completa do host a ser requisitado (URL e porta da aplicação)
        """
        return "%s:%d" % (self.host, self.port)

    def getQtyRequests(self):
        """
        Recupera a quantidade total de request que será realizada, incluindo todos
        clientes emulados.
        """
        return self.qty_request * self.num_clients + self.leftover_request

class ThreadClient (threading.Thread):
    """
    Representa um cliente na hora dos testes de carga.
    """

    def __init__(self, configuration, index, errors):
        """
        Construtor de um cliente de teste de carga

        @param configuration : Configuration
            configuração do teste de carga a ser realizado
        @param index : int
            índice da thread cliente e que marcará os erros ocorridos na 
            lista de erros
        @param errors : list<int>
            lista de quantidade de erros ocorridos
        """
        threading.Thread.__init__(self)
        self.configuration = configuration
        self.index = index
        self.errors = errors

    def runRequests(self):
        """
        Executa as requisições dos recursos definidos no arquivo de recursos
        da configuração.
        """
        url = self.configuration.getURL()
        for request in self.configuration.requests:
            try:
                html = urllib.request.urlopen(url + "/" + request).read()
            except Exception:
                self.errors[self.index] += 1

    def run(self):
        """
        Executa todas requisições desse cliente. São as requisições dos recursos 
        definidos no arquivo de recursos da configuração multiplicado pela 
        self.configuration.qty_request.
        """
        for i in range(self.configuration.qty_request):
            self.runRequests()
            


def showHelpMessage():
    """
    Mostra a mensagem de ajuda para o usuário
    """
    print ('Realiza teste de carga em um determinado servidor web.')
    print ('python loadTest.py -r <request_file> -o <host> -p <port> -n <qty_each_request> -c <num_clients>')
    print ('')
    print ('Opções:')
    print ('-r --request_file=REQUEST_FILE           Arquivo com a lista de recursos a ser requisitado ao servidor web')
    print ('-o --host=HOST                           Host do servidor web. Padrão: http://localhost')
    print ('-p --port=PORT                           Porta em que o servidor web está ouvindo. Padrão: 8008')
    print ('-n --qty_each_request=QTY_EACH_REQUEST   Quantidade de requisições para cada recurso. Padrão: 1')
    print ('-c --num_clients=NUM_CLIENTS             Quantidade de clientes fazendo requisições. Padrão: 1')

def validIntegerPositive(attr_name, value):
    """
    Válida se o valor de um atributo é um inteiro positivo.
    Se é inteiro positivo retorna o valor, caso contrário encerra a aplicação com erro.

    @param attr_name : str
        nome do atributo a ser validado
    @param value : str:
        valor do atributo em string

    @return
        se o valor é um inteiro positivo retorna o valor, caso contrário encerra a 
        aplicação com erro
    """
    value_int = 0;
    try:
        value_int = int(value)
        if value_int < 0:
            print("%s deve ser um " + "número inteiro positivo (valor associado = %s)." % (attr_name, value))
            sys.exit(2)
    except ValueError:
        print("%s deve ser um " + "número inteiro positivo (valor associado = %s)." % (attr_name, value))
        sys.exit(2)
    return value_int

def defineConfiguration(argv, configuration):
    """
    Define a configuração do teste de carga a partir dos argumentos da aplicação.

    @param argv : list<str>
        lista de argumentos da aplicação
    @param configuration : Configuration
        configuração do teste de carga a ser realizado
    """
    try:
        opts, args = getopt.getopt(argv,"hr:o:p:n:c:",["request_file=", "host=", "port=", "qty_each_request=", "num_clients="])
    except getopt.GetoptError:
        print (getopt.GetoptError.message)
        showHelpMessage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            showHelpMessage()
            sys.exit()
        elif opt in ("-r", "--request_file"):
            if (not os.path.isfile(arg)):
                print ('ERRO! O arquivo de requisições %s não existe.!' % arg)
                sys.exit(2)
            fp = open(arg, 'r')
            for line in fp:
                configuration.requests.append(line);
        elif opt in ("-o", "--host"):
            configuration.host = arg
        elif opt in ("-p", "--port"):
            configuration.port = validIntegerPositive('port', arg)
        elif opt in ("-n", "--qty_each_request"):
            configuration.qty_request = validIntegerPositive('qty_each_request', arg)
        elif opt in ("-c", "--num_clients"):
            configuration.num_clients = validIntegerPositive('num_clients', arg)
            if configuration.num_clients > multiprocessing.cpu_count():
                 configuration.num_clients = multiprocessing.cpu_count()

def testConfiguration(configuration):
    """
    Testa se uma configuração de teste de carga é válida.
    Se não é válida encerra a aplicação.

    @param configuration : Configuration
        configuração do teste de carga a ser realizado
    """
    if not configuration.requests:
        print ('ERRO! Arquivo de requisições não contém nenhum recurso a ser requisitado!')
        sys.exit(2)
    try:
        urllib.request.urlopen(configuration.getURL())
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print ('ERRO! %s' % str(e))
            sys.exit(2)
    except Exception as e:
        print ('ERRO! %s' % str(e))
        sys.exit(2)

def runRequests(configuration, error_ind, errors):
    """
    Executa as request da thread principal.

    @param configuration : Configuration
        configuração do teste de carga a ser realizado
    @param error_ind : int
        índice que marcará os erros ocorridos na lista de erros
    @param errors : list<int>
        lista de quantidade de erros ocorridos
    """
    url = configuration.getURL()
    for request in configuration.requests:
        try:
            urllib.request.urlopen(url + "/" + request)
        except Exception:
            self.errors[error_ind] += 1

def defineQtyRequest(configuration):
    """
    Calcula a quantidade de requisição que cada thread deverá fazer da base
    de dados, com base na quantidade de vezes que o usuário quer realizar de
    requisições na base e na quantidade de usuário que pretende emular.

    @param configuration : Configuration
        configuração do teste de carga a ser realizado
    """
    configuration.leftover_request = configuration.qty_request % configuration.num_clients
    configuration.qty_request = configuration.qty_request // configuration.num_clients

def main(argv):
    configuration = Configuration()
    defineConfiguration(argv, configuration)
    defineQtyRequest(configuration)
    testConfiguration(configuration)
    clients = []
    errors = [ 0 * configuration.num_clients ]
    start_time = time.time() 
    for i in range(configuration.num_clients - 1):
        clients.append(ThreadClient(configuration, i + 1, errors))
        clients[i].start()

    for i in range(configuration.qty_request + configuration.leftover_request):
        runRequests(configuration, 0, errors)

    for i in range(configuration.num_clients - 1):
        clients[i].join()
    time_total = int((time.time() - start_time) * 1000000)
    print ("%ld,%d,%d,%d" % (time_total, sum(errors), configuration.getQtyRequests(), configuration.num_clients), end='')
    # print ("Demorou %f milissegundos para fazer %d vez(es) as requisições com %d clientes" % ((time.time() - startTime) * 1000, configuration.qty_request, configuration.num_clients))
    # print ("%d erros em requisições." % (sum(errors)))

if __name__ == "__main__":
    main(sys.argv[1:])
