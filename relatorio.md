# TechHacker--Target-Recognition

### 1. Além do PortScan, quais são as 5 ferramentas mais úteis para reconhecimento em um pentest?

Algumas das ferramentas mais úteis para um pentest completo são:

* **WAFW00F**

  Detecta e identifica Web Application Firewalls, como Cloudflare, que protegem um website, realizando uma análise de respostas HTTP. Por exemplo, ao detectar um WAF na frente de uma aplicação, o tester pode ajustar ataques (evitar assinaturas bloqueadas) ou buscar bypasses específicos.

* **theHarvester**

  Coleta e-mails, subdomínios e nomes de hosts a partir de fontes OSINT, com informações públicas como o Google, Bing, LinkedIn. Um exemplo seria agrupar endereços de e-mail válidos dos hosts de uma empresa antes de realizar um ataque de phishing direcionado.

* **Amass**

  Framework utilizado para enumeração de subdomínios que combina fontes passivas como certificados públicos, arquivos WHOIS e brute-force ativo, para revelar subdomínios escondidos internamente na rede, com objetivo de ampliar o escopo de testes.

* **Censys**

  Plataforma de visibilidade da Internet que faz varreduras regulares em toda a rede, permitindo buscas por certificados TLS, banners e configuração de serviços expostos, ideal para mapear rapidamente superfícies de ataque.

* **Shodan**

  Permite descobrir e analisar dispositivos IoT e serviços expostos na Internet (câmeras, impressoras, entre outros dispositivos conectados à rede), mapeando banners e metadados. Ex.: localizar câmeras vulneráveis conectadas em redes de empresas para encontrar possíveis superfícies de ataque em sistemas de vigilância.

---

### 2. Diferenças entre Scanner SYN e TCP Connect Scan

* **SYN Scan (“half-open”, `-sS` no Nmap)**

  1. Envia pacote **SYN**;

  2. Se recebe **SYN-ACK**, considera a porta “open” e envia **RST** (não completa o handshake);

  3. Se recebe **RST**, considera “closed”.

  * **Vantagens:**

    * Mais rápido e discreto, pois não gera registros completos no alvo.
    * Requer privilégios de root/raw sockets.
  * **Uso ideal:** redes protegidas por IDS/IPS, quando se deseja minimizar logs no servidor alvo.

* **TCP Connect Scan (`-sT`)**

  1. Usa a chamada de sistema `connect()` do SO, completando o **3-way handshake** (SYN, SYN-ACK, ACK);

  2. Fecha a conexão normalmente (FIN).

  * **Vantagens:**

    * Funciona sem privilégios especiais.
    * Mais compatível em ambientes restritos a raw sockets.
  * **Uso ideal:** quando não há acesso a privilégios de root ou em redes menos monitoradas, mas gera mais logs no servidor alvo.

---

### 3. Técnicas de evasão de IPS durante o reconhecimento

1. **Fragmentação de pacotes**

   Divide o payload em vários fragmentos menores para que o IPS não consiga corresponder ao padrão completo de assinatura, reduzindo a chance de detecção por assinatura, mas podendo aumentar a complexidade e tempo.

2. **Variação de timing (“slow scan”)**

   Espalha verificações em grandes intervalos ou horários aleatórios, evitando gatilhos de taxa de detecção, mas aumentando significativamente o tempo total de reconhecimento.

3. **Uso de decoys**

   Incluir IPs falsos fontes simultâneos com o IP real (`--decoy` no Nmap), confundindo o IPS/IDS ao gerar múltiplas origens para diminuir o foco em um único scanner.

4. **IP spoofing e proxies**

   Encaminhar tráfego via VPNs, TOR ou múltiplos servidores proxy; ou falsificar endereços IP de origem, ocultando a verdadeira origem, mas depende da resposta do servidor, um spoofing puro inviabiliza recebimento de resposta.

5. **Manipulação de flags e opções TCP**

   Enviar pacotes com flags incomuns (NULL, FIN, Xmas scan) ou ajustar campos TTL e janela TCP, explorando lacunas na detecção de assinaturas, porém, nem todos os sistemas reagem a pacotes fora do padrão.

6. **Encriptação/Túnel SSL**

   Encapsular sondagens dentro de um túnel TLS (stunnel, SSH) para mascarar conteúdo, fazendo com que IPS sem inspeção profunda não detecte o conteúdo, porém introduzindo overhead de configuração e latência.

---

## Documentação Técnica e Manual do Usuário

1. **Instalação**

   * Requisitos: Python 3.8+, ambiente virtual.
   * Comandos:

     ```bash
     python3 -m venv venv
     source venv/bin/activate   # Linux/macOS
     .\venv\Scripts\Activate.ps1  # Windows PowerShell
     pip install -r requirements.txt
     ```
2. **Estrutura do Projeto**

   ```plaintext
   TechHacker--Target-Recognition/
   ├── recon/
   │   ├── portscan.py
   │   ├── whois_lookup.py
   │   ├── dns_enum.py
   │   ├── subdomain_enum.py
   │   └── waf_detect.py
   └── main.py
   ```
3. **Uso**
   Execute o menu interativo com:

   ```bash
   python main.py
   ```

   Escolha a ferramenta (1–5) e forneça os parâmetros solicitados.

---

## Descrição da Arquitetura e Decisões de Design

* **Modularidade**: cada funcionalidade em `recon/*.py` isola responsabilidades e facilita manutenção.
* **CLI Interativo**: `main.py` oferece menu uniforme para todas as ferramentas, evitando repetição de código.
* **Multithreading em PortScan**: até 100 threads paralelas para reduzir tempo de escaneamento.
* **Dependências externas**:

  * `dnspython`, `python-whois` para protocolos DNS e WHOIS.
  * `wafw00f` via subprocesso para fingerprint de WAF.
* **Validações de Input**: em cada `run_*()` há checagem de formato e tratamento de erros, garantindo robustez.

---

## Análise das Ferramentas Integradas

| Módulo              | Pontos Fortes                                 | Limitações                           |
| ------------------- | --------------------------------------------- | ------------------------------------ |
| **PortScan**        | Paralelismo, banner grabbing, TCP/UDP         | “Filtered” em firewalls rigorosos    |
| **WHOIS Lookup**    | Campos abrangentes (registrar, datas)         | Timeout em domínios pequenos         |
| **DNS Enumeration** | Atenção a A, MX, NS, TXT                      | NXDOMAIN para tipos ausentes         |
| **Subdomain Enum.** | Simplicidade e rapidez                        | Depende da wordlist                  |
| **WAF Detection**   | Identifica WAFs conhecidos (Cloudflare, etc.) | Falha em infra própria (ex.: Google) |

---

## Exemplos de Resultado dos Testes Realizados

1. **PortScan (`scanme.nmap.org`, portas 1–100)**

   * Open: 22 (SSH), 80 (HTTP), 9929 (nping-echo)
   * Filtered: demais portas

2. **WHOIS Lookup**

   * Teste: `google.com`
   * Campos retornados: registrar, creation\_date, expiration\_date, name\_servers, etc.

3. **DNS Enumeration**

   * `google.com`: A record(172.217.29.46), NS(ns2.google.com., ns1.google.com.,...).
   * `wikipedia.org`: A record, NS e TXT; MX ausente (NXDOMAIN).
   * `wikimedia.org.`: A(195.200.68.224), NS(ns0.wikimedia.org.,...).

4. **Subdomain Enumeration**

   * `github.com`: 
        - www.github.com -> 20.201.28.151
        - test.github.com -> 192.0.2.1

5. **WAF Detection**

   * `google.com`: sem WAF detectado.
   * `shopify.com`: Cloudflare WAF detectado.

---
