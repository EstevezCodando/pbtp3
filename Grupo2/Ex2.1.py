import multiprocessing
import time
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Usa um backend não interativo
import matplotlib.pyplot as plt

def soma_parcial(lista):
    return sum(lista)

def soma_paralela(numeros, num_processos):
    if num_processos < 1:
        raise ValueError("O número de processos deve ser pelo menos 1.")
    
    partes = np.array_split(numeros, num_processos)  # Melhor balanceamento da carga
    
    with multiprocessing.Pool(num_processos) as pool:
        resultados = pool.map(soma_parcial, partes)
    
    return sum(resultados)

def medir_tempo(numeros, max_processos):
    tempos = []
    processos = list(range(1, max_processos + 1))
    
    for num_processos in processos:
        inicio = time.time()
        soma_paralela(numeros, num_processos)
        fim = time.time()
        tempo_execucao = fim - inicio
        tempos.append(tempo_execucao)
        print(f"Processos: {num_processos}, Tempo: {tempo_execucao:.4f} segundos")
    
    return processos, tempos

def plotar_grafico(processos, tempos):
    plt.figure(figsize=(10, 5))
    plt.plot(processos, tempos, marker='o', linestyle='-', color='b')
    plt.xlabel("Número de Processos")
    plt.ylabel("Tempo de Execução (s)")
    plt.title("Impacto do Número de Processos no Tempo de Execução")
    plt.xticks(processos)
    plt.grid()
    plt.savefig("E2_1_tempo_execucao.png")  # Salva a imagem em um arquivo PNG
    print("Gráfico salvo como tempo_execucao.png")

if __name__ == "__main__":
    numeros = list(range(1, 10_000_001))  # Lista de 1 até 10 milhões
    max_processos = os.cpu_count() // 2  # Usa apenas núcleos físicos
    processos, tempos = medir_tempo(numeros, max_processos)
    plotar_grafico(processos, tempos)
