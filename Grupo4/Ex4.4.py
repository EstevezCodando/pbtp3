import ipaddress
import random
import time

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_prefix = False
        self.prefix = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, prefix):
        node = self.root
        for bit in self._prefix_to_bits(prefix):
            if bit not in node.children:
                node.children[bit] = TrieNode()
            node = node.children[bit]
        node.is_end_of_prefix = True
        node.prefix = prefix

    def longest_prefix_match(self, ip):
        node = self.root
        longest_match = None
        for bit in self._ip_to_bits(ip):
            if bit in node.children:
                node = node.children[bit]
                if node.is_end_of_prefix:
                    longest_match = node.prefix
            else:
                break
        return longest_match

    def _prefix_to_bits(self, prefix):
        ip, length = prefix.split('/')
        binary_ip = ''.join(f'{int(octet):08b}' for octet in ip.split('.'))
        return binary_ip[:int(length)]

    def _ip_to_bits(self, ip):
        return ''.join(f'{int(octet):08b}' for octet in ip.split('.'))


def generate_random_prefixes(n):
    prefixes = set()
    while len(prefixes) < n:
        ip = '.'.join(str(random.randint(0, 255)) for _ in range(4))
        prefix_length = random.randint(8, 32)
        prefixes.add(f"{ip}/{prefix_length}")
    return list(prefixes)


def linear_search(ip, prefixes):
    longest_match = None
    longest_length = -1
    for prefix in prefixes:
        network = ipaddress.ip_network(prefix, strict=False)
        if ipaddress.ip_address(ip) in network:
            if network.prefixlen > longest_length:
                longest_match = prefix
                longest_length = network.prefixlen
    return longest_match


def main():
    ip_to_search = "192.168.1.55"
    num_prefixes = 1000
    prefixes = generate_random_prefixes(num_prefixes)

    # Busca linear
    start_time = time.time()
    linear_result = linear_search(ip_to_search, prefixes)
    linear_time = time.time() - start_time

    # Busca com Trie
    trie = Trie()
    for prefix in prefixes:
        trie.insert(prefix)
    
    start_time = time.time()
    trie_result = trie.longest_prefix_match(ip_to_search)
    trie_time = time.time() - start_time

    print(f"Resultado da busca linear: {linear_result} (Tempo: {linear_time:.6f} s)")
    print(f"Resultado da busca com Trie: {trie_result} (Tempo: {trie_time:.6f} s)")

if __name__ == "__main__":
    main()
