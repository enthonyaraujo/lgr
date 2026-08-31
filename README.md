# LGR Studio — Lugar Geométrico das Raízes

Aplicação responsiva para calcular, visualizar e explicar os **sete passos clássicos do LGR**. A mesma interface funciona no Electron, no navegador do desktop e em celulares ou tablets conectados ao servidor local.

O cálculo científico continua centralizado em Python (`control`, NumPy, SciPy, Matplotlib e SymPy). As interfaces apenas validam entradas, apresentam o LaTeX e exibem os resultados; não redefinem as regras do LGR.

## Recursos

- Renderização matemática offline com KaTeX, incluindo fórmulas estáticas e o memorial gerado dinamicamente.
- Prévia LaTeX durante a digitação, antes de executar o traçado.
- Entradas por:
  - expressão completa: `G(s) = (s + 2)/(s(s + 1)(s + 4))`;
  - numerador e denominador separados;
  - coeficientes polinomiais;
  - polos, zeros e ganho;
  - presets didáticos.
- Escrita flexível com multiplicação implícita (`2s`, `s(s+1)`), `^`, expoentes Unicode (`s²`, `s³`) e símbolos `×`, `·` e `÷`.
- Gráfico com zoom, pan por mouse ou toque e exportação PNG/SVG.
- Tema claro/escuro e layout adaptado para desktop, tablet e celular.
- Aplicação web instalável no dispositivo como PWA; o shell visual é armazenado localmente, enquanto os cálculos continuam dependendo do servidor Python.

## Requisitos

- Node.js 22.12 ou mais recente;
- Python 3.12 ou mais recente;
- Windows, macOS ou Linux.

As dependências declaradas usam projetos ativos e foram auditadas em 31/08/2026. Consulte [requirements.txt](requirements.txt) e [package.json](package.json) para as faixas efetivas.

## Instalação

Linux/macOS:

```bash
npm install
python3 -m venv .venv
source .venv/bin/activate
python -m ensurepip --upgrade
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
npm install
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Executar no desktop

Com o ambiente virtual ativado:

```bash
npm start
```

No Linux/macOS também é possível usar:

```bash
./run.sh
```

O Electron mantém `contextIsolation` e o sandbox do renderer habilitados. Se uma distribuição Linux específica exigir desativar o sandbox, trate isso como configuração local explícita; o projeto não desabilita essa proteção por padrão.

## Executar no navegador

Somente neste computador:

```bash
npm run web
```

Acesse [http://127.0.0.1:8501](http://127.0.0.1:8501).

### Acessar pelo celular ou tablet

Com o computador e o dispositivo móvel na mesma rede:

```bash
npm run web:mobile
```

Descubra o IP local do computador e abra `http://IP-DO-COMPUTADOR:8501` no dispositivo. Não exponha esse servidor diretamente à internet; para acesso externo, coloque-o atrás de HTTPS e de um servidor de produção.

No Linux/macOS, os equivalentes são `./run.sh --web` e `./run.sh --mobile`.

Interfaces legadas continuam disponíveis:

```bash
npm run web:streamlit
npm run gui
```

## Validação e segurança

```bash
npm test
npm audit
uvx pip-audit -r requirements.txt
```

`npm test` executa verificações sintáticas JavaScript e os testes Python. Esses comandos não geram builds.

## Estrutura principal

```text
lgr/
├── src/
│   ├── main/main.js              # Electron e IPC
│   ├── preload/preload.js        # API isolada do renderer
│   └── renderer/
│       ├── index.html            # Interface compartilhada
│       ├── app.js                # Interação, KaTeX, zoom e memorial
│       ├── web-api.js            # Adaptador HTTP para navegadores
│       ├── styles.css            # Design responsivo
│       ├── manifest.webmanifest  # Instalação como PWA
│       ├── sw.js                 # Cache do shell visual
│       └── vendor/katex/         # KaTeX local
├── lgr_engine.py                 # Motor e sete passos clássicos
├── python_bridge.py              # Entrada unificada e serialização
├── web_server.py                 # Servidor HTTP local sem framework adicional
├── app.py                        # Interface alternativa Streamlit
├── gui.py                        # Interface alternativa Tkinter
└── tests/                        # Regressões de entrada e do caso clássico
```

## Regra de integridade

As fórmulas e a sequência de `lgr_completo()` representam a implementação de referência dos sete passos clássicos. Melhorias de interface, portabilidade ou entrada não devem alterar esse procedimento.
