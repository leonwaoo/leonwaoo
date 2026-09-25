"""Estilo visual compartilhado (inspirado em Frutiger Aero).

Paleta em azul-céu, painéis de vidro com brilho, bolhas e fontes embutidas
(Nunito e JetBrains Mono, do Google Fonts) para que os SVGs fiquem iguais
em qualquer navegador.
"""
import base64
import re
import urllib.parse
import urllib.request
from xml.sax.saxutils import escape

# ------------------------------------------------------------------ paleta
CEU_TOPO = "#f2faff"
CEU_BASE = "#cdeeff"
BORDA = "#8ccff3"
TITULO = "#0b4f8a"
TEXTO = "#245e8f"
SUAVE = "#5b86ad"
AQUA_1 = "#7fe6ff"
AQUA_2 = "#1e9bff"
AQUA_3 = "#0a6fd6"
VERDE = "#4fd27a"
BRANCO = "#ffffff"
ESCALA = ["#0a6fd6", "#1e9bff", "#38c6ff", "#7fe6ff", "#4fd27a", "#9fdcff", "#0b4f8a", "#bfeaff"]

SANS = "Nunito"
MONO = "JetBrains Mono"
_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"


def _get(url, binario=False):
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        dados = r.read()
    return dados if binario else dados.decode()


def fontes(texto_sans="", texto_mono=""):
    """@font-face com subconjunto das fontes contendo só os caracteres usados."""
    regras = ""
    for familia, texto, eixo in [(SANS, texto_sans, "wght@400..900"), (MONO, texto_mono, "wght@400..700")]:
        chars = "".join(sorted(set(texto + " ")))
        if not texto:
            continue
        url = (
            "https://fonts.googleapis.com/css2?family="
            + urllib.parse.quote(familia)
            + ":"
            + eixo
            + "&text="
            + urllib.parse.quote(chars)
        )
        try:
            css = _get(url)
            src = re.search(r"url\((.+?)\)", css).group(1)
            b64 = base64.b64encode(_get(src, binario=True)).decode()
            regras += (
                f"@font-face{{font-family:'{familia}';font-weight:100 900;"
                f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
            )
        except Exception as erro:  # sem rede: cai nas fontes do sistema
            print("aviso: fonte não embutida", familia, erro)
    return regras


def pilha(familia):
    if familia == MONO:
        return f"'{MONO}', Consolas, Menlo, monospace"
    return f"'{SANS}', 'Segoe UI', Ubuntu, sans-serif"


# ------------------------------------------------------------------ ícones
_icones = {}


def icone(nome, x, y, tamanho, cor=BRANCO):
    """Ícone do Material Symbols (Google) posicionado em (x, y)."""
    if nome not in _icones:
        svg = _get(f"https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsrounded/{nome}/default/24px.svg")
        _icones[nome] = "".join(re.findall(r'<path d="[^"]+"/>', svg))
    s = tamanho / 960
    return f'<g transform="translate({x} {y}) scale({s:.5f}) translate(0 960)" fill="{cor}">{_icones[nome]}</g>'


_logos = {}


def logo(slug, x, y, tamanho, cor=BRANCO):
    """Logo do Simple Icons; retorna None se não existir."""
    if slug not in _logos:
        try:
            svg = _get(f"https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg")
            _logos[slug] = re.search(r'<path d="([^"]+)"', svg).group(1)
        except Exception:
            _logos[slug] = None
    if not _logos[slug]:
        return None
    s = tamanho / 24
    return f'<path transform="translate({x} {y}) scale({s:.4f})" fill="{cor}" d="{_logos[slug]}"/>'


# ------------------------------------------------------------------ blocos
def defs_base(p=""):
    """Gradientes do painel de vidro, do brilho e das bolhas (prefixo p)."""
    return f"""
<linearGradient id="{p}ceu" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{CEU_TOPO}"/><stop offset="1" stop-color="{CEU_BASE}"/></linearGradient>
<linearGradient id="{p}brilho" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="{p}bolha" cx=".35" cy=".3" r=".75"><stop stop-color="{AQUA_1}"/><stop offset=".55" stop-color="{AQUA_2}"/><stop offset="1" stop-color="{AQUA_3}"/></radialGradient>
<radialGradient id="{p}bolhaVerde" cx=".35" cy=".3" r=".75"><stop stop-color="#b8f5c9"/><stop offset=".55" stop-color="{VERDE}"/><stop offset="1" stop-color="#1f9d4f"/></radialGradient>
<radialGradient id="{p}deco" cx=".35" cy=".3" r=".7"><stop stop-color="#fff" stop-opacity=".95"/><stop offset=".6" stop-color="{AQUA_1}" stop-opacity=".35"/><stop offset="1" stop-color="{AQUA_2}" stop-opacity=".15"/></radialGradient>
<filter id="{p}sombra" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="{AQUA_3}" flood-opacity=".22"/></filter>
"""


def painel(w, h, p="", r=18, bolhas=True):
    """Painel de vidro azul-céu com brilho no topo e bolhas decorativas."""
    deco = ""
    if bolhas:
        deco = (
            f'<circle cx="{w - 34}" cy="{h - 26}" r="16" fill="url(#{p}deco)"/>'
            f'<circle cx="{w - 62}" cy="{h - 14}" r="7" fill="url(#{p}deco)"/>'
            f'<circle cx="{w - 18}" cy="{h - 52}" r="5" fill="url(#{p}deco)"/>'
        )
    return (
        f'<rect x="4" y="3" width="{w - 8}" height="{h - 10}" rx="{r}" fill="url(#{p}ceu)" stroke="{BORDA}" stroke-width="1.5" filter="url(#{p}sombra)"/>'
        f'<rect x="6" y="5" width="{w - 12}" height="{(h - 10) * 0.45:.1f}" rx="{r - 2}" fill="url(#{p}brilho)"/>'
        + deco
    )


def bolha(cx, cy, r, nome_icone, p="", verde=False):
    """Bolha brilhante com ícone branco no centro."""
    grad = f"{p}bolhaVerde" if verde else f"{p}bolha"
    t = r * 1.05
    return (
        f'<circle cx="{cx}" cy="{cy + 2}" r="{r}" fill="{AQUA_3}" opacity=".18"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{grad})" stroke="#ffffff" stroke-opacity=".7" stroke-width="1.5"/>'
        + icone(nome_icone, cx - t / 2, cy - t / 2, t)
        + f'<ellipse cx="{cx}" cy="{cy - r * 0.5:.1f}" rx="{r * 0.68:.1f}" ry="{r * 0.36:.1f}" fill="#fff" opacity=".45"/>'
    )


def svg(w, h, conteudo, rotulo, css="", texto_mono=""):
    """Monta o SVG final embutindo só os caracteres usados nas fontes."""
    from html import unescape
    texto = unescape("".join(re.findall(r">([^<>]+)</text>", conteudo)))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(rotulo)}">'
        f"<style>{fontes(texto, texto_mono)}{css}</style>{conteudo}</svg>\n"
    )


def txt(s):
    return escape(s)
