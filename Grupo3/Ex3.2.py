import threading

class No:
    def __init__(self, valor: int):
        self.valor = valor
        self.esquerda = None
        self.direita = None

class ArvoreBinariaBusca:
    def __init__(self):
        self.raiz = None
        self.contador = 0  # Contador de nós inseridos
    
    def inserir(self, valor: int):
        """Insere um valor na árvore binária de busca."""
        if self.raiz is None:
            self.raiz = No(valor)
            self.contador += 1
        else:
            self._inserir_recursivo(self.raiz, valor)
    
    def _inserir_recursivo(self, no_atual: No, valor: int):
        if valor < no_atual.valor:
            if no_atual.esquerda is None:
                no_atual.esquerda = No(valor)
                self.contador += 1
            else:
                self._inserir_recursivo(no_atual.esquerda, valor)
        else:
            if no_atual.direita is None:
                no_atual.direita = No(valor)
                self.contador += 1
            else:
                self._inserir_recursivo(no_atual.direita, valor)
    
    def buscar_n_esimo_no_paralelo(self, n: int) -> list:
        """Busca o caminho até o n-ésimo nó inserido utilizando paralelismo."""
        if self.raiz is None or n < 1 or n > self.contador:
            return []
        contador = [0]
        caminho = []
        lock = threading.Lock()

        def buscar_dfs(no, caminho_atual):
            if no is None:
                return []
            
            with lock:
                contador[0] += 1
                if contador[0] == n:
                    caminho_atual.append(no.valor)
                    caminho.extend(caminho_atual)
                    return
            
            caminho_atual.append(no.valor)
            thread_esquerda = threading.Thread(target=buscar_dfs, args=(no.esquerda, caminho_atual[:]))
            thread_direita = threading.Thread(target=buscar_dfs, args=(no.direita, caminho_atual[:]))
            
            thread_esquerda.start()
            thread_direita.start()
            
            thread_esquerda.join()
            thread_direita.join()
        
        buscar_dfs(self.raiz, [])
        return caminho

# Exemplo de uso
if __name__ == "__main__":
    arvore = ArvoreBinariaBusca()
    elementos = [1, 2, 3, 4, 5, 6, 7,8]
    for elemento in elementos:
        arvore.inserir(elemento)
    
    # Testando a busca do 5º nó inserido paralelamente
    n = 5
    caminho = arvore.buscar_n_esimo_no_paralelo(n)
    if caminho:
        print(f"O {n}º nó foi encontrado. Caminho: {caminho}")
    else:
        print(f"O {n}º nó não foi encontrado na árvore.")
