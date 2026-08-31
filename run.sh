#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Ativa o ambiente virtual Python se existir
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

case "${1:-}" in
    --web)
        python web_server.py
        ;;
    --mobile)
        python web_server.py --host 0.0.0.0
        ;;
    --streamlit)
        streamlit run app.py
        ;;
    --gui)
        python gui.py
        ;;
    --cli)
        python main.py
        ;;
    *)
        npm start
        ;;
esac
