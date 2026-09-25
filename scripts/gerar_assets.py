"""Gera os elementos visuais do perfil em SVG.

- intro.svg: cartão de apresentação animado (estilo terminal)
- skill-*.svg: cards de áreas de atuação com ícone
- btn-*.svg: botões de contato
- divisor.svg: divisor animado entre seções

Os ícones vêm do Material Symbols (Google), baixados no momento da geração.
"""
import os
import re
import urllib.request
from xml.sax.saxutils import escape

OUT = "dist"
BG = "#0d1117"
BORDER = "#2a1a4a"
ROXO = "#a855f7"
ROXO_CLARO = "#c084fc"
LILAS = "#e9d5ff"
MUTED = "#9ca3af"
SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Sans-Serif"
MONO = "'Fira Code', 'JetBrains Mono', Consolas, Menlo, monospace"

ICON_URL = "https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsrounded/{}/default/24px.svg"
_cache = {}


def icone(nome, x, y, tamanho, cor):
    """Retorna o ícone do Material Symbols posicionado em (x, y)."""
    if nome not in _cache:
        with urllib.request.urlopen(ICON_URL.format(nome)) as r:
            svg = r.read().decode()
        _cache[nome] = "".join(re.findall(r'<path d="[^"]+"/>', svg))
    escala = tamanho / 960
    return (
        f'<g transform="translate({x} {y}) scale({escala:.5f}) translate(0 960)" fill="{cor}">'
        f"{_cache[nome]}</g>"
    )


def salvar(nome, conteudo):
    with open(os.path.join(OUT, nome), "w", encoding="utf-8") as f:
        f.write(conteudo)
    print("gerado", nome)


# ---------------------------------------------------------------- cartão
LINHAS = [
    ("whoami", "Leon Daniel Corrêa"),
    ("cat foco.txt", "Dados · Inteligência Artificial · Automação"),
    ("ls stack/", "Python · SQL · Power BI · Tableau · React · Kotlin"),
    ("echo $MISSAO", "Transformar dados em decisões e problemas em produtos"),
    ("status", "aberto a oportunidades"),
]


def intro():
    W, H = 880, 300
    corpo = ""
    t = 0.4
    for i, (cmd, saida) in enumerate(LINHAS):
        y = 88 + i * 40
        w_cmd = 22 + len(cmd) * 9.2
        d_cmd = len(cmd) * 0.045
        d_out = 0.5
        corpo += (
            f'<clipPath id="c{i}"><rect x="40" y="{y - 16}" height="22" width="0">'
            f'<animate attributeName="width" from="0" to="{w_cmd}" begin="{t:.2f}s" dur="{d_cmd:.2f}s" fill="freeze"/>'
            f"</rect></clipPath>"
            f'<g clip-path="url(#c{i})"><text x="40" y="{y}" class="p">$</text>'
            f'<text x="60" y="{y}" class="c">{escape(cmd)}</text></g>'
        )
        t += d_cmd + 0.15
        y2 = y + 18
        if cmd == "status":
            corpo += (
                f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="{d_out}s" fill="freeze"/>'
                f'<circle cx="{W - 250}" cy="{y - 5}" r="5" fill="#22c55e">'
                f'<animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>'
                f'<text x="{W - 238}" y="{y}" class="o">{escape(saida)}</text></g>'
            )
        else:
            corpo += (
                f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="{d_out}s" fill="freeze"/>'
                f'<text x="{W - 40}" y="{y}" class="o" text-anchor="end">{escape(saida)}</text></g>'
            )
        corpo += f'<line x1="40" y1="{y2 - 4}" x2="{W - 40}" y2="{y2 - 4}" stroke="{BORDER}" stroke-dasharray="2 5"/>'
        t += d_out
    ultimo_y = 88 + len(LINHAS) * 40
    corpo += (
        f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".1s" fill="freeze"/>'
        f'<text x="40" y="{ultimo_y}" class="p">$</text>'
        f'<rect x="60" y="{ultimo_y - 14}" width="10" height="18" fill="{ROXO_CLARO}">'
        f'<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect></g>'
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Cartão de apresentação de Leon Daniel Corrêa">
<defs>
  <linearGradient id="bar" x1="0" x2="1"><stop stop-color="#1e1033"/><stop offset="1" stop-color="#2a1250"/></linearGradient>
  <linearGradient id="brilho" x1="0" x2="1"><stop stop-color="{ROXO}" stop-opacity="0"/><stop offset=".5" stop-color="{ROXO}"/><stop offset="1" stop-color="{ROXO}" stop-opacity="0"/></linearGradient>
</defs>
<style>
  .p {{ font: 700 15px {MONO}; fill: {ROXO}; }}
  .c {{ font: 500 15px {MONO}; fill: {LILAS}; }}
  .o {{ font: 400 15px {MONO}; fill: {MUTED}; }}
  .h {{ font: 500 13px {MONO}; fill: {MUTED}; }}
</style>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{BORDER}"/>
<path d="M0.5 44V14.5A14 14 0 0 1 14.5 0.5H{W - 14.5}A14 14 0 0 1 {W - 0.5} 14.5V44Z" fill="url(#bar)"/>
<circle cx="26" cy="22" r="6" fill="#7c3aed"/><circle cx="46" cy="22" r="6" fill="#a855f7"/><circle cx="66" cy="22" r="6" fill="#e9d5ff"/>
<text x="{W / 2}" y="27" class="h" text-anchor="middle">leon@perfil: ~</text>
<rect x="0" y="43" width="{W}" height="1.5" fill="url(#brilho)">
  <animate attributeName="x" values="-{W};{W}" dur="4s" repeatCount="indefinite"/>
</rect>
{corpo}
</svg>
"""


# ---------------------------------------------------------------- skills
SKILLS = [
    ("dados", "insights", "Análise de dados", ["Limpeza, exploração e dashboards", "com Python, SQL, Power BI e Tableau"]),
    ("ia", "auto_awesome", "Inteligência artificial", ["IA generativa em produtos e fluxos", "de trabalho, com Gemini e prompts"]),
    ("automacao", "hub", "Automação e integração", ["Consultas SQL, integração entre", "sistemas e automação de rotinas"]),
    ("financas", "payments", "Finanças e fluxo de caixa", ["Projeção de caixa, controle financeiro", "e padronização de planilhas"]),
    ("produtos", "devices", "Produtos digitais", ["Aplicações web e mobile,", "do problema ao deploy"]),
    ("organizacao", "account_tree", "Organização da informação", ["Organização de dados, documentação", "e registros de qualidade"]),
]


def skill(icon, titulo, linhas, atraso):
    W, H = 430, 130
    texto = "".join(
        f'<text x="112" y="{78 + i * 20}" class="d">{escape(l)}</text>' for i, l in enumerate(linhas)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(titulo)}">
<defs>
  <linearGradient id="q" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#2a1250"/><stop offset="1" stop-color="#140a26"/></linearGradient>
  <linearGradient id="borda" x1="0" x2="1"><stop stop-color="{ROXO}"/><stop offset="1" stop-color="{ROXO}" stop-opacity="0"/></linearGradient>
</defs>
<style>
  .t {{ font: 700 17px {SANS}; fill: {LILAS}; }}
  .d {{ font: 400 13px {SANS}; fill: {MUTED}; }}
  .in {{ opacity: 0; animation: in .7s ease {atraso}s forwards; }}
  @keyframes in {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
</style>
<g class="in">
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{BORDER}"/>
<rect x="16" y="0" width="{W * 0.6:.0f}" height="2" rx="1" fill="url(#borda)"/>
<rect x="24" y="30" width="68" height="68" rx="16" fill="url(#q)" stroke="#5b21b6"/>
{icone(icon, 40, 46, 36, ROXO_CLARO)}
<text x="112" y="52" class="t">{escape(titulo)}</text>
{texto}
</g>
</svg>
"""


# ---------------------------------------------------------------- botões
BOTOES = [
    ("linkedin", "badge", "LinkedIn"),
    ("email", "mail", "E-mail"),
    ("portfolio", "language", "Portfólio"),
]


def botao(icon, rotulo):
    W, H = 200, 52
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(rotulo)}">
<defs>
  <linearGradient id="f" x1="0" x2="1"><stop stop-color="#1e1033"/><stop offset="1" stop-color="#3b1d6e"/></linearGradient>
  <linearGradient id="s" x1="0" x2="1"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".18"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <clipPath id="k"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="{(H - 2) / 2}"/></clipPath>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="{(H - 2) / 2}" fill="url(#f)" stroke="#7c3aed" stroke-width="1.5"/>
<g clip-path="url(#k)"><rect x="-80" y="0" width="60" height="{H}" fill="url(#s)" transform="skewX(-20)">
  <animate attributeName="x" values="-80;{W + 60}" dur="3s" repeatCount="indefinite"/>
</rect></g>
{icone(icon, 26, 14, 24, ROXO_CLARO)}
<text x="{W / 2 + 14}" y="{H / 2 + 5}" text-anchor="middle" style="font: 600 15px {SANS}; fill: {LILAS}; letter-spacing: .5px">{escape(rotulo)}</text>
</svg>
"""


# ---------------------------------------------------------------- divisor
def divisor():
    W, H = 880, 36
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="divisor">
<defs>
  <linearGradient id="l" x1="0" x2="1"><stop stop-color="{ROXO}" stop-opacity="0"/><stop offset=".5" stop-color="{ROXO}"/><stop offset="1" stop-color="{ROXO}" stop-opacity="0"/></linearGradient>
  <radialGradient id="g"><stop stop-color="{LILAS}"/><stop offset=".4" stop-color="{ROXO}" stop-opacity=".8"/><stop offset="1" stop-color="{ROXO}" stop-opacity="0"/></radialGradient>
</defs>
<rect x="0" y="{H / 2 - 0.75}" width="{W}" height="1.5" fill="url(#l)"/>
<circle cy="{H / 2}" r="10" fill="url(#g)">
  <animate attributeName="cx" values="60;{W - 60};60" dur="7s" repeatCount="indefinite"/>
</circle>
<g transform="translate({W / 2} {H / 2}) rotate(45)">
  <rect x="-6" y="-6" width="12" height="12" fill="{BG}" stroke="{ROXO_CLARO}" stroke-width="1.5">
    <animateTransform attributeName="transform" type="rotate" values="0;90;90" keyTimes="0;.3;1" dur="4s" repeatCount="indefinite"/>
  </rect>
</g>
</svg>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    salvar("intro.svg", intro())
    for i, (slug, icon, titulo, linhas) in enumerate(SKILLS):
        salvar(f"skill-{slug}.svg", skill(icon, titulo, linhas, round(0.15 * i, 2)))
    for slug, icon, rotulo in BOTOES:
        salvar(f"btn-{slug}.svg", botao(icon, rotulo))
    salvar("divisor.svg", divisor())


if __name__ == "__main__":
    main()
