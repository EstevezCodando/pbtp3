import ipaddress
import random
import time
import matplotlib
matplotlib.use('Agg')  # Usa um backend não interativo
import matplotlib.pyplot as plt

# Gerando 1200 prefixos IPv4 aleatórios
def gerar_prefixos_ipv4(qtd=1200):
    prefixos = set()
    while len(prefixos) < qtd:
        ip = f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.0/{random.choice([8, 16, 24])}"
        prefixos.add(ip)
    return list(prefixos)

# Implementação de busca linear
def busca_linear(prefixos, ip):
    ip_addr = ipaddress.ip_address(ip)
    melhor_prefixo = None
    maior_prefixlen = -1

    for prefixo in prefixos:
        rede = ipaddress.ip_network(prefixo, strict=False)
        if ip_addr in rede and rede.prefixlen > maior_prefixlen:
            melhor_prefixo = prefixo
            maior_prefixlen = rede.prefixlen

    return melhor_prefixo

# Implementação da Patricia Trie para IPv4
class NodoPatricia:
    def __init__(self, prefixo=None):
        self.prefixo = prefixo
        self.filhos = {}

class PatriciaTrie:
    def __init__(self):
        self.raiz = NodoPatricia()

    def inserir_prefixo(self, prefixo):
        rede = ipaddress.ip_network(prefixo, strict=False)
        bits = self._ip_para_bits(rede.network_address, rede.prefixlen)

        nodo_atual = self.raiz
        while bits:
            if bits in nodo_atual.filhos:
                nodo_atual = nodo_atual.filhos[bits]
                break
            else:
                novo_nodo = NodoPatricia(prefixo=str(rede))
                nodo_atual.filhos[bits] = novo_nodo
                break

    def buscar_longest_prefix_match(self, ip):
        ip = ipaddress.ip_address(ip)
        bits = self._ip_para_bits(ip, 32)

        nodo_atual = self.raiz
        melhor_correspondencia = None

        while bits:
            if nodo_atual.prefixo:
                melhor_correspondencia = nodo_atual.prefixo
            for prefixo_armaz in nodo_atual.filhos:
                if bits.startswith(prefixo_armaz):
                    nodo_atual = nodo_atual.filhos[prefixo_armaz]
                    bits = bits[len(prefixo_armaz):]
                    break
            else:
                break

        return melhor_correspondencia

    def _ip_para_bits(self, ip, bits):
        return bin(int(ip))[2:].zfill(bits)

# Configuração do experimento
prefixos = gerar_prefixos_ipv4()
trie = PatriciaTrie()
for p in prefixos:
    trie.inserir_prefixo(p)

# Número de buscas a serem realizadas
buscas = [2, 4, 8, 16, 32,64,128,256,512,1024]
tempos_linear = []
tempos_trie = []

for num_buscas in buscas:
    ips_teste = [f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}" for _ in range(num_buscas)]

    # Tempo para busca linear
    inicio = time.time()
    for ip in ips_teste:
        busca_linear(prefixos, ip)
    tempos_linear.append(time.time() - inicio)

    # Tempo para busca na Patricia Trie
    inicio = time.time()
    for ip in ips_teste:
        trie.buscar_longest_prefix_match(ip)
    tempos_trie.append(time.time() - inicio)

# Plotando os resultados
plt.figure(figsize=(10, 5))
plt.plot(buscas, tempos_linear, marker='o', label="Busca Linear")
plt.plot(buscas, tempos_trie, marker='s', label="Trie Patricia")
plt.xlabel("Número de Buscas")
plt.ylabel("Tempo (s)")
plt.title("Comparação de Desempenho: Busca Linear vs. Trie Patricia")

plt.legend()
plt.grid()
plt.savefig("comparacao_busca_ipv4.png")