package org.ufla.multithreadedwebserver;

/**
 * Representa a configuração do servidor.
 * 
 * @author andre
 * @author caio
 * @author carlos
 *
 */
public class ServerConfiguration {

	/**
	 * Porta que servidor web ficará ouvindo.
	 */
	private int portListener = 8008;
	/**
	 * Capacidade máxima da fila de requisições.
	 */
	private int capacityQueue = 10;
	/**
	 * Tamanho do pool de threads do executor.
	 */
	private int poolSize = 3;
	/**
	 * Determina se o servidor deve realizar o log dos 
	 * tratamentos de requisições ou não.
	 */
	private boolean log = false;
	/**
	 * Instância da configuração do servidor.
	 */
	private static ServerConfiguration serverConfiguration;

	public ServerConfiguration() {
		portListener = 8008;
		capacityQueue = 10;
		poolSize = 3;
		log = false;
	}

	/**
	 * Recupera instância da configuração do servidor.
	 * 
	 * @return
	 */
	public static ServerConfiguration getInstance() {
		if (serverConfiguration == null) {
			serverConfiguration = new ServerConfiguration();
		}
		return serverConfiguration;
	}
	
	/**
	 * Verifica se o modo de log está ativado ou desativado.
	 * 
	 * @return true, se o modo de log está ativado ou false, caso contrário
	 */
	public static boolean onLog() {
		return getInstance().isLog();
	}

	public int getPortListener() {
		return portListener;
	}

	public void setPortListener(int portListener) {
		this.portListener = portListener;
	}

	public int getCapacityQueue() {
		return capacityQueue;
	}

	public void setCapacityQueue(int capacityQueue) {
		this.capacityQueue = capacityQueue;
	}

	public int getPoolSize() {
		return poolSize;
	}

	public void setPoolSize(int poolSize) {
		this.poolSize = poolSize;
	}
	
	public boolean isLog() {
		return log;
	}

	public void setLog(boolean log) {
		this.log = log;
	}

}
