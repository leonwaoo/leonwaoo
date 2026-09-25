"""Gera os elementos visuais do perfil em SVG (roxo sobre fundo escuro).

- banner.svg e rodape.svg
- intro.svg: cartão de apresentação animado (estilo terminal)
- skill-*.svg: cards de áreas de atuação com ícone
- tecnologias.svg: grade com as logos das ferramentas
- btn-*.svg: botões de contato
- divisor.svg: divisor animado entre seções
"""
import os
import textwrap

from estilo import (
    P,
    BG, BORDA, F, CLARO, M, ACENTO, ACENTO_CLARO, ACENTO_ESCURO, SUAVE,
    icone, logo, svg, txt, T, tam, tam_mono,
)

OUT = "dist"
T_ACENTO = P["acento"]
T_ACENTO_ESCURO = P["acento_escuro"]
T_BRANCO = P["branco"]
T_CLARO = P["claro"]
T_ESCURO = P["escuro"]
T_MEIO = P["meio"]
T_TILE = P["tile"]
T_TILE2 = P["tile2"]
T_TRACO = P["traco"]


def salvar(nome, conteudo):
    with open(os.path.join(OUT, nome), "w", encoding="utf-8") as f:
        f.write(conteudo)
    print("gerado", nome)


def estrelas(w, h, n, semente=11):
    """Pontinhos de luz piscando, espalhados pelo fundo."""
    out = ""
    for i in range(n):
        x = (semente * 53 + i * 137) % w
        y = (semente * 29 + i * 71) % h
        r = 0.8 + (i % 3) * 0.6
        dur = 2 + (i % 5) * 0.7
        out += (
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{CLARO}" opacity=".6">'
            f'<animate attributeName="opacity" values=".15;.8;.15" dur="{dur:.1f}s" begin="-{i * 0.37:.2f}s" repeatCount="indefinite"/></circle>'
        )
    return out


# ------------------------------------------------------------------ banner
def banner():
    W, H = 1200, 280
    c = f"""<defs>
<linearGradient id="fundo" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{T_ESCURO}"/><stop offset=".55" stop-color="{T_MEIO}"/><stop offset="1" stop-color="{T_ACENTO_ESCURO}"/></linearGradient>
<radialGradient id="luz" cx=".8" cy=".2" r=".6"><stop stop-color="{ACENTO_CLARO}" stop-opacity=".55"/><stop offset="1" stop-color="{ACENTO_CLARO}" stop-opacity="0"/></radialGradient>
<linearGradient id="onda1" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{ACENTO}" stop-opacity=".55"/><stop offset="1" stop-color="{ACENTO_ESCURO}" stop-opacity=".2"/></linearGradient>
<linearGradient id="onda2" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{ACENTO_CLARO}" stop-opacity=".35"/><stop offset="1" stop-color="{ACENTO}" stop-opacity=".1"/></linearGradient>
<clipPath id="k"><rect width="{W}" height="{H}" rx="20"/></clipPath>
</defs>
<g clip-path="url(#k)">
<rect width="{W}" height="{H}" fill="url(#fundo)"/>
<rect width="{W}" height="{H}" fill="url(#luz)"/>
{estrelas(W, H - 70, 40)}
<path fill="url(#onda1)"><animate attributeName="d" dur="9s" repeatCount="indefinite" values="
M0 200 C 250 160, 450 250, 700 205 S 1050 170, 1200 200 V 280 H 0 Z;
M0 210 C 250 240, 450 170, 700 215 S 1050 240, 1200 205 V 280 H 0 Z;
M0 200 C 250 160, 450 250, 700 205 S 1050 170, 1200 200 V 280 H 0 Z"/></path>
<path fill="url(#onda2)"><animate attributeName="d" dur="12s" repeatCount="indefinite" values="
M0 230 C 300 205, 600 265, 900 230 S 1150 215, 1200 225 V 280 H 0 Z;
M0 225 C 300 255, 600 205, 900 235 S 1150 250, 1200 230 V 280 H 0 Z;
M0 230 C 300 205, 600 265, 900 230 S 1150 215, 1200 225 V 280 H 0 Z"/></path>
</g>
<text x="{W / 2}" y="122" text-anchor="middle" class="nome">Leon Daniel</text>
<text x="{W / 2}" y="166" text-anchor="middle" class="sub">Dados · IA · Automação</text>
"""
    css = (
        f".nome{{font:900 {tam(60)} {T};fill:{T_BRANCO};letter-spacing:.5px}}"
        f".sub{{font:700 19px {F};fill:{CLARO};letter-spacing:3px;opacity:.9}}"
    )
    return svg(W, H, c, "Leon Daniel — Dados · IA · Automação", css)


def rodape():
    W, H = 1200, 130
    c = f"""<defs>
<linearGradient id="f1" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{ACENTO}"/><stop offset=".5" stop-color="{T_TRACO}"/><stop offset="1" stop-color="{T_ESCURO}"/></linearGradient>
<linearGradient id="f2" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{ACENTO_CLARO}" stop-opacity=".45"/><stop offset="1" stop-color="{ACENTO}" stop-opacity=".15"/></linearGradient>
<clipPath id="k"><rect width="{W}" height="{H}" rx="20"/></clipPath></defs>
<g clip-path="url(#k)">
<path fill="url(#f2)"><animate attributeName="d" dur="10s" repeatCount="indefinite" values="
M0 30 C 250 0, 500 60, 750 25 S 1100 10, 1200 30 V 130 H 0 Z;
M0 20 C 250 55, 500 5, 750 35 S 1100 50, 1200 20 V 130 H 0 Z;
M0 30 C 250 0, 500 60, 750 25 S 1100 10, 1200 30 V 130 H 0 Z"/></path>
<path d="M0 55 C 260 25, 520 85, 780 50 S 1080 35, 1200 55 V 130 H 0 Z" fill="url(#f1)"/>
{estrelas(W, 40, 12, 5)}
</g>
<text x="{W / 2}" y="{H - 28}" text-anchor="middle" class="r">dados → decisões</text>
"""
    return svg(W, H, c, "dados → decisões", f".r{{font:800 {tam(22)} {T};fill:{T_BRANCO};letter-spacing:1px}}")


# ------------------------------------------------------------------ cartão
LINHAS = [
    ("whoami", "Leon Daniel"),
    ("cat foco.txt", "Dados · Inteligência Artificial · Automação"),
    ("ls stack/", "Python · SQL · Power BI · Tableau · React · Kotlin"),
    ("ls ias/", "diversas IAs generativas, cada uma para um tipo de tarefa"),
    ("echo $MISSAO", "transformar dados em decisões e problemas em produtos"),
    ("status", "aberto a oportunidades"),
]


def intro():
    W, H = 880, 336
    corpo, t, mono = "", 0.4, "$"
    for i, (cmd, saida) in enumerate(LINHAS):
        y = 88 + i * 38
        w_cmd = 24 + len(cmd) * 9.4
        d_cmd = len(cmd) * 0.045
        mono += cmd + saida
        corpo += (
            f'<clipPath id="c{i}"><rect x="40" y="{y - 16}" height="22" width="0">'
            f'<animate attributeName="width" from="0" to="{w_cmd}" begin="{t:.2f}s" dur="{d_cmd:.2f}s" fill="freeze"/></rect></clipPath>'
            f'<g clip-path="url(#c{i})"><text x="40" y="{y}" class="p">$</text><text x="60" y="{y}" class="c">{txt(cmd)}</text></g>'
        )
        t += d_cmd + 0.15
        if cmd == "status":
            saida_svg = (
                f'<circle cx="{W - 250}" cy="{y - 5}" r="5" fill="#22c55e">'
                f'<animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>'
                f'<text x="{W - 238}" y="{y}" class="o">{txt(saida)}</text>'
            )
        else:
            saida_svg = f'<text x="{W - 40}" y="{y}" class="o" text-anchor="end">{txt(saida)}</text>'
        corpo += (
            f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".5s" fill="freeze"/>{saida_svg}</g>'
            f'<line x1="40" y1="{y + 14}" x2="{W - 40}" y2="{y + 14}" stroke="{BORDA}" stroke-dasharray="2 5"/>'
        )
        t += 0.5
    uy = 88 + len(LINHAS) * 38
    corpo += (
        f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".1s" fill="freeze"/>'
        f'<text x="40" y="{uy}" class="p">$</text><rect x="60" y="{uy - 14}" width="10" height="18" fill="{ACENTO_CLARO}">'
        f'<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect></g>'
    )
    c = f"""<defs>
<linearGradient id="bar" x1="0" x2="1"><stop stop-color="{T_ESCURO}"/><stop offset="1" stop-color="{T_TILE}"/></linearGradient>
<linearGradient id="brilho" x1="0" x2="1"><stop stop-color="{ACENTO}" stop-opacity="0"/><stop offset=".5" stop-color="{ACENTO}"/><stop offset="1" stop-color="{ACENTO}" stop-opacity="0"/></linearGradient>
</defs>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{BORDA}"/>
<path d="M0.5 44V14.5A14 14 0 0 1 14.5 0.5H{W - 14.5}A14 14 0 0 1 {W - 0.5} 14.5V44Z" fill="url(#bar)"/>
<circle cx="26" cy="22" r="6" fill="{T_ACENTO_ESCURO}"/><circle cx="46" cy="22" r="6" fill="{T_ACENTO}"/><circle cx="66" cy="22" r="6" fill="{T_CLARO}"/>
<text x="{W / 2}" y="27" class="h" text-anchor="middle">leon@perfil: ~</text>
<rect x="0" y="43" width="{W}" height="1.5" fill="url(#brilho)"><animate attributeName="x" values="-{W};{W}" dur="4s" repeatCount="indefinite"/></rect>
{corpo}"""
    css = (
        f".p{{font:700 {tam_mono(15)} {M};fill:{ACENTO}}}.c{{font:600 {tam_mono(15)} {M};fill:{CLARO}}}"
        f".o{{font:400 {tam_mono(15)} {M};fill:{SUAVE}}}.h{{font:500 {tam_mono(13)} {M};fill:{SUAVE}}}"
    )
    return svg(W, H, c, "Cartão de apresentação de Leon Daniel", css, texto_mono=mono + "leon@perfil: ~")


# ------------------------------------------------------------------ skills
SKILLS = [
    ("dados", "insights", "Análise de dados", "Limpeza, exploração e dashboards com Python, SQL, Power BI e Tableau"),
    ("ia", "auto_awesome", "Inteligência artificial", "Uso diversas IAs generativas para pesquisar, prototipar, automatizar tarefas e acelerar análises"),
    ("automacao", "hub", "Automação e integração", "Consultas SQL, integração entre sistemas e automação de rotinas"),
    ("financas", "payments", "Finanças e fluxo de caixa", "Projeção de caixa, controle financeiro e padronização de planilhas"),
    ("produtos", "devices", "Produtos digitais", "Aplicações web e mobile, do problema ao deploy"),
    ("organizacao", "account_tree", "Organização da informação", "Organização de dados, documentação e registros de qualidade"),
]


def skill(icon, titulo, desc, atraso):
    W, H = 430, 136
    linhas = textwrap.wrap(desc, 40)
    texto = "".join(f'<text x="112" y="{80 + i * 20}" class="d">{txt(l)}</text>' for i, l in enumerate(linhas))
    c = f"""<defs>
<linearGradient id="q" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{T_TILE}"/><stop offset="1" stop-color="{T_TILE2}"/></linearGradient>
<linearGradient id="borda" x1="0" x2="1"><stop stop-color="{ACENTO}"/><stop offset="1" stop-color="{ACENTO}" stop-opacity="0"/></linearGradient>
</defs>
<g class="in">
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{BORDA}"/>
<rect x="16" y="0" width="{W * 0.6:.0f}" height="2" rx="1" fill="url(#borda)"/>
<rect x="24" y="{H / 2 - 34}" width="68" height="68" rx="16" fill="url(#q)" stroke="{T_TRACO}"/>
{icone(icon, 40, H / 2 - 18, 36)}
<text x="112" y="54" class="t">{txt(titulo)}</text>{texto}
</g>"""
    css = (
        f".t{{font:800 {tam(18)} {T};fill:{CLARO}}}.d{{font:600 13.5px {F};fill:{SUAVE}}}"
        f".in{{opacity:0;animation:in .7s ease {atraso}s forwards}}"
        "@keyframes in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}"
    )
    return svg(W, H, c, titulo, css)


# ------------------------------------------------------------------ tecnologias
TECNOLOGIAS = [
    ("python", "Python"), (None, "SQL", "database"), ("powerbi", "Power BI"), ("tableau", "Tableau"),
    ("microsoftexcel", "Excel"), (None, "IA generativa", "auto_awesome"), ("javascript", "JavaScript"),
    ("typescript", "TypeScript"), ("react", "React"), ("vite", "Vite"), ("html5", "HTML5"),
    ("css", "CSS"), ("kotlin", "Kotlin"), ("flutter", "Flutter"),
]


def tecnologias():
    W, por_linha, passo = 880, 7, 118
    rows = (len(TECNOLOGIAS) + por_linha - 1) // por_linha
    H = 30 + rows * 128
    x0 = (W - (por_linha - 1) * passo) / 2
    itens = ""
    for i, t in enumerate(TECNOLOGIAS):
        slug, nome = t[0], t[1]
        cx, cy = x0 + (i % por_linha) * passo, 66 + (i // por_linha) * 128
        marca = logo(slug, cx - 17, cy - 17, 34) if slug else None
        if marca is None:
            marca = icone(t[2] if len(t) > 2 else "code", cx - 20, cy - 20, 40, CLARO)
        itens += (
            f'<g class="in" style="animation-delay:{i * 0.05:.2f}s">'
            f'<rect x="{cx - 36}" y="{cy - 36}" width="72" height="72" rx="18" fill="url(#q)" stroke="{T_TRACO}"/>'
            f'<rect x="{cx - 22}" y="{cy - 36}" width="44" height="2" rx="1" fill="{ACENTO}"/>'
            f"{marca}"
            f'<text x="{cx}" y="{cy + 60}" text-anchor="middle" class="l">{txt(nome)}</text></g>'
        )
    c = f"""<defs><linearGradient id="q" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{T_TILE}"/><stop offset="1" stop-color="{T_TILE2}"/></linearGradient></defs>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{BORDA}"/>{itens}"""
    css = f".l{{font:700 13px {F};fill:{CLARO}}}.in{{opacity:0;animation:in .5s ease forwards}}@keyframes in{{to{{opacity:1}}}}"
    return svg(W, H, c, "Tecnologias", css)


# ------------------------------------------------------------------ botões
BOTOES = [("linkedin", "badge", "LinkedIn"), ("email", "mail", "E-mail"), ("portfolio", "language", "Portfólio")]


def botao(icon, rotulo):
    W, H = 200, 52
    c = f"""<defs>
<linearGradient id="f" x1="0" x2="1"><stop stop-color="{T_ESCURO}"/><stop offset="1" stop-color="{T_MEIO}"/></linearGradient>
<linearGradient id="s" x1="0" x2="1"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".18"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="k"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="{(H - 2) / 2}"/></clipPath></defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="{(H - 2) / 2}" fill="url(#f)" stroke="{T_ACENTO_ESCURO}" stroke-width="1.5"/>
<g clip-path="url(#k)"><rect x="-80" y="0" width="60" height="{H}" fill="url(#s)" transform="skewX(-20)"><animate attributeName="x" values="-80;{W + 60}" dur="3s" repeatCount="indefinite"/></rect></g>
{icone(icon, 26, 14, 24)}
<text x="{W / 2 + 14}" y="{H / 2 + 6}" text-anchor="middle" class="b">{txt(rotulo)}</text>"""
    return svg(W, H, c, rotulo, f".b{{font:800 15px {F};fill:{CLARO};letter-spacing:.5px}}")


# ------------------------------------------------------------------ divisor
def divisor():
    W, H = 880, 36
    c = f"""<defs>
<linearGradient id="l" x1="0" x2="1"><stop stop-color="{ACENTO}" stop-opacity="0"/><stop offset=".5" stop-color="{ACENTO}"/><stop offset="1" stop-color="{ACENTO}" stop-opacity="0"/></linearGradient>
<radialGradient id="g"><stop stop-color="{CLARO}"/><stop offset=".4" stop-color="{ACENTO}" stop-opacity=".8"/><stop offset="1" stop-color="{ACENTO}" stop-opacity="0"/></radialGradient></defs>
<rect x="0" y="{H / 2 - 0.75}" width="{W}" height="1.5" fill="url(#l)"/>
<circle cy="{H / 2}" r="10" fill="url(#g)"><animate attributeName="cx" values="60;{W - 60};60" dur="7s" repeatCount="indefinite"/></circle>
<g transform="translate({W / 2} {H / 2}) rotate(45)"><rect x="-6" y="-6" width="12" height="12" fill="{BG}" stroke="{ACENTO_CLARO}" stroke-width="1.5">
<animateTransform attributeName="transform" type="rotate" values="0;90;90" keyTimes="0;.3;1" dur="4s" repeatCount="indefinite"/></rect></g>"""
    return svg(W, H, c, "divisor")


# ------------------------------------------------------------------ ícones
PROJETOS = {
    "data-sense": "query_stats", "confere-agora": "verified_user", "ordem-pro": "receipt_long",
    "calcula-clt": "calculate", "site-aroeiras": "storefront", "portfolio": "account_circle",
}
TITULOS = ["person", "psychology", "work", "workspace_premium", "code", "rocket_launch", "monitoring", "timeline", "forum"]


def icone_projeto(nome):
    """Ícone de projeto: bloco com degradê, brilho e uma luz percorrendo a borda."""
    W = 72
    per = 4 * 60
    c = f"""<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{T_ACENTO_ESCURO}"/><stop offset="1" stop-color="{T_ESCURO}"/></linearGradient>
<radialGradient id="luz" cx=".25" cy=".2" r=".8"><stop stop-color="{ACENTO_CLARO}" stop-opacity=".55"/><stop offset="1" stop-color="{ACENTO_CLARO}" stop-opacity="0"/></radialGradient>
</defs>
<rect x="6" y="6" width="60" height="60" rx="18" fill="url(#g)"/>
<rect x="6" y="6" width="60" height="60" rx="18" fill="url(#luz)"/>
<rect x="6" y="6" width="60" height="60" rx="18" fill="none" stroke="{ACENTO}" stroke-opacity=".35" stroke-width="1.5"/>
<rect x="6" y="6" width="60" height="60" rx="18" fill="none" stroke="{ACENTO_CLARO}" stroke-width="2" stroke-linecap="round" stroke-dasharray="36 {per - 36}">
<animate attributeName="stroke-dashoffset" values="0;-{per}" dur="4s" repeatCount="indefinite"/></rect>
{icone(nome, 19, 19, 34, T_BRANCO, cheio=True)}
<ellipse cx="30" cy="16" rx="18" ry="6" fill="#fff" opacity=".12"/>"""
    return svg(W, W, c, nome)


def icone_titulo(nome):
    c = f"""<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{T_ACENTO_ESCURO}"/><stop offset="1" stop-color="{T_MEIO}"/></linearGradient></defs>
<rect x="1" y="1" width="30" height="30" rx="9" fill="url(#g)"/>
{icone(nome, 6, 6, 20, T_BRANCO, cheio=True)}"""
    return svg(32, 32, c, nome)


def main():
    os.makedirs(OUT, exist_ok=True)
    salvar("banner.svg", banner())
    salvar("rodape.svg", rodape())
    salvar("intro.svg", intro())
    for i, (slug, icon, titulo, desc) in enumerate(SKILLS):
        salvar(f"skill-{slug}.svg", skill(icon, titulo, desc, round(0.15 * i, 2)))
    salvar("tecnologias.svg", tecnologias())
    for slug, icon, rotulo in BOTOES:
        salvar(f"btn-{slug}.svg", botao(icon, rotulo))
    salvar("divisor.svg", divisor())
    for slug, nome in PROJETOS.items():
        salvar(f"proj-{slug}.svg", icone_projeto(nome))
    for nome in TITULOS:
        salvar(f"ic-{nome}.svg", icone_titulo(nome))


if __name__ == "__main__":
    main()
