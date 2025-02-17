import ipaddress

class NodoTrie:
    def __init__(self):
        self.filhos = {}
        self.eh_prefixo = False

class TrieIP:
    def __init__(self):
        self.raiz = NodoTrie()

    def inserir_prefixo(self, prefixo):
        """Insere um prefixo IPv4 na árvore Trie."""
        rede = ipaddress.ip_network(prefixo, strict=False)
        nodo_atual = self.raiz
        for bit in self._ip_para_bits(rede.network_address, rede.prefixlen):
            if bit not in nodo_atual.filhos:
                nodo_atual.filhos[bit] = NodoTrie()
            nodo_atual = nodo_atual.filhos[bit]
        nodo_atual.eh_prefixo = True

    def buscar_ip(self, endereco):
        """Busca se um endereço IPv4 está dentro de algum prefixo armazenado."""
        ip = ipaddress.ip_address(endereco)
        nodo_atual = self.raiz
        for bit in self._ip_para_bits(ip, 32):
            if nodo_atual.eh_prefixo:
                return True  # Encontrou um prefixo válido
            if bit not in nodo_atual.filhos:
                return False
            nodo_atual = nodo_atual.filhos[bit]
        return nodo_atual.eh_prefixo

    def _ip_para_bits(self, ip, bits):
        """Converte um endereço IP em uma sequência de bits limitada ao prefixo."""
        return bin(int(ip))[2:].zfill(32)[:bits]

# Exemplo de uso
trie = TrieIP()
trie.inserir_prefixo("192.168.1.0/24")

# Testando se o IP está dentro do prefixo
ip_teste = "192.168.1.5"
print(f"O IP {ip_teste} está no prefixo? {trie.buscar_ip(ip_teste)}")  # Deve retornar True

ip_teste2 = "192.168.2.5"
print(f"O IP {ip_teste2} está no prefixo? {trie.buscar_ip(ip_teste2)}")  # Deve retornar False
