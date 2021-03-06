package org.ufla.multithreadedwebserver;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.util.concurrent.Executor;

import org.ufla.multithreadedwebserver.concurrent.MyThreadPoolExecutor;

import com.sun.net.httpserver.HttpServer;

/**
 *
 * Responsável por configurar e inicializar o servidor web.
 * 
 * @author andre
 * @author caio
 * @author carlos
 *
 */
public class MultithreadedWebServer {

	/**
	 * Diretório raiz em que o servidor web irá buscar os recursos, diretório em que
	 * a aplicação está rodando.
	 */
	public static String rootDirectory = System.getProperty("user.dir");

	/**
	 * Realiza a configuração e inicialização do servidor multithread.
	 * 
	 * @param args
	 * 
	 * @throws Exception
	 */
	public static void main(String[] args) throws Exception {
		try {
			ArgsHandler.applyConfigurations(args);
		} catch (Exception e) {
			System.err.println(e.getMessage());
			System.out.println();
			ArgsHandler.showHelpMessage();
			System.exit(2);
		}
		createMyHttpServer();
	}

	/**
	 * Inicializa o servidor HTTP implementado neste projeto.
	 * 
	 * @throws IOException
	 */
	private static void createMyHttpServer() throws IOException {
		ServerConfiguration serverConfiguration = ServerConfiguration.getInstance();
		Executor executor = new MyThreadPoolExecutor(serverConfiguration.getPoolSize(),
				serverConfiguration.getCapacityQueue());
		MyHttpServer server = new MyHttpServer(serverConfiguration.getPortListener(), executor);
		startLog();
		server.start();
	}

	/**
	 * Inicializa um servidor HTTP implementado pela Sun.
	 * 
	 * @throws IOException
	 */
	@SuppressWarnings("unused")
	private static void createSunHttpServer() throws IOException {
		ServerConfiguration serverConfiguration = ServerConfiguration.getInstance();
		HttpServer server = HttpServer.create(new InetSocketAddress(serverConfiguration.getPortListener()), 1);
		Executor executor = new MyThreadPoolExecutor(serverConfiguration.getPoolSize(),
				serverConfiguration.getCapacityQueue());
		server.createContext("/", new MyHttpHandler());
		server.setExecutor(executor);
		server.start();
		startLog();
	}

	/**
	 * Realiza um log inicial definindo as configurações do servidor web.
	 */
	private static void startLog() {
		ServerConfiguration serverConfiguration = ServerConfiguration.getInstance();
		System.out.printf(
				"Servidor web executando na porta %d.\nPool de threads de tamanho %d.\n"
						+ "Fila de tarefas com a capacidade máxima de %d tarefas.\n"
						+ "Diretório raiz para busca de recursos é '%s'\n",
				serverConfiguration.getPortListener(), serverConfiguration.getPoolSize(),
				serverConfiguration.getCapacityQueue(), rootDirectory);
	}

}
