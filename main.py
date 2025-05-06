from recon.portscan import run_portscan 
from recon.whois_lookup import run_whois
from recon.dns_enum import run_dns_enum
from recon.subdomain_enum import run_subdomain_enum
from recon.waf_detect import run_waf_detect

TOOLS = {
    '1': ('PortScan', lambda: run_portscan()),
    '2': ('WHOIS Lookup', run_whois),
    '3': ('DNS Enumeration', run_dns_enum),
    '4': ('Subdomain Enumeration', run_subdomain_enum),
    '5': ('WAF Detection', run_waf_detect),
}


def main():
    while True:
        print("\n=== Recon Toolkit ===")
        for key, (name, _) in TOOLS.items():
            print(f"{key}) {name}")
        print("0) Sair")
        choice = input("Selecione uma opção: ")
        if choice == '0':
            break
        tool = TOOLS.get(choice)
        if tool:
            tool[1]()
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()