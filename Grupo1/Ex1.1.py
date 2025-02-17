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
    
    print("In-order:", arvore.percurso_in_ordem())
    print("Pre-order:", arvore.percurso_pre_ordem())
    print("Post-order:", arvore.percurso_pos_ordem())
