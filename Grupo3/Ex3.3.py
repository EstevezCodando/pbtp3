import threading

class No:
    def __init__(self, valor: int):
        self.valor = valor
        self.esquerda = None
        self.direita = None

class ArvoreBinariaBusca:
    def __init__(self):
        self.raiz = None
    
    def inserir(self, valor: int):
        """Insere um valor na árvore binária de busca."""
        if self.raiz is None:
            self.raiz = No(valor)
        else:
            self._inserir_recursivo(self.raiz, valor)
    
    def _inserir_recursivo(self, no_atual: No, valor: int):
        if valor < no_atual.valor:
            if no_atual.esquerda is None:
                no_atual.esquerda = No(valor)
            else:
                self._inserir_recursivo(no_atual.esquerda, valor)
        else:
            if no_atual.direita is None:
                no_atual.direita = No(valor)
            else:
                self._inserir_recursivo(no_atual.direita, valor)

    def buscar_profundidade_paralelo(self, valor: int) -> list:
        """Busca um valor na árvore binária de forma paralela e retorna o caminho até ele."""
        if self.raiz is None:
            return []
        
        caminho_esquerda = []
        caminho_direita = []
        encontrado_esquerda = encontrado_direita = False

        def buscar_esquerda():
            nonlocal encontrado_esquerda, caminho_esquerda
            encontrado_esquerda, caminho_esquerda = self._buscar_dfs(self.raiz.esquerda, valor, [self.raiz.valor])

        def buscar_direita():
            nonlocal encontrado_direita, caminho_direita
            encontrado_direita, caminho_direita = self._buscar_dfs(self.raiz.direita, valor, [self.raiz.valor])

        thread_esquerda = threading.Thread(target=buscar_esquerda)
        thread_direita = threading.Thread(target=buscar_direita)
        
        thread_esquerda.start()
        thread_direita.start()
        
        thread_esquerda.join()
        thread_direita.join()
        
        if encontrado_esquerda:
            return caminho_esquerda
        elif encontrado_direita:
            return caminho_direita
        return []
    
    def _buscar_dfs(self, no: No, valor: int, caminho: list) -> tuple:
        if no is None:
            return False, []
        caminho.append(no.valor)
        if no.valor == valor:
            return True, caminho
        encontrado_esquerda, caminho_esquerda = self._buscar_dfs(no.esquerda, valor, caminho[:])
        if encontrado_esquerda:
            return True, caminho_esquerda
        encontrado_direita, caminho_direita = self._buscar_dfs(no.direita, valor, caminho[:])
        return encontrado_direita, caminho_direita

    def encontrar_maximo_paralelo(self) -> int:
        """Encontra o valor máximo da árvore de forma paralela."""
        if self.raiz is None:
            return float('-inf')
        
        max_esquerda = max_direita = self.raiz.valor
        
        def buscar_maximo_esquerda():
            nonlocal max_esquerda
            max_esquerda = self._encontrar_maximo(self.raiz.esquerda)
        
        def buscar_maximo_direita():
            nonlocal max_direita
            max_direita = self._encontrar_maximo(self.raiz.direita)
        
        thread_esquerda = threading.Thread(target=buscar_maximo_esquerda)
        thread_direita = threading.Thread(target=buscar_maximo_direita)
        
        thread_esquerda.start()
        thread_direita.start()
        
        thread_esquerda.join()
        thread_direita.join()
        
        return max(max_esquerda, max_direita)
    
    def _encontrar_maximo(self, no: No) -> int:
        if no is None:
            return float('-inf')
        while no.direita is not None:
            no = no.direita
        return no.valor

# Exemplo de uso
if __name__ == "__main__":
    arvore = ArvoreBinariaBusca()
    elementos = [15, 10, 20, 8, 12, 17, 25]
    for elemento in elementos:
        arvore.inserir(elemento)
    
  
    # Testando a busca paralela pelo valor máximo
    maximo = arvore.encontrar_maximo_paralelo()
    print(f"O maior valor na árvore é {maximo}.")
