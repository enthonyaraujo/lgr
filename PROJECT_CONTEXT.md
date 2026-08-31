# CONTEXTO DE PROJETO: LGR Studio (Lugar Geométrico das Raízes)

> Documento de contexto consolidado para alimentação de modelos de IA (ChatGPT, Claude, Codex, etc.).

---

## 1. Visão Geral e Propósito

- **Nome do Projeto:** `LGR Studio` (ou `lgr`)
- **Domínio:** Engenharia de Controle / Sistemas Dinâmicos / Teoria Clássica de Controle
- **Objetivo Principal:** Aplicação interativa que calcula, plota e explica passo a passo o **Lugar Geométrico das Raízes (LGR / Root Locus)** para qualquer Função de Transferência em malha aberta $G(s)H(s) = \frac{N(s)}{D(s)}$.
- **Premissa Fundamental:** Execução rigorosa dos **7 passos clássicos** do traçado do LGR, com cálculo analítico e visualização gráfica com legendas dinâmicas, sem alterar qualquer etapa de cálculo original.

---

## 2. Arquitetura e Stack Tecnológica

A aplicação adota uma arquitetura desacoplada **Electron (Frontend) + Python Bridge (Cálculo Científico)**:

```
┌─────────────────────────────────────────────────────────────┐
│                 ELECTRON FRONTEND (Renderer)                │
│  - HTML5, CSS3 moderno (Dark/Light mode)                   │
│  - KaTeX local para renderização de LaTeX                   │
│  - Visualizador de imagem interativo (Zoom, Pan, Export)    │
│  - Cards do Memorial de Cálculo dos 7 Passos                │
└──────────────────────────────┬──────────────────────────────┘
                               │ IPC (contextBridge)
┌──────────────────────────────▼──────────────────────────────┐
│                  ELECTRON MAIN PROCESS                      │
│  - src/main/main.js & src/preload/preload.js                │
│  - Flags de segurança Linux: --no-sandbox                   │
│  - Spawna python_bridge.py via stdio                        │
└──────────────────────────────┬──────────────────────────────┘
                               │ JSON via stdin / stdout
┌──────────────────────────────▼──────────────────────────────┐
│                    PYTHON SCIENTIFIC ENGINE                 │
│  - python_bridge.py: parse JSON, gera Base64/SVG e métricas │
│  - lgr_engine.py: cálculo exato dos 7 passos clássicos      │
│  - Libs: numpy, scipy, matplotlib, control, sympy           │
└─────────────────────────────────────────────────────────────┘
```

### Frontends Alternativos inclusos:
- **`app.py`:** Web UI moderna via Streamlit com download de PNG 300 DPI e KaTeX.
- **`gui.py`:** Desktop GUI clássica em Tkinter com canvas interativo do Matplotlib.

---

## 3. Os 7 Passos Clássicos do LGR (Regras Matemáticas)

O núcleo do algoritmo (`lgr_engine.py`) segue rigorosamente a convenção clássica (Ogata/Nise/Dorf):

1. **Passo 1, 2 e 3 (Ramos, Polos, Zeros e Simetria):**
   - Polos de malha aberta ($P$ polos, início em $K=0$).
   - Zeros de malha aberta ($Z$ zeros, término em $K \to \infty$).
   - Total de ramos do LGR: $n = \max(P, Z)$.
   - Simetria obrigatória em relação ao eixo real $\sigma$.
   - Segmentos do eixo real pertencem ao LGR se o somatório de polos e zeros reais à direita for ímpar.

2. **Passo 4 (Assíntotas e Centroide):**
   - Se $P > Z$, existem $P - Z$ ramos que tendem ao infinito ao longo de assíntotas.
   - **Centroide:** $\sigma_a = \frac{\sum \text{Polos} - \sum \text{Zeros}}{P - Z}$.
   - **Ângulos das Assíntotas:** $\theta_k = \frac{(2k + 1) \cdot 180^\circ}{P - Z}$, para $k = 0, \dots, P - Z - 1$.

3. **Passo 5 (Pontos de Partida e Retorno - Breakaway / Break-in):**
   - Condição: $\frac{dK}{ds} = 0 \iff N'(s)D(s) - N(s)D'(s) = 0$.
   - As raízes reais da equação diferencial são avaliadas para verificar se pertencem ao LGR e se o ganho correspondente $K_{break} = -\frac{D(s)}{N(s)} > 0$.

4. **Passo 6 (Cruzamento do Eixo Imaginário $j\omega$):**
   - Intersecção dos ramos com o eixo $j\omega$ determinando a frequência crítica $\omega_{cruz}$ e o ganho limite de estabilidade $K_{crit}$.

5. **Passo 7 (Ângulos de Partida $\theta_d$ e Chegada $\theta_a$):**
   - Para polos complexos conjugados $p$: $\theta_d = 180^\circ + \sum \angle(p - z_i) - \sum_{j \neq p} \angle(p - p_j)$.
   - Para zeros complexos $z$: $\theta_a = 180^\circ - \sum \angle(z - z_k) + \sum \angle(z - p_m)$.

---

## 4. Estrutura de Arquivos e Responsabilidades

```
/home/enthony/GitHub/lgr/
├── src/
│   ├── main/
│   │   └── main.js          # Processo principal Electron (IPC, janelas, spawn do Python bridge)
│   ├── preload/
│   │   └── preload.js       # ContextBridge com exposed APIs (calculateLGR, getPresets, saveImage, etc.)
│   └── renderer/
│       ├── index.html       # Layout HTML semântico com Sidebar, Banner KaTeX e Abas
│       ├── styles.css       # Design System completo (Dark/Light mode, Glassmorphism, Zoom UI)
│       ├── app.js           # Lógica do renderer (interação KaTeX, Pan/Zoom, Memorial, Exportação)
│       └── vendor/katex/    # KaTeX offline completo (fontes, scripts e CSS)
├── lgr_engine.py            # Motor matemático com os 7 passos clássicos e parser de Sympy
├── python_bridge.py         # Ponte de comunicação IPC JSON stdio entre Electron e Python
├── app.py                   # Interface alternativa Streamlit
├── gui.py                   # Interface alternativa Desktop Tkinter
├── main.py                  # Launcher unificado em Python
├── package.json             # Manifesto Node/Electron (scripts, electron ^44.1.0, katex)
├── requirements.txt         # Dependências Python (numpy, scipy, matplotlib, control, sympy)
├── run.sh                   # Script executável bash com suporte a flags (--web, --gui, default Electron)
└── README.md                # Documentação do projeto para usuários finais
```

---

## 5. Protocolo de Comunicação IPC (JSON Schema)

### Requisição Electron -> Python (`stdin`):
```json
{
  "action": "calculate",
  "mode": "expr",              // "expr" | "coeffs" | "zpk" | "preset"
  "expr": "(s + 2) / (s * (s + 1) * (s + 4))",
  "num": "1, 2",               // Usado se mode="coeffs"
  "den": "1, 5, 4, 0",          // Usado se mode="coeffs"
  "zeros": "-2",               // Usado se mode="zpk"
  "poles": "0, -1, -4",        // Usado se mode="zpk"
  "k": 1.0,                    // Usado se mode="zpk"
  "preset_key": "Exemplo 1...",// Usado se mode="preset"
  "title": "Lugar Geométrico das Raízes"
}
```

### Resposta Python -> Electron (`stdout`):
```json
{
  "success": true,
  "image": "data:image/png;base64,...",
  "svg": "<svg ...></svg>",
  "latex_exp": "G(s) = \\frac{s + 2}{s^3 + 5s^2 + 4s}",
  "latex_fac": "G(s) = \\frac{s + 2}{s(s + 1)(s + 4)}",
  "detalhes": {
    "P": 3,
    "Z": 1,
    "ramos": 3,
    "polos": [{"re": 0.0, "im": 0.0, "str": "0.00"}, ...],
    "zeros": [{"re": -2.0, "im": 0.0, "str": "-2.00"}],
    "centroide": -1.5,
    "angulos_assintotas": [{"k": 0, "graus": 90.0, "rad": 1.570796}, ...],
    "break_points": [{"s": -0.468, "K": 0.419}],
    "jw_cruzamentos": [{"w": 2.0, "K": 20.0}],
    "angulos_partida": []
  }
}
```

---

## 6. Comandos de Execução e Build

```bash
# Instalação das dependências
npm install
source .venv/bin/activate && pip install -r requirements.txt

# Execução Principal (Electron Desktop com --no-sandbox)
npm start
# ou: ./run.sh

# Execução Alternativa Web (Streamlit)
./run.sh --web

# Execução Alternativa Tkinter
./run.sh --gui
```

---

## 7. Diretrizes para Futuras Modificações / Extensões

1. **Integridade Algorítmica:** Nunca altere as fórmulas nem simplifique os 7 passos da função `lgr_completo` em `lgr_engine.py`.
2. **Ambiente Linux / Electron:** Mantenha a flag `--no-sandbox` para evitar conflitos de permissões do Chromium SUID sandbox em distribuições Linux.
3. **Independência Offline:** O KaTeX e as bibliotecas de plotagem estão 100% locais; novas dependências devem ser empacotadas sem exigir CDNs online.
4. **Novas Features em Potencial:**
   - Adição de cálculo de resposta no tempo (degrau / impulso para um ganho $K$ escolhido).
   - Diagrama de Bode / Nyquist integrado no mesmo painel.
   - Ajuste dinâmico de ganho $K$ via slider em tempo real sobre os ramos do LGR.
