import multiprocessing
import time
import matplotlib.pyplot as plt
import gc

def crivo_eratostenes(limite):
    primos = [True] * (limite + 1)
    primos[0] = primos[1] = False
    for i in range(2, int(limite**0.5) + 1):
        if primos[i]:
            for j in range(i * i, limite + 1, i):
                primos[j] = False
    return [num for num, is_prime in enumerate(primos) if is_prime]

def count_primes_in_range(start, end, primos):
    return sum(1 for p in primos if start <= p <= end)

def parallel_prime_count(start, end, num_processes, primos):
    pool = multiprocessing.Pool(processes=num_processes)
    chunk_size = (end - start) // num_processes
    ranges = [(start + i * chunk_size, start + (i + 1) * chunk_size - 1) for i in range(num_processes)]
    ranges[-1] = (ranges[-1][0], end)
    
    results = pool.starmap(count_primes_in_range, [(r[0], r[1], primos) for r in ranges])
    pool.close()
    pool.join()
    
    return sum(results)

def plotar_grafico_primos(num_processes, elapsed_time_avg):
    plt.figure(figsize=(10, 5))
    plt.plot(num_processes, elapsed_time_avg, marker='o', linestyle='-', color='b')
    plt.xlabel("Número de Processos")
    plt.ylabel("Tempo Médio de Execução (s)")
    plt.title("Impacto do Número de Processos na Contagem de Números Primos")
    plt.xticks(num_processes)
    plt.grid()
    plt.savefig("E2_3_tempo_primos_Era.png")
    print("Gráfico salvo como E2_3_tempo_primos.png")

if __name__ == "__main__":
    start = 1
    end = 100000
    primos = crivo_eratostenes(end)
    num_cores = multiprocessing.cpu_count()
    num_executions = 5
    
    print(f"Número de núcleos disponíveis: {num_cores}")
    
    num_processes_list = list(range(1, num_cores + 1))
    elapsed_time_avg = []
    
    print("Aquecendo a CPU...")
    for _ in range(100000000):
        pass
    
    for num_processes in num_processes_list:
        print(f"\nExecutando com {num_processes} processo(s)...")
        execution_times = []
        
        for _ in range(num_executions):
            gc.disable()
            start_time = time.perf_counter()
            total_primes = parallel_prime_count(start, end, num_processes, primos)
            end_time = time.perf_counter()
            gc.enable()
            
            elapsed_time = end_time - start_time
            execution_times.append(elapsed_time)
        
        avg_time = sum(execution_times) / num_executions
        elapsed_time_avg.append(avg_time)
        
        print(f"Total de números primos entre {start} e {end}: {total_primes}")
        print(f"Tempo médio de execução: {avg_time:.3f} segundos")
    
    plotar_grafico_primos(num_processes_list, elapsed_time_avg)
