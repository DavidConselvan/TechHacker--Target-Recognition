import whois

def run_whois():
    domain = input("Digite o domínio para WHOIS lookup: ")
    try:
        w = whois.whois(domain)
        for key, value in w.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Erro no WHOIS: {e}")