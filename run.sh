#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Ativa o ambiente virtual Python se existir
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Se receber flag --web, inicia o Streamlit
if [ "$1" == "--web" ]; then
    streamlit run app.py
# Se receber flag --gui, inicia a GUI Tkinter clássica
elif [ "$1" == "--gui" ]; then
    python3 gui.py
# Se receber flag --cli, inicia o menu de opções
elif [ "$1" == "--cli" ]; then
    python3 main.py
# Padrão: Inicia a Interface Moderna do Electron com --no-sandbox
else
    npx electron . --no-sandbox
fi
