# 📈 LGR Studio — Interface Desktop Moderna em Electron & Python

Interface desktop interativa e moderna construída com **Electron**, **HTML5/CSS3/JavaScript**, **KaTeX** e motor de cálculo científico em **Python** (`control`, `numpy`, `matplotlib`, `sympy`).

O aplicativo executa rigorosamente os **7 passos clássicos** da análise do Lugar Geométrico das Raízes (LGR) de sistemas de controle em malha fechada sem alterar qualquer etapa de cálculo ou plotagem do algoritmo original.

---

## ✨ Destaques da Nova Interface (Electron)

- **🎨 Design Moderno & Premium:**
  - Interface escura por padrão (com alternador de Tema Claro/Escuro).
  - Banner de equações com renderização instantânea em **LaTeX via KaTeX** ($G(s) = \frac{N(s)}{D(s)}$ expandida e fatorada).
  - Painel de controle responsivo com chips de exemplos rápidos.
  - Badges de contadores em tempo real (Polos, Zeros, Ramos, Centroide).

- **🔍 Visualizador do Gráfico do LGR:**
  - Zoom interativo (com roda do mouse ou botões de zoom in/out).
  - Arraste livre da imagem (pan).
  - Exportação direta em **PNG em Alta Resolução (300 DPI)** e **Vetorial SVG**.
  - Botão de **Copiar Gráfico para a Área de Transferência**.

- **📑 Memorial de Cálculo dos 7 Passos Clássicos:**
  1. **Passos 1, 2 e 3:** Polos ($p_i$), Zeros ($z_i$), Total de Ramos ($n = \max(P, Z)$) e Simetria.
  2. **Passo 4:** Centroide ($\sigma_a$) e Ângulos das Assíntotas ($\theta_k$).
  3. **Passo 5:** Pontos de Partida e Retorno no eixo real (Break-in / Breakaway) via $\frac{dK}{ds} = 0$ e Ganho $K_{break}$.
  4. **Passo 6:** Cruzamento com o Eixo $j\omega$ e Ganho Crítico de Estabilidade $K_{crit}$.
  5. **Passo 7:** Ângulos de Partida ($\theta_d$) de polos complexos e Chegada ($\theta_a$) em zeros complexos.

- **🎯 Modos de Entrada Flexíveis:**
  - **✍️ Expressão Algébrica / Simbólica:** Notação livre como `(s + 2) / (s * (s + 1) * (s + 4))` ou `1 / (s*(s^2 + 2s + 2))`.
  - **🔢 Coeficientes Polinomiais:** Coeficientes diretos (ex: `1, 2` e `1, 5, 4, 0`).
  - **🎯 Polos, Zeros e Ganho:** Zeros, polos (reais e complexos) e ganho escalar $K$.
  - **📚 Presets Clássicos:** Exemplos de livros consagrados (Ogata, Nise, Dorf) carregados com 1 clique.

---

## 🚀 Como Executar

### 1. Pré-requisitos e Instalação

Certifique-se de ter **Node.js** (v18+) e **Python** (v3.10+) instalados.

```bash
# 1. Instalar dependências Node (Electron & KaTeX)
npm install

# 2. Criar ambiente virtual e instalar dependências Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

### 2. Iniciar o Aplicativo

#### 🌟 Interface Desktop Electron (Recomendada):
```bash
npm start
```
*ou:*
```bash
./run.sh
```

#### 🌐 Interface Web Alternativa (Streamlit):
```bash
./run.sh --web
```

#### 🖥️ Interface Tkinter Clássica:
```bash
./run.sh --gui
```

---

## 📁 Estrutura do Projeto

```
lgr/
├── src/
│   ├── main/
│   │   └── main.js           # Processo Principal do Electron (IPC & spawn Python)
│   ├── preload/
│   │   └── preload.js        # ContextBridge seguro para IPC
│   └── renderer/
│       ├── index.html        # Estrutura visual da aplicação
│       ├── styles.css        # Design System moderno, Dark/Light mode
│       ├── app.js            # Lógica reativa, KaTeX, Zoom/Pan, Exportação
│       └── vendor/
│           └── katex/        # KaTeX local offline para fórmulas matemáticas
├── lgr_engine.py             # Motor dos 7 passos clássicos do LGR e Sympy
├── python_bridge.py          # Bridge de comunicação JSON stdio Electron-Python
├── app.py                    # Interface Web Streamlit
├── gui.py                    # Interface Tkinter Desktop
├── package.json              # Dependências e scripts Electron
├── requirements.txt          # Dependências Python (control, numpy, matplotlib, sympy)
└── run.sh                    # Launcher executável unificado
```
