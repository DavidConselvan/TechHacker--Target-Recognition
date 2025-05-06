import dns.resolver

WORDLIST = ["www", "mail", "ftp", "test", "dev", "stage"]

def run_subdomain_enum():
    domain = input("Digite o domínio para enumeração de subdomínios: ")
    print(f"Procurando subdomínios em {domain}...")
    for sub in WORDLIST:
        host = f"{sub}.{domain}"
        try:
            answers = dns.resolver.resolve(host, 'A')
            for r in answers:
                print(f"{host} -> {r.to_text()}")
        except Exception:
            pass