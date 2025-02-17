import time
import random
import matplotlib.pyplot as plt
import csv
import psutil
from ipaddress import IPv4Network

# Geração de prefixos IPv4 aleatórios
def gerar_prefixos(qtd):
    prefixos = []
    for _ in range(qtd):
        prefixo = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.0/{random.randint(8, 24)}"
        prefixos.append(prefixo)
    return prefixos

# Implementação de busca linear
def busca_linear(prefixos, ip):
    melhor_prefixo = None  # Inicializa como None
    for prefixo in prefixos:
        rede = IPv4Network(prefixo, strict=False)
        if ip in rede:
            if melhor_prefixo is None or IPv4Network(melhor_prefixo).prefixlen < rede.prefixlen:
                melhor_prefixo = prefixo
    return melhor_prefixo

# Implementação de Trie
class TrieNode:
    def __init__(self):
        self.children = {}  # Dicionário para armazenar os filhos (0 ou 1)
        self.is_end_of_prefix = False  # Indica se este nó representa o fim de um prefixo
        self.prefix = None  # Armazena o prefixo completo (ex: "192.168.1.0/24")

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def inserir(self, prefixo):
        bits = self._prefixo_para_bits(prefixo)  # Converte o prefixo em uma lista de bits
        node = self.root
        for bit in bits:
            if bit not in node.children:
                node.children[bit] = TrieNode()  # Cria um novo nó se o bit não existir
            node = node.children[bit]
        node.is_end_of_prefix = True  # Marca o fim do prefixo
        node.prefix = prefixo  # Armazena o prefixo completo
    
    def buscar_mais_longo(self, ip):
        bits = self._ip_para_bits(ip)  # Converte o IP em uma lista de bits
        node = self.root
        melhor_prefixo = ""
        for bit in bits:
            if bit in node.children:
                node = node.children[bit]
                if node.is_end_of_prefix:
                    melhor_prefixo = node.prefix  # Atualiza o prefixo mais longo encontrado
            else:
                break  # Interrompe a busca se o bit não existir
        return melhor_prefixo

    def _prefixo_para_bits(self, prefixo):
        rede, mascara = prefixo.split('/')  # Separa o IP da máscara
        mascara = int(mascara)  # Converte a máscara para inteiro
        bits = self._ip_para_bits(rede)  # Converte o IP em bits
        return bits[:mascara]  # Retorna apenas os bits relevantes (de acordo com a máscara)

    def _ip_para_bits(self, ip):
        octetos = list(map(int, ip.split('.')))  # Divide o IP em octetos
        bits = []
        for octeto in octetos:
            bits.extend(f"{octeto:08b}")  # Converte cada octeto em 8 bits
        return bits

def construir_trie(prefixos):
    trie = Trie()
    for prefixo in prefixos:
        trie.inserir(prefixo)
    return trie

# Implementação de Patricia Trie
class PatriciaTrieNode:
    def __init__(self):
        self.children = {}
        self.prefix = None
        self.is_end_of_prefix = False

class PatriciaTrie:
    def __init__(self):
        self.root = PatriciaTrieNode()

    def inserir(self, prefixo):
        bits = self._prefixo_para_bits(prefixo)
        node = self.root
        for bit in bits:
            if bit not in node.children:
                node.children[bit] = PatriciaTrieNode()
            node = node.children[bit]
        node.is_end_of_prefix = True
        node.prefix = prefixo

    def buscar_mais_longo(self, ip):
        bits = self._ip_para_bits(ip)
        node = self.root
        melhor_prefixo = ""
        caminho = ""
        for bit in bits:
            if bit in node.children:
                caminho += bit
                node = node.children[bit]
                if node.is_end_of_prefix:
                    melhor_prefixo = node.prefix
            else:
                break
        return melhor_prefixo

    def _prefixo_para_bits(self, prefixo):
        rede, mascara = prefixo.split('/')
        mascara = int(mascara)
        bits = self._ip_para_bits(rede)
        return bits[:mascara]

    def _ip_para_bits(self, ip):
        octetos = list(map(int, ip.split('.')))
        bits = []
        for octeto in octetos:
            bits.extend(f"{octeto:08b}")
        return bits

def construir_patricia(prefixos):
    trie = PatriciaTrie()
    for prefixo in prefixos:
        trie.inserir(prefixo)
    return trie

# Parâmetros
qtd_prefixos = 2000
prefixos = gerar_prefixos(qtd_prefixos)
ip_teste = IPv4Network("192.168.1.55/32").network_address

# Construção das estruturas
trie = construir_trie(prefixos)
patricia = construir_patricia(prefixos)

# Medição de tempos para diferentes quantidades de buscas
num_buscas = [2**i for i in range(1, 11)]
tempos_linear = []
tempos_trie = []
tempos_patricia = []
temperaturas = []

for n in num_buscas:
    ips_teste = [IPv4Network(f"192.168.1.{random.randint(1, 255)}/32").network_address for _ in range(n)]
    
    # Coletar temperatura da CPU antes da execução
    # Coletar temperatura da CPU antes da execução
    temp = None
    sensors = psutil.sensors_temperatures()
    if "coretemp" in sensors:
        for entry in sensors["coretemp"]:
            if hasattr(entry, 'current'):
                temp = entry.current
                break
    temperaturas.append(temp)
    
    # Busca Linear
    inicio = time.time()
    for ip in ips_teste:
        busca_linear(prefixos, ip)
    tempos_linear.append(time.time() - inicio)
    
    time.sleep(5)  # Intervalo para evitar aquecimento
    
    # Busca Trie
    inicio = time.time()
    for ip in ips_teste:
        trie.buscar_mais_longo(ip.compressed)
    tempos_trie.append(time.time() - inicio)
    
    time.sleep(5)  # Intervalo para evitar aquecimento
    
    # Busca Patricia
    inicio = time.time()
    for ip in ips_teste:
        patricia.buscar_mais_longo(ip.compressed)
    tempos_patricia.append(time.time() - inicio)
    
    time.sleep(5)  # Intervalo para evitar aquecimento

# Salvar resultados em CSV
with open("tempos_buscas.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Número de Buscas", "Busca Linear (s)", "Trie (s)", "Patricia (s)", "Temperatura CPU (°C)"])
    for i in range(len(num_buscas)):
        writer.writerow([num_buscas[i], tempos_linear[i], tempos_trie[i], tempos_patricia[i], temperaturas[i]])

# Geração do gráfico
plt.figure(figsize=(10, 6))
plt.plot(num_buscas, tempos_linear, marker='o', label='Busca Linear')
plt.plot(num_buscas, tempos_trie, marker='s', label='Trie')
plt.plot(num_buscas, tempos_patricia, marker='^', label='Patricia')
plt.xscale("log", base=2)
plt.xlabel("Número de buscas")
plt.ylabel("Tempo (s)")
plt.title("Comparação de Desempenho: Busca Linear vs. Trie vs. Patricia")
plt.legend()
plt.grid()
plt.savefig("comparacao_buscas.png")
