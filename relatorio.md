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

1. **PortScan (`scanme.nmap.org`, portas 1–25)**

   ````
   Iniciando escaneamento em 45.33.32.156 (TCP) - 2025-05-05 22:14:43.870227
   
   Escaneando portas de 1 a 25...

   Resultados do escaneamento:
   ------------------------------------------------------------
   Porta    Estado       Protocolo  Serviço         Banner/SO
   ------------------------------------------------------------
   1        filtered     TCP        Unknown         -
   2        filtered     TCP        Unknown         -
   3        filtered     TCP        Unknown         -
   4        filtered     TCP        Unknown         -
   5        filtered     TCP        Unknown         -
   6        filtered     TCP        Unknown         -
   7        filtered     TCP        Echo            -
   8        filtered     TCP        Unknown         -
   9        filtered     TCP        Discard         -
   10       filtered     TCP        Unknown         -
   11       filtered     TCP        Unknown         -
   12       filtered     TCP        Unknown         -
   13       filtered     TCP        Daytime         -
   14       filtered     TCP        Unknown         -
   15       filtered     TCP        Unknown         -
   16       filtered     TCP        Unknown         -
   17       filtered     TCP        QOTD            -
   18       filtered     TCP        Unknown         -
   19       filtered     TCP        Chargen         -
   20       filtered     TCP        FTP-DATA        -
   21       filtered     TCP        FTP             -
   22       open         TCP        SSH             SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13
   23       filtered     TCP        Telnet          -
   24       filtered     TCP        Unknown         -
   25       open         TCP        SMTP            -
   ------------------------------------------------------------
   ````

2. **WHOIS Lookup**
   ````
   domain_name: GOOGLE.COM
   registrar: MarkMonitor, Inc.
   registrar_url: http://www.markmonitor.com
   reseller: None
   whois_server: whois.markmonitor.com
   referral_url: None
   updated_date: [datetime.datetime(2019, 9, 9, 15, 39, 4), datetime.datetime(2024, 8, 2, 2, 17, 33, tzinfo=datetime.timezone.utc)]
   creation_date: [datetime.datetime(1997, 9, 15, 4, 0), datetime.datetime(1997, 9, 15, 7, 0, tzinfo=datetime.timezone.utc)]  
   expiration_date: [datetime.datetime(2028, 9, 14, 4, 0), datetime.datetime(2028, 9, 13, 7, 0, tzinfo=datetime.timezone.utc)]
   name_servers: ['NS1.GOOGLE.COM', 'NS2.GOOGLE.COM', 'NS3.GOOGLE.COM', 'NS4.GOOGLE.COM']
   status: ['clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited', 'clientTransferProhibited https://icann.org/epp#clientTransferProhibited', 'clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited', 'serverDeleteProhibited https://icann.org/epp#serverDeleteProhibited', 'serverTransferProhibited https://icann.org/epp#serverTransferProhibited', 'serverUpdateProhibited https://icann.org/epp#serverUpdateProhibited', 'clientUpdateProhibited (https://www.icann.org/epp#clientUpdateProhibited)', 'clientTransferProhibited (https://www.icann.org/epp#clientTransferProhibited)', 'clientDeleteProhibited (https://www.icann.org/epp#clientDeleteProhibited)', 'serverUpdateProhibited (https://www.icann.org/epp#serverUpdateProhibited)', 'serverTransferProhibited (https://www.icann.org/epp#serverTransferProhibited)', 'serverDeleteProhibited (https://www.icann.org/epp#serverDeleteProhibited)']
   emails: ['abusecomplaints@markmonitor.com', 'whoisrequest@markmonitor.com']
   dnssec: unsigned
   name: None
   org: Google LLC
   address: None
   city: None
   state: CA
   registrant_postal_code: None
   country: US
   ````

3. **DNS Enumeration**
   ````
   A records para wikimedia.org:
   - 195.200.68.224
   MX records para wikimedia.org:
      Erro: The DNS query name does not exist: wikimedia.org.

   NS records para wikimedia.org:
   - ns0.wikimedia.org.
   - ns1.wikimedia.org.
   - ns2.wikimedia.org.

   TXT records para wikimedia.org:
      Erro: The DNS query name does not exist: wikimedia.org.
   ````

4. **Subdomain Enumeration**

   ````
   Procurando subdomínios em github.com...
   www.github.com -> 20.201.28.151
   test.github.com -> 192.0.2.1
   ````

5. **WAF Detection**

   ````
                     ?              ,.   (   .      )        .      "
            __        ??          ("     )  )'     ,'        )  . (`     '`
      (___()'`;   ???          .; )  ' (( (" )    ;(,     ((  (  ;)  "  )")
      /,___ /`                 _"., ,._'_.,)_(..,( . )_  _' )_') (. _..( ' )
      \\   \\                 |____|____|____|____|____|____|____|____|____|

                                 ~ WAFW00F : v2.3.1 ~
                     ~ Sniffing Web Application Firewalls since 2014 ~

   [*] Checking https://google.com
   [+] Generic Detection results:
   [-] No WAF detected by the generic detection
   [~] Number of requests: 7

   ````

   ````

                     ?              ,.   (   .      )        .      "
               __        ??          ("     )  )'     ,'        )  . (`     '`
         (___()'`;   ???          .; )  ' (( (" )    ;(,     ((  (  ;)  "  )")
         /,___ /`                 _"., ,._'_.,)_(..,( . )_  _' )_') (. _..( ' )
         \\   \\                 |____|____|____|____|____|____|____|____|____|

                                    ~ WAFW00F : v2.3.1 ~
                        ~ Sniffing Web Application Firewalls since 2014 ~

      [*] Checking https://www.shopify.com
      [+] The site https://www.shopify.com is behind Cloudflare (Cloudflare Inc.) WAF.
      [~] Number of requests: 2
   ````

---
