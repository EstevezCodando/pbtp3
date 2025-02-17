import multiprocessing
import time

# Função para verificar se um número é primo
def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# Abordagem sequencial
def sequential_prime_count(start, end):
    count = 0
    for num in range(start, end + 1):
        if is_prime(num):
            count += 1
    return count

# Abordagem paralela
def parallel_prime_count(start, end, num_processes):
    pool = multiprocessing.Pool(processes=num_processes)
    ranges = [(i, min(i + (end - start) // num_processes, end)) for i in range(start, end, (end - start) // num_processes)]
    
    results = pool.starmap(count_primes_in_range, ranges)
    pool.close()
    pool.join()
    
    return sum(results)

# Função auxiliar para contar primos em um intervalo (usada na abordagem paralela)
def count_primes_in_range(start, end):
    count = 0
    for num in range(start, end + 1):
        if is_prime(num):
            count += 1
    return count

# Função principal
if __name__ == "__main__":
    start = 1
    end = 1000000
    num_processes = multiprocessing.cpu_count()
    print(f"Intervalo: {start} a {end}")
    print(f"Número de núcleos disponíveis: {num_processes}")

    # Execução sequencial
    print("\nExecutando abordagem sequencial...")
    start_time = time.time()
    total_primes_seq = sequential_prime_count(start, end)
    end_time = time.time()
    elapsed_time_seq = end_time - start_time
    print(f"Total de números primos (sequencial): {total_primes_seq}")
    print(f"Tempo de execução (sequencial): {elapsed_time_seq:.2f} segundos")

    # Execução paralela
    print("\nExecutando abordagem paralela...")
    start_time = time.time()
    total_primes_par = parallel_prime_count(start, end, num_processes)
    end_time = time.time()
    elapsed_time_par = end_time - start_time
    print(f"Total de números primos (paralela): {total_primes_par}")
    print(f"Tempo de execução (paralela): {elapsed_time_par:.2f} segundos")

    # Comparação de desempenho
    speedup = elapsed_time_seq / elapsed_time_par
    print(f"\nSpeedup (ganho de desempenho): {speedup:.2f}x")