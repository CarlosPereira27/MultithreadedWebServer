package org.ufla.multithreadedwebserver;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;

/**
 * Responsável por tratar requisições HTTP através da comunicação com o socket
 * do cliente que realizou a requisição. Apenas o método GET está implementado.
 * 
 * @author andre
 * @author caio
 * @author carlos
 *
 */
public class HttpSocketHandler implements Runnable {

	/**
	 * Socket do cliente que realizou a requisição HTTP
	 */
	private Socket clientSocket;

	/**
	 * Header de sucesso da requisição HTTP.
	 */
	private static final String SUCCESS_REQUEST_HEADER = "HTTP/1.0 200 OK\nContent-Type: text/html\n\n";
	/**
	 * Mensagem de recurso não encontrado da requisição HTTP (header e body).
	 */
	private static final String FILE_NOT_FOUND_MSG = "HTTP/1.0 404 Not Found\nContent-Type: "
			+ "text/html\n\n<HTML><HEAD><TITLE>Not Found</TITLE></HEAD><BODY>Not Found</BODY></HTML>";
	/**
	 * Mensagem de método não suportado da requisição HTTP (header e body).
	 */
	private static final String HTTP_METHOD_NOT_SUPPORTED_MSG = "HTTP/1.0 500 HTTP method not supported\n"
			+ "Content-Type: text/html\n\n<HTML><HEAD><TITLE>HTTP method not supported</TITLE>"
			+ "</HEAD><BODY>Multhreaded Web Server only support HTTP method GET</BODY></HTML>";


	private static final int BUFFER_SIZE_RESOURCE = 1 << 16; // 64KBytes

	/**
	 * Constrói um HttpSocketHandler para tratar a requisição realizada pelo
	 * parâmetro clientSocket
	 * 
	 * @param clientSocket
	 *            socket conectado ao cliente que fez uma requisição HTTP.
	 */
	public HttpSocketHandler(Socket clientSocket) {
		this.clientSocket = clientSocket;
	}

	/**
	 * Verifica através dos tokens da primeira linha da requisição HTTP se o método
	 * da requisição é o GET.
	 * 
	 * @param tokens
	 *            tokens da primeira linha da requisição HTTP
	 * @return true, se o método da requisição HTTP é o GET, caso contrário, false
	 */
	private boolean isGetCommand(String tokens[]) {
		return tokens[0].equals("GET") && tokens[tokens.length - 1].equals("HTTP/1.1");
	}

	/**
	 * Extraí o identificador do recurso solicitado através dos tokens da primeira
	 * linha da requisição HTTP.
	 * 
	 * @param tokens
	 *            tokens da primeira linha da requisição HTTP
	 * @return nome do recurso solicitado
	 */
	private String extractResourceFromGet(String tokens[]) {
		StringBuilder resource = new StringBuilder();
		for (int i = 1; i < tokens.length - 2; i++) {
			resource.append(tokens[i]).append(' ');
		}
		resource.append(tokens[tokens.length - 2]);
		return resource.toString();
	}

	/**
	 * Realiza o tratamento da requisição HTTP realizada pelo clientSocket
	 */
	public void run() {
		BufferedWriter out = null;
		BufferedReader in = null;
		try {
			out = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()), BUFFER_SIZE_RESOURCE);
			in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
			String command = in.readLine();
			if (command == null) {
				throw new IOException("null line");
			}
			String tokens[] = command.split(" ");
			if (isGetCommand(tokens)) {
				String resource = extractResourceFromGet(tokens);
				if (ServerConfiguration.onLog()) {
					System.out.println("Thread '" + Thread.currentThread().getName() + "' tratando a requisição '"
							+ resource + "'");
				}
				File file = new File(MultithreadedWebServer.rootDirectory + resource);
				if (file.exists() && file.isFile()) {
					char cbuf[] = new char[BUFFER_SIZE_RESOURCE - 1];
					BufferedReader resourceReader = new BufferedReader(new FileReader(file), BUFFER_SIZE_RESOURCE);
					clientSocket.setSendBufferSize((int) (SUCCESS_REQUEST_HEADER.length() + file.length()));
					out.write(SUCCESS_REQUEST_HEADER.toCharArray());
					while (resourceReader.read(cbuf) != -1) {
						out.write(cbuf);
					}
					resourceReader.close();
				} else {
					clientSocket.setSendBufferSize(FILE_NOT_FOUND_MSG.length());
					out.write(FILE_NOT_FOUND_MSG.toCharArray());
				}
			} else {
				clientSocket.setSendBufferSize(HTTP_METHOD_NOT_SUPPORTED_MSG.length());
				out.write(HTTP_METHOD_NOT_SUPPORTED_MSG.toCharArray());
			}
		} catch (IOException e) {
			// System.err.println("Erro de E/S no socket.");
			// System.err.println(e.getMessage());
		} finally {
			try {
				out.flush();
				out.close();
				in.close();
				clientSocket.close();
			} catch (IOException e) {
				System.err.println("Erro em fechar o socket.");
				System.err.println(e.getMessage());
			}

		}
	}
	

}
