"""
Bridge Python-Electron para o Lugar Geométrico das Raízes (LGR)
Comunicação via JSON stdio.
"""

import sys
import json
import io
import base64
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sympy as sp

from lgr_engine import (
    lgr_completo,
    parse_tf_expression,
    parse_coeffs_str,
    parse_zpk,
    format_complex,
    PRESETS,
)


def get_transfer_function(payload):
    mode = payload.get("mode", "expr")
    
    if mode == "expr":
        expr_str = payload.get("expr", "").strip()
        num, den, latex_exp, latex_fac = parse_tf_expression(expr_str)
        return num, den, latex_exp, latex_fac
        
    elif mode == "coeffs":
        num_str = payload.get("num", "1, 2")
        den_str = payload.get("den", "1, 5, 4, 0")
        num = parse_coeffs_str(num_str)
        den = parse_coeffs_str(den_str)
        s = sp.Symbol('s')
        poly_num = sp.Poly.from_list(num, gens=s)
        poly_den = sp.Poly.from_list(den, gens=s)
        latex_exp = rf"G(s) = \frac{{{sp.latex(poly_num.as_expr())}}}{{{sp.latex(poly_den.as_expr())}}}"
        latex_fac = rf"G(s) = \frac{{{sp.latex(sp.factor(poly_num.as_expr()))}}}{{{sp.latex(sp.factor(poly_den.as_expr()))}}}"
        return num, den, latex_exp, latex_fac

    elif mode == "zpk":
        k_val = float(payload.get("k", 1.0))
        zeros_str = payload.get("zeros", "")
        poles_str = payload.get("poles", "")
        num, den = parse_zpk(zeros_str, poles_str, k_val)
        s = sp.Symbol('s')
        poly_num = sp.Poly.from_list(num, gens=s)
        poly_den = sp.Poly.from_list(den, gens=s)
        latex_exp = rf"G(s) = \frac{{{sp.latex(poly_num.as_expr())}}}{{{sp.latex(poly_den.as_expr())}}}"
        latex_fac = rf"G(s) = \frac{{{sp.latex(sp.factor(poly_num.as_expr()))}}}{{{sp.latex(sp.factor(poly_den.as_expr()))}}}"
        return num, den, latex_exp, latex_fac

    elif mode == "preset":
        preset_key = payload.get("preset_key")
        if preset_key not in PRESETS:
            preset_key = list(PRESETS.keys())[0]
        preset = PRESETS[preset_key]
        num = preset["num"]
        den = preset["den"]
        s = sp.Symbol('s')
        poly_num = sp.Poly.from_list(num, gens=s)
        poly_den = sp.Poly.from_list(den, gens=s)
        latex_exp = rf"G(s) = \frac{{{sp.latex(poly_num.as_expr())}}}{{{sp.latex(poly_den.as_expr())}}}"
        latex_fac = rf"G(s) = \frac{{{sp.latex(sp.factor(poly_num.as_expr()))}}}{{{sp.latex(poly_den.as_expr())}}}"
        return num, den, latex_exp, latex_fac

    raise ValueError(f"Modo desconhecido: {mode}")


def handle_calculate(payload):
    num, den, latex_exp, latex_fac = get_transfer_function(payload)
    title = payload.get("title", "Lugar Geométrico das Raízes")

    # Executa o LGR preservando rigorosamente os 7 passos originais
    fig, ax, detalhes = lgr_completo(num, den, titulo=title, show_plot=False)

    # Gera a imagem Base64 em alta qualidade
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=160, bbox_inches="tight", facecolor="white")
    buf.seek(0)
    img_base64 = "data:image/png;base64," + base64.b64encode(buf.read()).decode("utf-8")
    
    # Gera imagem em formato vetorial SVG
    svg_buf = io.BytesIO()
    fig.savefig(svg_buf, format="svg", bbox_inches="tight", facecolor="white")
    svg_buf.seek(0)
    svg_text = svg_buf.read().decode("utf-8")
    
    plt.close(fig)

    # Serializa detalhes para JSON
    polos_serializados = [
        {"re": float(np.real(p)), "im": float(np.imag(p)), "str": format_complex(p)}
        for p in detalhes["polos"]
    ]
    zeros_serializados = [
        {"re": float(np.real(z)), "im": float(np.imag(z)), "str": format_complex(z)}
        for z in detalhes["zeros"]
    ]
    angulos_partida_serializados = [
        {"polo_str": format_complex(ap["polo"]), "angulo": float(ap["angulo"])}
        for ap in detalhes["angulos_partida"]
    ]

    response_data = {
        "success": True,
        "image": img_base64,
        "svg": svg_text,
        "latex_exp": latex_exp,
        "latex_fac": latex_fac,
        "detalhes": {
            "P": detalhes["P"],
            "Z": detalhes["Z"],
            "ramos": detalhes["ramos"],
            "polos": polos_serializados,
            "zeros": zeros_serializados,
            "centroide": float(detalhes["centroide"]) if detalhes["centroide"] is not None else None,
            "angulos_assintotas": detalhes["angulos_assintotas"],
            "break_points": detalhes["break_points"],
            "jw_cruzamentos": detalhes["jw_cruzamentos"],
            "angulos_partida": angulos_partida_serializados,
        },
    }
    return response_data


def main():
    try:
        raw_input = sys.stdin.read().strip()
        if not raw_input:
            if len(sys.argv) > 1:
                raw_input = sys.argv[1]
            else:
                raw_input = json.dumps({"action": "presets"})

        data = json.loads(raw_input)
        action = data.get("action", "calculate")

        if action == "presets":
            presets_list = []
            for k, v in PRESETS.items():
                presets_list.append({
                    "id": k,
                    "title": k,
                    "expr": v["expr"],
                    "num": v["num"],
                    "den": v["den"],
                    "desc": v["desc"]
                })
            print(json.dumps({"success": True, "presets": presets_list}))
            return

        elif action == "calculate":
            result = handle_calculate(data)
            print(json.dumps(result))
            return

        else:
            print(json.dumps({"success": False, "error": f"Ação desconhecida: {action}"}))

    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))


if __name__ == "__main__":
    main()
