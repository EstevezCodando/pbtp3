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

    def buscar_paralelo(self, valor: int) -> bool:
        """Busca um valor na árvore binária de forma paralela."""
        if self.raiz is None:
            return False
        
        if self.raiz.valor == valor:
            return True

        resultado_esquerda = resultado_direita = False
        
        def buscar_esquerda():
            nonlocal resultado_esquerda
            resultado_esquerda = self._buscar_recursivo(self.raiz.esquerda, valor)
        
        def buscar_direita():
            nonlocal resultado_direita
            resultado_direita = self._buscar_recursivo(self.raiz.direita, valor)
        
        thread_esquerda = threading.Thread(target=buscar_esquerda)
        thread_direita = threading.Thread(target=buscar_direita)
        
        thread_esquerda.start()
        thread_direita.start()
        
        thread_esquerda.join()
        thread_direita.join()
        
        return resultado_esquerda or resultado_direita
    
    def _buscar_recursivo(self, no: No, valor: int) -> bool:
        if no is None:
            return False
        if valor == no.valor:
            return True
        elif valor < no.valor:
            return self._buscar_recursivo(no.esquerda, valor)
        else:
            return self._buscar_recursivo(no.direita, valor)

# Exemplo de uso
if __name__ == "__main__":
    arvore = ArvoreBinariaBusca()
    elementos = [50, 30, 70, 20, 40, 60, 80]
    for elemento in elementos:
        arvore.inserir(elemento)
    
    # Testando a busca paralela
    valor_busca = 60
    encontrado = arvore.buscar_paralelo(valor_busca)
    print(f"O valor {valor_busca} {'foi encontrado' if encontrado else 'não foi encontrado'} na árvore.")
