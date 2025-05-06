import dns.resolver

def run_dns_enum():
    domain = input("Digite o domínio para enumeração DNS: ").strip().lower()
    record_types = ["A", "MX", "NS", "TXT"]
    for rtype in record_types:
        print(f"\n{rtype} records para {domain}:")
        try:
            answers = dns.resolver.resolve(domain, rtype)
            for r in answers:
                print(f" - {r.to_text()}")
        except Exception as e:
            print(f"   Erro: {e}")