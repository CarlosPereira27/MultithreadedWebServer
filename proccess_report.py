# -*- coding: utf-8 -*-
#!/usr/bin/python3

from __future__ import unicode_literals
import sys, getopt
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import math

# --------------------------------------------------------
# ---------------- BEGIN Parâmetros ----------------------
# --------------------------------------------------------

# Arquivo do relatório gerado
report_files = [ "reports/gcloud/report_gcloud_ssh_com.csv", \
"reports/gcloud_48clients/report.csv" ]

# Quantidade de testes realizados
qty_tests = 10

# Valor crítico para um grau de confiança de 95%
critical_value_z = 1.96

# Sufixos dos tempos salvos
out_files_suffix = [ "time" ]

# --------------------------------------------------------
# ---------------- END Parâmetros ------------------------
# --------------------------------------------------------

def mean(values):
    """
    Cálcula a média de uma coleção de valores.

    @param values : list<float>
        lista de valores a ser cálculada a média

    @return : float
        média da coleção de valores
    """
    return sum(values) / len(values)

def standard_deviation(values, mean):
    """
    Cálcula o desvio padrão de uma coleção de valores.

    @param values : list<float>
        lista de valores a ser cálculado o desvio padrão
    
    @param mean : float
        média dos valores analisados

    @return : float
        desvio padrão da coleção de valores
    """
    std_deviation = 0
    for value in values:
        std_deviation += pow(value - mean, 2)
    return pow(std_deviation / (len(values) - 1), 0.5)

def verifyNThreads(nthreads):
    """
    Valida se todos números de processos dos testes do cenário analisado
    estão iguais (corretos), caso esteja incorreto a aplicação encerra
    com erro

    @param nthreads : int
        número de threads dos testes do cenário analisado
    """
    for i in range(qty_tests - 1):
        if nthreads[i] != nthreads[i + 1]:
            print ("ERRO! Caso de teste com número de processos diferentes.")
            print (nthreads)
            exit(2)

def plotChart(filename, xdata, ydata, xlabel, ylabel):
    """
    Desenha um gráfico de linha.

    @param filename : str
        nome do arquivo em que o gráfico será salvo
    @param xdata : list
        dados do eixo x
    @param ydata : list
        dados do eixo y
    @param xlabel : str
        rótulo do eixo x
    @param ylabel : str
        rótulo do eixo y
    """
    plt.plot(xdata, ydata, 'bo-', lw = 3, mew = 5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(os.path.join(filename + ".png"), dpi=300)
    plt.gcf().clear()

def plotChartGeneralIdealLine(filename, xdata, ydata, \
        xlabel, ylabel, yideal):
    """
    Desenha um gráfico com quatro linhas para valores de y diferente e insere suas legendas.

    @param filename : str
        nome do arquivo em que o gráfico será salvo
    @param xdata : list
        dados do eixo x
    @param ydata : list
        dados do eixo y, linha 0 
    @param leg : str
        legenda para a linha 0
    @param xlabel : str
        rótulo do eixo x
    @param ylabel : str
        rótulo do eixo y
    """
    lw_val = 3
    mew_val = 4
    line0, = plt.plot(xdata, ydata, 'bo-', lw = lw_val, mew = mew_val)
    line1, = plt.plot(xdata, yideal, 'k--', lw = 2.2, mew = 0, label="ideal")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(handles=[line1]);
    plt.savefig(os.path.join(filename + ".png"), dpi=300)
    plt.gcf().clear()


class Report:
    """
    Representa um relatório de uma determinada base de dados.
    """

    def __init__(self, qty_times, critical_value_z, qty_tests):
        """
        Constrói um relatório para uma determinada quantidade de tempos salvos, 
        determinado valor crítico do grau de confiança do intervalo de confiança,
        e determinada quantidade de testes.

        @param qty_times : int
            quantidade de tempos usados no relatório
        @param critical_value_z : float
            valor crítico do grau de confiança do intervalo de confiança
        @param qty_tests : int
            quantidade de testes realizados em cada cenário
        """
        self.qty_times = qty_times
        self.qty_tests = qty_tests
        self.critical_value_z = critical_value_z
        self.time_mean = list()
        self.dev_confid_inter = list()
        self.speedup = list()
        self.efficiency = list()
        for i in range(self.qty_times):
            self.time_mean.append(list())
            self.dev_confid_inter.append(list())
            self.speedup.append(list())
            self.efficiency.append(list())
        self.nthreads = list()


    def includeReportUnit(self, report_unit, index, nthreads_unit):
        """
        Inclui uma nova unidade de relatório nesse relatório.

        @param report_unit : list<list<int>>
            unidade de relatório, uma unidade de relatório é uma matrix onde cada
            linha corresponde a um tipo de tempo dos qty_times tipos de tempo e
            dentro de cada linha contém qty_times de tempos desse tipo
        @param index : int
            índice da unidade de relatório, representa o índice do número de processos
        @param nthreads_unit : int
            número de threads da unidade de relatório

        """
        self.calcMean(report_unit)
        self.calcDevConfidInter(report_unit, index)
        self.calcSpeedup(report_unit, index)
        self.calcEfficiency(report_unit, index, nthreads_unit)
        self.nthreads.append(nthreads_unit)

    def calcMean(self, report_unit):
        """
        Calcula a média dos tempos da unidade de relatório.

        @param report_unit : list<list<int>>
            unidade de relatório, uma unidade de relatório é uma matrix onde cada
            linha corresponde a um tipo de tempo dos qty_times tipos de tempo e
            dentro de cada linha contém qty_times de tempos desse tipo
        """
        for i in range(self.qty_times):
            self.time_mean[i].append(int(mean(report_unit[i])))

    def getStdDev(self, report_unit, index):
        """
        Calcula o desvio padrão dos tempos da unidade de relatório.

        @param report_unit : list<list<int>>
            unidade de relatório, uma unidade de relatório é uma matrix onde cada
            linha corresponde a um tipo de tempo dos qty_times tipos de tempo e
            dentro de cada linha contém qty_times de tempos desse tipo
        @param index : int
            índice da unidade de relatório, representa o índice do número de processos

        @return list<float>
            desvio padrão dos tempos da unidade de relatório.
        """
        std_deviation_report = list()
        for j in range(self.qty_times):
            std_deviation_report.append(standard_deviation(report_unit[j], self.time_mean[j][index]))
        return std_deviation_report

    def calcDevConfidInter(self, report_unit, index):
        """
        Calcula o intervalo de confiança da unidade de relatório.

        @param report_unit : list<list<int>>
            unidade de relatório, uma unidade de relatório é uma matrix onde cada
            linha corresponde a um tipo de tempo dos qty_times tipos de tempo e
            dentro de cada linha contém qty_times de tempos desse tipo
        @param index : int
            índice da unidade de relatório, representa o índice do número de processos
        """
        std_deviation_report = self.getStdDev(report_unit, index)
        for i in range(self.qty_times):
            self.dev_confid_inter[i].append(int(self.critical_value_z * \
                (std_deviation_report[i] / (pow(self.qty_tests, 0.5)))))

    def calcSpeedup(self, report_unit, index):
        """
        Calcula speedup da unidade de relatório.

        @param report_unit : list<list<int>>
            unidade de relatório, uma unidade de relatório é uma matrix onde cada
            linha corresponde a um tipo de tempo dos qty_times tipos de tempo e
            dentro de cada linha contém qty_times de tempos desse tipo
        @param index : int
            índice da unidade de relatório, representa o índice do número de processos
        """
        for i in range(self.qty_times):
            self.speedup[i].append(self.time_mean[i][0] / self.time_mean[i][index])

    def calcEfficiency(self, report_unit, index, nthreads_unit):
        """
        Calcula eficiência da unidade de relatório.

        @param report_unit : list<list<int>>
            unidade de relatório, uma unidade de relatório é uma matrix onde cada
            linha corresponde a um tipo de tempo dos qty_times tipos de tempo e
            dentro de cada linha contém qty_times de tempos desse tipo
        @param index : int
            índice da unidade de relatório, representa o índice do número de processos
        @param nthreads_unit : int
            número de threads da unidade de relatório
        """
        for i in range(self.qty_times):
            self.efficiency[i].append(self.speedup[i][index] / nthreads_unit)

    def generateFinalReportCsv(self, pathfile, out_files_suffix):
        """
        Gera as planilhas com os resultados estatísticos do relatório.

        @param pathfile : str
            caminho e nome do arquivo original do relatório
        @param out_files_suffix : list<str>
            lista de sufixos para planilhas de cada tipo de tempo analisado
        """
        for i in range(self.qty_times):
            file_out = open(pathfile[:-4] + "_" + out_files_suffix[i] + "_final.csv", 'w')
            file_out.write("nthreads,time_mean,confidence_interval,speedup,efficiency\n")
            N = len(self.nthreads)
            for j in range(N):
                file_out.write("%d" % (self.nthreads[j]))
                file_out.write(",%d,[%d - %d],%f,%f\n" % (self.time_mean[i][j], \
                    self.time_mean[i][j] - self.dev_confid_inter[i][j], \
                    self.time_mean[i][j] + self.dev_confid_inter[i][j], \
                    self.speedup[i][j], self.efficiency[i][j]))
            file_out.close()

    def generateCharts(self, pathfile, out_files_suffix):
        """
        Gera os gráficos com os resultados estatísticos do relatório.

        @param pathfile : str
            caminho e nome do arquivo original do relatório
        @param out_files_suffix : list<str>
            lista de sufixos para planilhas de cada tipo de tempo analisado
        """
        speedup_ideal = []
        efficiency_ideal = []
        for nthread in self.nthreads:
            speedup_ideal.append(nthread)
        for i in range(len(self.nthreads)):
            efficiency_ideal.append(1)
        for i in range(self.qty_times):
            log_time_mean = []
            N = len(self.time_mean[i])
            for l in range(N):
                log_time_mean.append(math.log(self.time_mean[i][l]))
            plotChart(pathfile[:-4] + "_" + out_files_suffix[i] + "_mean", self.nthreads, \
                log_time_mean, "nthreads", "log(tempo)")
            plotChartGeneralIdealLine(pathfile[:-4] + "_" + out_files_suffix[i] + "_speedup", \
                self.nthreads, self.speedup[i], "nthreads", "speedup", speedup_ideal)
            plotChartGeneralIdealLine(pathfile[:-4] + "_" + out_files_suffix[i] + "_efficiency", \
                self.nthreads, self.efficiency[i], "nthreads", "eficiência", efficiency_ideal)

def main(argv):
    qty_times = 1

    for pathfile in report_files:
        report = Report(qty_times, critical_value_z, qty_tests)
        file = open(pathfile, 'r')
        reading = True
        index = 0
        line = file.readline()
        while reading:
            report_unit = list()
            nthreads_aux = list()
            for j in range(qty_times):
                report_unit.append(list())

            for i in range(qty_tests):
                line = file.readline()
                if not line:
                    # Se não consegir ler no ínicio de um cenário de teste, arquivo
                    # acabou corretamente, caso contrário não, então a aplicação 
                    # encerra com erro
                    if i == 0:
                        reading = False
                        break
                    print ("ERRO! Não foi possível ler cenário de teste inteiro.")
                    exit(2)

                tokens = line.split(",")
                for j in range(qty_times):
                    report_unit[j].append(int(tokens[j]))
                nthreads_aux.append(int(tokens[qty_times + 3]))
            if not reading:
                break
            verifyNThreads(nthreads_aux)
            report.includeReportUnit(report_unit, index, nthreads_aux[0])
            index += 1

        file.close()
        report.generateFinalReportCsv(pathfile, out_files_suffix)
        report.generateCharts(pathfile, out_files_suffix)

if __name__ == "__main__":
    main(sys.argv[1:])