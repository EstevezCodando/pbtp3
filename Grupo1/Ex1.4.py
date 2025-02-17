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

    def remover(self, valor: int):
        """Remove um nó da árvore binária de busca."""
        self.raiz = self._remover_recursivo(self.raiz, valor)
    
    def _remover_recursivo(self, no: No, valor: int):
        if no is None:
            return no
        
        if valor < no.valor:
            no.esquerda = self._remover_recursivo(no.esquerda, valor)
        elif valor > no.valor:
            no.direita = self._remover_recursivo(no.direita, valor)
        else:
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda
            
            sucessor = self._menor_valor(no.direita)
            no.valor = sucessor.valor
            no.direita = self._remover_recursivo(no.direita, sucessor.valor)
        
        return no
    
    def _menor_valor(self, no: No):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def buscar(self, valor: int) -> bool:
        """Busca um valor na árvore binária de busca."""
        return self._buscar_recursivo(self.raiz, valor)
    
    def _buscar_recursivo(self, no: No, valor: int) -> bool:
        if no is None:
            return False
        if valor == no.valor:
            return True
        elif valor < no.valor:
            return self._buscar_recursivo(no.esquerda, valor)
        else:
            return self._buscar_recursivo(no.direita, valor)

    def verificar_bst(self) -> bool:
        """Verifica se a árvore é uma BST válida."""
        return self._verificar_bst_recursivo(self.raiz, float('-inf'), float('inf'))
    
    def _verificar_bst_recursivo(self, no: No, minimo: float, maximo: float) -> bool:
        if no is None:
            return True
        if not (minimo < no.valor < maximo):
            return False
        return (self._verificar_bst_recursivo(no.esquerda, minimo, no.valor) and
                self._verificar_bst_recursivo(no.direita, no.valor, maximo))

    def percurso_in_ordem(self):
        """Retorna a lista de valores no percurso in-ordem."""
        return self._percorrer_in_ordem(self.raiz, [])
    
    def _percorrer_in_ordem(self, no: No, valores: list):
        if no:
            self._percorrer_in_ordem(no.esquerda, valores)
            valores.append(no.valor)
            self._percorrer_in_ordem(no.direita, valores)
        return valores
    
    def percurso_pre_ordem(self):
        """Retorna a lista de valores no percurso pré-ordem."""
        return self._percorrer_pre_ordem(self.raiz, [])
    
    def _percorrer_pre_ordem(self, no: No, valores: list):
        if no:
            valores.append(no.valor)
            self._percorrer_pre_ordem(no.esquerda, valores)
            self._percorrer_pre_ordem(no.direita, valores)
        return valores
    
    def percurso_pos_ordem(self):
        """Retorna a lista de valores no percurso pós-ordem."""
        return self._percorrer_pos_ordem(self.raiz, [])
    
    def _percorrer_pos_ordem(self, no: No, valores: list):
        if no:
            self._percorrer_pos_ordem(no.esquerda, valores)
            self._percorrer_pos_ordem(no.direita, valores)
            valores.append(no.valor)
        return valores

# Exemplo de uso
if __name__ == "__main__":
    arvore = ArvoreBinariaBusca()
    elementos = [50, 30, 70, 20, 40, 60, 80]
    for elemento in elementos:
        arvore.inserir(elemento)
    
  
    # Testando se a árvore continua sendo uma BST válida
    print("A árvore é uma BST válida?", arvore.verificar_bst())

    # Inserindo valor errado para tornar BST invalida.
    arvore.raiz.direita.valor = 10
    
    print("A árvore ainda é uma BST válida?", arvore.verificar_bst())

