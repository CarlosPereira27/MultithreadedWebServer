package org.ufla.multithreadedwebserver;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.Executor;

/**
 * Responsável por escutar as requisições HTTP requisitadas neste servidor e
 * submetê-las para que um executor trate essas requisições.
 * 
 * @author andre
 * @author caio
 * @author carlos
 *
 */
public class MyHttpServer {

	/**
	 * Socket em que servidor web ficará escutando as requisições.
	 */
	private ServerSocket serverSocket;
	/**
	 * Responsável por executar as requisições HTTP submetidas
	 */
	private Executor executor;

	/**
	 * Constrói um servidor HTTP para escutar e tratar requisições HTTP.
	 * 
	 * @param port
	 *            porta em que o servidor irá escutar
	 * @param executor
	 *            responsável por executar as requisições HTTP submetidas
	 */
	public MyHttpServer(int port, Executor executor) {
		try {
			serverSocket = new ServerSocket(port);
			this.executor = executor;
		} catch (IOException e) {
			System.err.println("Não foi possível ouvir na: " + port);
			System.err.println(e.getMessage());
			System.exit(2);
		}
	}

	/**
	 * Inicia a execução do servidor.
	 */
	public void start() {
		while (true) {
			Socket clientSocket;
			try {
				clientSocket = serverSocket.accept();
				HttpSocketHandler httpHandler = new HttpSocketHandler(clientSocket);
				executor.execute(httpHandler);
			} catch (IOException e) {
				System.err.println("Conexão rejeitada.");
				System.err.println(e.getMessage());
			}
		}
	}

	/**
	 * Para a execução do servidor.
	 */
	public void stop() {
		try {
			serverSocket.close();
		} catch (IOException e) {
			System.err.println("Erro ao tentar parar servidor.");
			System.err.println(e.getMessage());
		}
	}

}
