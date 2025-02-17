import ipaddress

class NodoTrie:
    def __init__(self):
        self.filhos = {}
        self.prefixo = None  # Armazena o prefixo mais longo encontrado

class TrieIPv6:
    def __init__(self):
        self.raiz = NodoTrie()

    def inserir_prefixo(self, prefixo):
        """Insere um prefixo IPv6 na Trie."""
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

        for bit in self._ip_para_bits(ip, 128):
            if nodo_atual.prefixo:
                melhor_correspondencia = nodo_atual.prefixo  # Atualiza o melhor prefixo encontrado
            if bit not in nodo_atual.filhos:
                break  # Sai do loop se não houver mais correspondências
            nodo_atual = nodo_atual.filhos[bit]

        return melhor_correspondencia

    def _ip_para_bits(self, ip, bits):
        """Converte um endereço IPv6 em uma sequência de bits limitada ao prefixo."""
        return bin(int(ip))[2:].zfill(128)[:bits]

# Exemplo de uso
trie_ipv6 = TrieIPv6()
prefixos_ipv6 = ["2001:db8::/32", "2001:db8:1234::/48"]
for p in prefixos_ipv6:
    trie_ipv6.inserir_prefixo(p)

# Teste com um IP específico
ip_teste = "2001:db8:1234:5678::1"
print(f"O prefixo mais específico para {ip_teste} é {trie_ipv6.buscar_longest_prefix_match(ip_teste)}")  
# Deve retornar "2001:db8:1234::/48"

ip_teste2 = "2001:db8:5678::1"
print(f"O prefixo mais específico para {ip_teste2} é {trie_ipv6.buscar_longest_prefix_match(ip_teste2)}")  
# Deve retornar "2001:db8::/32"

ip_teste3 = "2001:dead:beef::1"
print(f"O prefixo mais específico para {ip_teste3} é {trie_ipv6.buscar_longest_prefix_match(ip_teste3)}")  
# Deve retornar None (pois não há prefixo correspondente)
