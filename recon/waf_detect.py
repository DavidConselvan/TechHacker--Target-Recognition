import subprocess

def run_waf_detect():
    url = input("Digite a URL alvo (ex.: https://exemplo.com): ")
    try:
        result = subprocess.run(
            ["wafw00f", url], capture_output=True, text=True
        )
        print(result.stdout)
    except FileNotFoundError:
        print("wafw00f não está instalado. Instale com `pip install wafw00f`.")
    except Exception as e:
        print(f"Erro na detecção de WAF: {e}")