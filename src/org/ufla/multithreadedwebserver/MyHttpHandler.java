package org.ufla.multithreadedwebserver;

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

/**
 * Responsável por tratar requisições HTTP do servidor web, entregando os
 * recursos requisitados ao cliente.
 *
 * @author andre
 * @author caio
 * @author carlos
 *
 */
public class MyHttpHandler implements HttpHandler {

	@SuppressWarnings("unused")
	private void debug(HttpExchange t) {
		System.out.println(
				"Thread '" + Thread.currentThread().getName() + "' tratando a requisição '" + t.getRequestURI() + "'");
	}

	/**
	 * Realiza o tratamento de uma determinada requisição HTTP.
	 */
	@Override
	public void handle(HttpExchange t) throws IOException {
//		debug(t);
		t.getResponseHeaders().set("Content-Type", "text/html; charset=UTF-8");
		OutputStream out = t.getResponseBody();
		File file = new File(MultithreadedWebServer.rootDirectory + t.getRequestURI());
		if (file.exists() && file.isFile()) {
			try {
				t.sendResponseHeaders(200, file.length());
				Path path = file.toPath();
				Files.copy(path, out);
				out.flush();
			} catch (Exception e) {
				t.sendResponseHeaders(500, e.getMessage().length());
				out.write(e.getMessage().getBytes());
			}
		} else {
			String message = "File Not Found!";
			t.sendResponseHeaders(404, message.length());
			out.write(message.getBytes());
		}
		out.close();
	}
}