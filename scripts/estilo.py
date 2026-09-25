"""Estilo visual compartilhado do perfil (cor de destaque sobre fundo escuro).

Traz a paleta, as fontes embutidas (Nunito e JetBrains Mono, do Google Fonts,
com só os caracteres usados) e os ícones do Material Symbols e do Simple Icons.
"""
import base64
import re
import urllib.parse
import urllib.request
from html import unescape
from xml.sax.saxutils import escape

import os

# Cada paleta define os mesmos papéis de cor. Escolha com a variável PALETA.
PALETAS = {
    "roxo": dict(borda="#2a1a4a", escuro="#1e1033", tile="#2a1250", tile2="#140a26", meio="#3b1d6e", traco="#5b21b6",
                 acento_escuro="#7c3aed", acento="#a855f7", acento_claro="#c084fc", claro="#e9d5ff", branco="#f5f3ff", extra="#d8b4fe"),
    "esmeralda": dict(borda="#123a30", escuro="#052e24", tile="#0b3d30", tile2="#06201a", meio="#065f46", traco="#047857",
                      acento_escuro="#059669", acento="#10b981", acento_claro="#34d399", claro="#d1fae5", branco="#ecfdf5", extra="#6ee7b7"),
    "ambar": dict(borda="#3a2a12", escuro="#2b1a05", tile="#3a2508", tile2="#1f1404", meio="#78350f", traco="#b45309",
                  acento_escuro="#d97706", acento="#f59e0b", acento_claro="#fbbf24", claro="#fef3c7", branco="#fffbeb", extra="#fcd34d"),
    "ciano": dict(borda="#12343c", escuro="#042f36", tile="#0a3a44", tile2="#05232a", meio="#155e75", traco="#0e7490",
                  acento_escuro="#0891b2", acento="#06b6d4", acento_claro="#22d3ee", claro="#cffafe", branco="#ecfeff", extra="#67e8f9"),
    "coral": dict(borda="#3d1a22", escuro="#2e0f16", tile="#3d1520", tile2="#200a10", meio="#881337", traco="#be123c",
                  acento_escuro="#e11d48", acento="#fb7185", acento_claro="#fda4af", claro="#ffe4e6", branco="#fff1f2", extra="#fecdd3"),
    "lima": dict(borda="#262d14", escuro="#1a1f0a", tile="#232a0e", tile2="#12160a", meio="#3f6212", traco="#4d7c0f",
                 acento_escuro="#65a30d", acento="#a3e635", acento_claro="#bef264", claro="#ecfccb", branco="#f7fee7", extra="#d9f99d"),
}
NOME_PALETA = os.environ.get("PALETA", "esmeralda")
P = PALETAS[NOME_PALETA]

BG = "#0d1117"
SUAVE = "#9ca3af"
BORDA = P["borda"]
ACENTO = P["acento"]
ACENTO_CLARO = P["acento_claro"]
ACENTO_ESCURO = P["acento_escuro"]
CLARO = P["claro"]
ESCALA = [P["acento"], P["acento_claro"], P["acento_escuro"], P["claro"], P["traco"], P["extra"], P["meio"], P["branco"]]

SANS = os.environ.get("FONTE_TEXTO", "Space Grotesk")
MONO = os.environ.get("FONTE_CODIGO", "VT323")
F = f"'{SANS}', 'Segoe UI', Ubuntu, sans-serif"
M = f"'{MONO}', Consolas, Menlo, monospace"
# Fonte dos títulos (nome no banner, títulos dos cards). Fontes largas usam um fator menor.
TITULO = os.environ.get("FONTE_TITULO", "Press Start 2P")
T = f"'{TITULO}', {F}"
_FATORES = {"Press Start 2P": 0.64, "Silkscreen": 0.7, "Orbitron": 0.85, "Audiowide": 0.9, "Monoton": 0.85, "Bungee": 0.85}
FATOR_TITULO = _FATORES.get(TITULO, 1.0)


FATOR_MONO = {"VT323": 1.3}.get(MONO, 1.0)


def tam(px):
    """Tamanho de fonte de título ajustado para a fonte escolhida."""
    return f"{px * FATOR_TITULO:.1f}px"


def tam_mono(px):
    """Tamanho da fonte de código ajustado (VT323 é menor que as outras)."""
    return f"{px * FATOR_MONO:.1f}px"
_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"


def _get(url, binario=False):
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        dados = r.read()
    return dados if binario else dados.decode()


def fontes(texto_sans="", texto_mono=""):
    """@font-face com um subconjunto das fontes contendo só os caracteres usados."""
    regras = ""
    familias = [(SANS, texto_sans), (MONO, texto_mono)]
    if TITULO != SANS:
        familias.append((TITULO, texto_sans))
    for familia, texto in familias:
        if not texto:
            continue
        chars = urllib.parse.quote("".join(sorted(set(texto + " "))))
        base = f"https://fonts.googleapis.com/css2?family={urllib.parse.quote(familia)}"
        for pesos in ("400;600;700;800", "400;500;600;700", "400;700", "400"):
            try:
                css = _get(f"{base}:wght@{pesos}&text={chars}")
                break
            except Exception:
                css = ""
        for peso, src in re.findall(r"font-weight:\s*(\d+);.*?url\((.+?)\)", css, flags=re.S):
            try:
                b64 = base64.b64encode(_get(src, binario=True)).decode()
            except Exception as erro:
                print("aviso: fonte não embutida", familia, erro)
                continue
            regras += (
                f"@font-face{{font-family:'{familia}';font-weight:{peso};"
                f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
            )
    return regras


_icones = {}


def icone(nome, x, y, tamanho, cor=None, cheio=False):
    """Ícone do Material Symbols (Google) posicionado em (x, y)."""
    cor = cor or ACENTO_CLARO
    chave = (nome, cheio)
    if chave not in _icones:
        estilo = "fill1" if cheio else "default"
        svg_txt = _get(f"https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsrounded/{nome}/{estilo}/24px.svg")
        _icones[chave] = "".join(re.findall(r'<path d="[^"]+"/>', svg_txt))
    s = tamanho / 960
    return f'<g transform="translate({x} {y}) scale({s:.5f}) translate(0 960)" fill="{cor}">{_icones[chave]}</g>'


_logos = {}


def logo(slug, x, y, tamanho, cor=None):
    """Logo do Simple Icons; retorna None se não existir."""
    if slug not in _logos:
        try:
            svg_txt = _get(f"https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg")
            _logos[slug] = re.search(r'<path d="([^"]+)"', svg_txt).group(1)
        except Exception:
            _logos[slug] = None
    if not _logos[slug]:
        return None
    cor = cor or CLARO
    s = tamanho / 24
    return f'<path transform="translate({x} {y}) scale({s:.4f})" fill="{cor}" d="{_logos[slug]}"/>'


def svg(w, h, conteudo, rotulo, css="", texto_mono=""):
    """Monta o SVG final embutindo as fontes com os caracteres usados."""
    texto = unescape("".join(re.findall(r">([^<>]+)</text>", conteudo)))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(rotulo)}">'
        f"<style>{fontes(texto, texto_mono)}{css}</style>{conteudo}</svg>\n"
    )


def txt(s):
    return escape(s)
