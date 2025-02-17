import multiprocessing
from typing import List, Tuple

def multiplicar_linha(args: Tuple[List[int], List[List[int]]]) -> List[int]:
    """
    Multiplica uma linha da matriz A pela matriz B.
    """
    linha, matriz_b = args
    return [sum(a * b for a, b in zip(linha, col)) for col in zip(*matriz_b)]

def multiplicacao_sequencial(matriz_a: List[List[int]], matriz_b: List[List[int]]) -> List[List[int]]:
    """
    Multiplica duas matrizes de forma sequencial.
    """
    return [multiplicar_linha((linha, matriz_b)) for linha in matriz_a]

def multiplicacao_paralela(matriz_a: List[List[int]], matriz_b: List[List[int]]) -> List[List[int]]:
    """
    Multiplica duas matrizes de forma paralela, dividindo o trabalho por linhas.
    """
    with multiprocessing.Pool(processes=len(matriz_a)) as pool:
        matriz_resultante = pool.map(multiplicar_linha, [(linha, matriz_b) for linha in matriz_a])
    return matriz_resultante

if __name__ == "__main__":
    # Matrizes de exemplo (3x3)
    matriz_a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    matriz_b = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]

    # Multiplicação paralela
    matriz_resultante = multiplicacao_paralela(matriz_a, matriz_b)
    
    # Exibir matriz resultante
    print("Matriz resultante:")
    for linha in matriz_resultante:
        print(linha)