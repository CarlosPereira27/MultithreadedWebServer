package org.ufla.multithreadedwebserver;

/**
 * Responsável por tratar os argumentos da aplicação e realizar a configuração
 * do servidor.
 * 
 * @author andre
 * @author caio
 * @author carlos
 *
 */
public class ArgsHandler {

	private static final String PORT_ID = "Porta em que o servidor está ouvindo (-p | --port)";
	private static final String PORT_PREFIX = "--port=";
	private static final String PORT_PREFIX_SIMPLE = "-p";

	private static final String CAPACITY_QUEUE_ID = "Capacidade máxima da fila de tarefas (-c | --queue_capacity=)";
	private static final String CAPACITY_QUEUE = "--queue_capacity=";
	private static final String CAPACITY_QUEUE_SIMPLE = "-c";

	private static final String POOL_SIZE_ID = "Tamanho do pool de threads (-s | --poll_size)";
	private static final String POOL_SIZE = "--poll_size=";
	private static final String POOL_SIZE_SIMPLE = "-s";
	
	private static final String LOG= "--log";
	private static final String LOG_SIMPLE = "-l";

	private static final String HELP = "--help";
	private static final String HELP_SIMPLE = "-h";
	private static final String HELP_MESSAGE = "Ajuda\n\n" + "Opções:\n"
			+ "-p --port=PORT                Porta em que o servidor está ouvindo\n"
			+ "-c --queue_capacity=CAPACITY  Capacidade máxima da fila de tarefas\n"
			+ "-s --poll_size=SIZE           Tamanho do pool de threads\n"
			+ "-l --log                      Ativa o log das requisições\n"
			+ "-h --help                     Imprime mensagem de ajuda\n";
	
	/**
	 * Mostra a mensagem de ajuda.
	 */
	public static void showHelpMessage() {
		System.out.println(HELP_MESSAGE);
	}

	/**
	 * Realiza a validação do valor de um determinado atributo que deve ser inteiro
	 * e positivo.
	 * 
	 * @param attr
	 *            atributo a ser validado
	 * @param value
	 *            valor do atributo a ser validado
	 * @return valor do atributo
	 * @throws Exception
	 *             exceção é lançada caso o valor não seja um inteiro positivo
	 */
	private static int validIntegerPositive(String attr, String value) throws Exception {
		int valueInt = 0;
		try {
			valueInt = Integer.parseInt(value);
			if (valueInt < 0) {
				throw new Exception();
			}
		} catch (Exception e) {
			throw new Exception(
					String.format("%s deve ser um " + "número inteiro positivo (valor associado = %s).", attr, value));
		}
		return valueInt;
	}

	/**
	 * Recupera uma string de um determinado índice de um array, retornando uma
	 * string default para caso a exceção OutOfBounds seja lançada.
	 * 
	 * @param i
	 *            índice do array
	 * @param args
	 *            array de strings
	 * @param defaultOutOfBounds
	 *            valor default a ser retornado caso índice não seja válido
	 * @return
	 */
	private static String valueHandleOutOfBounds(int i, String args[], String defaultOutOfBounds) {
		try {
			return args[i];
		} catch (Exception e) {
			return defaultOutOfBounds;
		}
	}

	/**
	 * Usando os argumentos da aplicação realiza a configuração do servidor.
	 * 
	 * @param args
	 *            argumentos da aplicação
	 * @throws Exception
	 *             caso tenha algum problema nos argumentos, essa exceção será
	 *             lançada
	 */
	public static void applyConfigurations(String[] args) throws Exception {
		ServerConfiguration configuration = ServerConfiguration.getInstance();
		for (int i = 0; i < args.length; i++) {
			if (args[i].equals(HELP) || args[i].equals(HELP_SIMPLE)) {
				System.out.println(HELP_MESSAGE);
				System.exit(0);
			} else if (args[i].equals(PORT_PREFIX_SIMPLE)) {
				configuration.setPortListener(validIntegerPositive(PORT_ID, valueHandleOutOfBounds(i + 1, args, "")));
				i++;
			} else if (args[i].startsWith(PORT_PREFIX)) {
				configuration.setPortListener(validIntegerPositive(PORT_ID, args[i].substring(PORT_PREFIX.length())));
			} else if (args[i].equals(CAPACITY_QUEUE_SIMPLE)) {
				configuration.setCapacityQueue(
						validIntegerPositive(CAPACITY_QUEUE_ID, valueHandleOutOfBounds(i + 1, args, "")));
				i++;
			} else if (args[i].startsWith(CAPACITY_QUEUE)) {
				configuration.setCapacityQueue(
						validIntegerPositive(CAPACITY_QUEUE_ID, args[i].substring(CAPACITY_QUEUE.length())));
			} else if (args[i].startsWith(POOL_SIZE_SIMPLE)) {
				configuration.setPoolSize(validIntegerPositive(POOL_SIZE_ID, valueHandleOutOfBounds(i + 1, args, "")));
				i++;
			} else if (args[i].equals(POOL_SIZE)) {
				configuration
						.setPoolSize(validIntegerPositive(CAPACITY_QUEUE_ID, args[i].substring(POOL_SIZE.length())));
			} else if (args[i].equals(LOG)) {
				configuration.setLog(true);
			} else if (args[i].equals(LOG_SIMPLE)) {
				configuration.setLog(true);
			} else if (args[i].startsWith("-")) {
				throw new Exception(String.format("Opção não reconhecida '%s'", args[i]));
			}
		}

	}

}
