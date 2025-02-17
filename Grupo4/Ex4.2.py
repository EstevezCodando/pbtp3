import ipaddress

class NodoTrie:
    def __init__(self):
        self.filhos = {}
        self.prefixo = None  # Armazena o prefixo válido mais longo encontrado

class TrieIP:
    def __init__(self):
        self.raiz = NodoTrie()

    def inserir_prefixo(self, prefixo):
        """Insere um prefixo IPv4 na Trie."""
        rede = ipaddress.ip_network(prefixo, strict=False)
        nodo_atual = self.raiz
        for bit in self._ip_para_bits(rede.network_address, rede.prefixlen):
            if bit not in nodo_atual.filhos:
                nodo_atual.filhos[bit] = NodoTrie()
            nodo_atual = nodo_atual.filhos[bit]
        nodo_atual.prefixo = str(rede)  # Armazena o prefixo mais específico nesse nó

    def buscar_longest_prefix_match(self, endereco):
        """Retorna o prefixo mais longo que corresponde ao IP dado."""
        ip = ipaddress.ip_address(endereco)
        nodo_atual = self.raiz
        melhor_correspondencia = None

        for bit in self._ip_para_bits(ip, 32):
            if nodo_atual.prefixo:
                melhor_correspondencia = nodo_atual.prefixo  # Atualiza com o prefixo mais longo encontrado
            if bit not in nodo_atual.filhos:
                break  # Sai do loop se não houver mais correspondências
            nodo_atual = nodo_atual.filhos[bit]

        return melhor_correspondencia

    def _ip_para_bits(self, ip, bits):
        """Converte um endereço IP em uma sequência de bits limitada ao prefixo."""
        return bin(int(ip))[2:].zfill(32)[:bits]

# Exemplo de uso
trie = TrieIP()
prefixos = ["192.168.0.0/16", "192.168.1.0/24", "10.0.0.0/8"]
for p in prefixos:
    trie.inserir_prefixo(p)

# Teste com um IP específico
ip_teste = "192.168.1.100"
print(f"O prefixo mais específico para {ip_teste} é {trie.buscar_longest_prefix_match(ip_teste)}")  
# Deve retornar "192.168.1.0/24"

ip_teste2 = "10.0.45.12"
print(f"O prefixo mais específico para {ip_teste2} é {trie.buscar_longest_prefix_match(ip_teste2)}")  
# Deve retornar "10.0.0.0/8"

ip_teste3 = "172.16.5.1"
print(f"O prefixo mais específico para {ip_teste3} é {trie.buscar_longest_prefix_match(ip_teste3)}")  
# Deve retornar None (pois não há prefixo correspondente)
