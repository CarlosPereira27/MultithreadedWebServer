import urllib.request
import os.path
import sys, getopt
import time
import threading

class Configuration:

    def __init__(self):
        self.requests = []
        self.host = "http://localhost"
        self.port = 8008
        self.qty_request = 1
        self.num_clients = 1
        self.leftover_request = 0

    def getURL(self):
        return "%s:%d" % (self.host, self.port)

    def getQtyRequests(self):
        return self.qty_request * self.num_clients + self.leftover_request

class ThreadClient (threading.Thread):

    def __init__(self, configuration, index, errors):
        threading.Thread.__init__(self)
        self.configuration = configuration
        self.index = index
        self.errors = errors

    def runRequests(self):
        url = self.configuration.getURL()
        for request in self.configuration.requests:
            try:
                html = urllib.request.urlopen(url + "/" + request).read()
            except Exception:
                self.errors[self.index] += 1

    def run(self):
        for i in range(self.configuration.qty_request):
            self.runRequests()
            


def showHelpMessage():
    print ('Realiza teste de carga em um determinado servidor web.')
    print ('python loadTest.py -r <request_file> -o <host> -p <port> -n <qty_each_request> -c <num_clients>')
    print ('')
    print ('Opções:')
    print ('-r --request_file=REQUEST_FILE           Arquivo com a lista de recursos a ser requisitado ao servidor web')
    print ('-o --host=HOST                           Host do servidor web. Padrão: http://localhost')
    print ('-p --port=PORT                           Porta em que o servidor web está ouvindo. Padrão: 8008')
    print ('-n --qty_each_request=QTY_EACH_REQUEST   Quantidade de requisições para cada recurso. Padrão: 1')
    print ('-c --num_clients=NUM_CLIENTS             Quantidade de clientes fazendo requisições. Padrão: 1')

def validIntegerPositive(attrName, value):
    valueInt = 0;
    try:
        valueInt = int(value)
        if valueInt < 0:
            print("%s deve ser um " + "número inteiro positivo (valor associado = %s)." % (attrName, value))
            sys.exit(2)
    except ValueError:
        print("%s deve ser um " + "número inteiro positivo (valor associado = %s)." % (attrName, value))
        sys.exit(2)
    return valueInt

def defineConfiguration(argv, configuration):
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

def testConfiguration(configuration):
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

def runRequests(configuration, errorInd, errors):
    url = configuration.getURL()
    for request in configuration.requests:
        try:
            urllib.request.urlopen(url + "/" + request)
        except Exception:
            self.errors[errorInd] += 1

def defineQtyRequest(configuration):
    configuration.leftover_request = configuration.qty_request % configuration.num_clients
    configuration.qty_request = configuration.qty_request // configuration.num_clients

def main(argv):
    configuration = Configuration()
    defineConfiguration(argv, configuration)
    defineQtyRequest(configuration)
    testConfiguration(configuration)
    clients = []
    errors = [ 0 * configuration.num_clients ]
    startTime = time.time() 
    for i in range(configuration.num_clients - 1):
        clients.append(ThreadClient(configuration, i + 1, errors))
        clients[i].start()

    for i in range(configuration.qty_request + configuration.leftover_request):
        runRequests(configuration, 0, errors)

    for i in range(configuration.num_clients - 1):
        clients[i].join()
    timeTotal = int((time.time() - startTime) * 1000000)
    print ("%ld,%d,%d,%d" % (timeTotal, sum(errors), configuration.getQtyRequests(), configuration.num_clients), end='')
    # print ("Demorou %f milissegundos para fazer %d vez(es) as requisições com %d clientes" % ((time.time() - startTime) * 1000, configuration.qty_request, configuration.num_clients))
    # print ("%d erros em requisições." % (sum(errors)))

if __name__ == "__main__":
    main(sys.argv[1:])
