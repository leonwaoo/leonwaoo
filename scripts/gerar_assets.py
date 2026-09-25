"""Gera os elementos visuais do perfil em SVG (estilo Frutiger Aero)."""
import os
import textwrap

from estilo import (
    AQUA_1, AQUA_2, AQUA_3, BORDA, BRANCO, MONO, SANS, SUAVE, TEXTO, TITULO, VERDE,
    bolha, defs_base, icone, logo, painel, pilha, svg, txt,
)

OUT = "dist"
F = pilha(SANS)
M = pilha(MONO)


def salvar(nome, conteudo):
    with open(os.path.join(OUT, nome), "w", encoding="utf-8") as f:
        f.write(conteudo)
    print("gerado", nome)


def bolhas_subindo(w, h, n=9, semente=7, topo=None):
    """Bolhas que sobem devagar (animação)."""
    out = ""
    fim = topo
    for i in range(n):
        x = (semente * 97 + i * 131) % w
        r = 4 + (i * 7) % 14
        dur = 7 + (i * 3) % 6
        atraso = -((i * 1.7) % dur)
        out += (
            f'<circle cx="{x}" cy="{h + r}" r="{r}" fill="url(#deco)" opacity=".85">'
            f'<animate attributeName="cy" values="{h + r};{(fim if fim is not None else -r)}" dur="{dur}s" begin="{atraso:.1f}s" repeatCount="indefinite"/>'
            f"</circle>"
        )
    return out


# ------------------------------------------------------------------ banner
def banner():
    W, H = 1200, 300
    raios = "".join(
        f'<polygon points="{-100 + i * 140},0 {40 + i * 140},0 {420 + i * 190},{H} {260 + i * 190},{H}" fill="#fff" opacity=".07"/>'
        for i in range(6)
    )
    c = f"""<defs>{defs_base()}
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#0a6fd6"/><stop offset=".55" stop-color="#38b6ff"/><stop offset="1" stop-color="#bfeaff"/></linearGradient>
<linearGradient id="grama" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#8be9a8"/><stop offset="1" stop-color="#1f9d4f"/></linearGradient>
<linearGradient id="agua" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#7fe6ff" stop-opacity=".9"/><stop offset="1" stop-color="#1e9bff" stop-opacity=".9"/></linearGradient>
<linearGradient id="pill" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity=".18"/></linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="22" fill="url(#sky)"/>
{raios}
<ellipse cx="170" cy="40" rx="260" ry="120" fill="#fff" opacity=".18"/>
{bolhas_subindo(W, H, 14)}
<path d="M0 {H - 60} C 200 {H - 110}, 420 {H - 20}, 640 {H - 70} S 1000 {H - 120}, {W} {H - 70} V {H - 22} Q {W} {H} {W - 22} {H} H 22 Q 0 {H} 0 {H - 22} Z" fill="url(#agua)"/>
<path d="M0 {H - 34} C 260 {H - 70}, 520 {H - 10}, 780 {H - 44} S 1080 {H - 60}, {W} {H - 36} V {H - 22} Q {W} {H} {W - 22} {H} H 22 Q 0 {H} 0 {H - 22} Z" fill="url(#grama)"/>
<text x="{W / 2}" y="138" text-anchor="middle" class="nome">Leon Daniel Corrêa</text>
<rect x="{W / 2 - 170}" y="160" width="340" height="44" rx="22" fill="url(#pill)" stroke="#fff" stroke-opacity=".7"/>
<text x="{W / 2}" y="189" text-anchor="middle" class="sub">Dados · IA · Automação</text>
"""
    css = (
        f".nome{{font:900 64px {F};fill:#fff;paint-order:stroke;stroke:#0a4f9e;stroke-opacity:.25;stroke-width:6px;letter-spacing:.5px}}"
        f".sub{{font:700 20px {F};fill:#fff;letter-spacing:1px}}"
    )
    return svg(W, H, c, "Leon Daniel Corrêa — Dados · IA · Automação", css)


def rodape():
    W, H = 1200, 150
    c = f"""<defs>{defs_base()}
<linearGradient id="a1" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#7fe6ff"/><stop offset="1" stop-color="#1e9bff"/></linearGradient>
<linearGradient id="a2" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#38b6ff"/><stop offset="1" stop-color="#0a6fd6"/></linearGradient>
</defs>
<path d="M0 50 C 220 10, 420 90, 640 50 S 1000 0, {W} 40 V {H - 22} Q {W} {H} {W - 22} {H} H 22 Q 0 {H} 0 {H - 22} Z" fill="url(#a1)" opacity=".7"/>
<path d="M0 78 C 260 40, 520 120, 780 72 S 1080 50, {W} 80 V {H - 22} Q {W} {H} {W - 22} {H} H 22 Q 0 {H} 0 {H - 22} Z" fill="url(#a2)"/>
{bolhas_subindo(W, H, 8, 3, topo=70)}
<text x="{W / 2}" y="{H - 30}" text-anchor="middle" class="r">dados → decisões</text>
"""
    return svg(W, H, c, "dados → decisões", f".r{{font:800 24px {F};fill:#fff;letter-spacing:1px}}")


# ------------------------------------------------------------------ cartão
LINHAS = [
    ("whoami", "Leon Daniel Corrêa"),
    ("cat foco.txt", "Dados · Inteligência Artificial · Automação"),
    ("ls stack/", "Python · SQL · Power BI · Tableau · React · Kotlin"),
    ("ls ias/", "diversas IAs generativas, cada uma para um tipo de tarefa"),
    ("echo $MISSAO", "transformar dados em decisões e problemas em produtos"),
    ("status", "aberto a oportunidades"),
]


def intro():
    W, H = 880, 360
    corpo, t = "", 0.4
    mono_txt = ""
    for i, (cmd, saida) in enumerate(LINHAS):
        y = 104 + i * 38
        w_cmd = 26 + len(cmd) * 9.6
        d_cmd = len(cmd) * 0.045
        mono_txt += cmd + saida + "$"
        corpo += (
            f'<clipPath id="c{i}"><rect x="40" y="{y - 17}" height="24" width="0">'
            f'<animate attributeName="width" from="0" to="{w_cmd}" begin="{t:.2f}s" dur="{d_cmd:.2f}s" fill="freeze"/></rect></clipPath>'
            f'<g clip-path="url(#c{i})"><text x="40" y="{y}" class="p">$</text><text x="60" y="{y}" class="c">{txt(cmd)}</text></g>'
        )
        t += d_cmd + 0.15
        if cmd == "status":
            saida_svg = (
                f'<circle cx="{W - 250}" cy="{y - 5}" r="6" fill="{VERDE}" stroke="#fff" stroke-width="1.5">'
                f'<animate attributeName="r" values="6;7.5;6" dur="1.6s" repeatCount="indefinite"/></circle>'
                f'<text x="{W - 236}" y="{y}" class="o">{txt(saida)}</text>'
            )
        else:
            saida_svg = f'<text x="{W - 44}" y="{y}" class="o" text-anchor="end">{txt(saida)}</text>'
        corpo += (
            f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".5s" fill="freeze"/>{saida_svg}</g>'
            f'<line x1="40" y1="{y + 14}" x2="{W - 44}" y2="{y + 14}" stroke="{BORDA}" stroke-opacity=".6" stroke-dasharray="2 5"/>'
        )
        t += 0.5
    uy = 104 + len(LINHAS) * 38
    corpo += (
        f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".1s" fill="freeze"/>'
        f'<text x="40" y="{uy}" class="p">$</text><rect x="60" y="{uy - 15}" width="10" height="19" rx="2" fill="{AQUA_2}">'
        f'<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect></g>'
    )
    c = f"""<defs>{defs_base()}
<linearGradient id="barra" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#9fe3ff"/><stop offset=".5" stop-color="#38a8f5"/><stop offset=".5" stop-color="#1e8ee6"/><stop offset="1" stop-color="#1673c9"/></linearGradient>
<clipPath id="janela"><rect x="4" y="3" width="{W - 8}" height="{H - 10}" rx="18"/></clipPath>
</defs>
{painel(W, H, bolhas=False)}
<g clip-path="url(#janela)"><rect x="0" y="0" width="{W}" height="48" fill="url(#barra)"/>
<rect x="0" y="0" width="{W}" height="22" fill="#fff" opacity=".25"/>
<rect x="-200" y="0" width="160" height="48" fill="#fff" opacity=".22" transform="skewX(-25)"><animate attributeName="x" values="-200;{W + 200}" dur="5s" repeatCount="indefinite"/></rect></g>
<text x="28" y="31" class="h">leon@perfil: ~</text>
<circle cx="{W - 88}" cy="25" r="8" fill="url(#bolhaVerde)" stroke="#fff"/><circle cx="{W - 64}" cy="25" r="8" fill="url(#bolha)" stroke="#fff"/><circle cx="{W - 40}" cy="25" r="8" fill="#ff6b6b" stroke="#fff"/>
<circle cx="{W - 70}" cy="{H - 40}" r="22" fill="url(#deco)"/><circle cx="{W - 110}" cy="{H - 24}" r="9" fill="url(#deco)"/>
{corpo}"""
    css = (
        f".p{{font:700 16px {M};fill:{AQUA_2}}}.c{{font:600 16px {M};fill:{TITULO}}}"
        f".o{{font:400 15px {M};fill:{TEXTO}}}.h{{font:700 15px {F};fill:#fff;letter-spacing:.5px}}"
    )
    return svg(W, H, c, "Cartão de apresentação de Leon Daniel Corrêa", css, texto_mono=mono_txt)


# ------------------------------------------------------------------ skills
SKILLS = [
    ("dados", "insights", "Análise de dados", "Limpeza, exploração e dashboards com Python, SQL, Power BI e Tableau"),
    ("ia", "auto_awesome", "Inteligência artificial", "Uso diversas IAs generativas para pesquisar, prototipar, automatizar tarefas e acelerar análises"),
    ("automacao", "hub", "Automação e integração", "Consultas SQL, integração entre sistemas e automação de rotinas repetitivas"),
    ("financas", "payments", "Finanças e fluxo de caixa", "Projeção de caixa, controle financeiro e planilhas padronizadas"),
    ("produtos", "devices", "Produtos digitais", "Aplicações web e mobile, do problema ao deploy"),
    ("organizacao", "account_tree", "Organização da informação", "Estruturação de dados, documentação técnica e registros de qualidade"),
]


def skill(icon, titulo, desc, atraso):
    W, H = 430, 150
    linhas = textwrap.wrap(desc, 38)
    texto = "".join(f'<text x="118" y="{86 + i * 21}" class="d">{txt(l)}</text>' for i, l in enumerate(linhas))
    c = f"""<defs>{defs_base()}</defs><g class="in">{painel(W, H)}
{bolha(64, 72, 34, icon)}
<text x="118" y="58" class="t">{txt(titulo)}</text>{texto}</g>"""
    css = (
        f".t{{font:800 19px {F};fill:{TITULO}}}.d{{font:600 14px {F};fill:{TEXTO}}}"
        f".in{{opacity:0;animation:in .7s ease {atraso}s forwards}}"
        "@keyframes in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}"
    )
    return svg(W, H, c, titulo, css)


# ------------------------------------------------------------------ experiências
EXPERIENCIAS = [
    ("database", "Desenvolvi consultas SQL e dei suporte técnico avançado para manter integrações entre sistemas funcionando"),
    ("trending_up", "Criei um sistema de projeção de fluxo de caixa que reduziu impactos no caixa e padronizei as planilhas financeiras para toda a equipe"),
    ("fact_check", "Organizei dados, mantive registros de qualidade e produzi documentação técnica usada em auditorias internas"),
    ("query_stats", "Participei de projetos de extensão em análise de dados"),
    ("auto_awesome", "Crio conteúdo e resolvo desafios práticos com IA generativa em um programa de embaixadores estudantis"),
    ("rocket_launch", "Desenvolvi e publiquei aplicações web e Android, do protótipo ao deploy"),
]


def experiencias():
    W = 880
    itens, y = "", 28
    for i, (icon, frase) in enumerate(EXPERIENCIAS):
        linhas = textwrap.wrap(frase, 88)
        alt = max(64, 28 + len(linhas) * 22)
        cy = y + alt / 2 - 6
        itens += f'<g class="in" style="animation-delay:{i * 0.12:.2f}s">'
        itens += bolha(62, cy, 22, icon, verde=(i % 2 == 1))
        base = cy - (len(linhas) - 1) * 11 + 6
        itens += "".join(f'<text x="104" y="{base + k * 22:.0f}" class="e">{txt(l)}</text>' for k, l in enumerate(linhas))
        itens += "</g>"
        if i < len(EXPERIENCIAS) - 1:
            itens += f'<line x1="62" y1="{cy + 26:.0f}" x2="62" y2="{y + alt + 12:.0f}" stroke="{BORDA}" stroke-width="2" stroke-dasharray="3 4"/>'
        y += alt + 14
    H = int(y + 24)
    c = f"<defs>{defs_base()}</defs>{painel(W, H)}{itens}"
    css = (
        f".e{{font:600 15.5px {F};fill:{TITULO}}}"
        ".in{opacity:0;animation:in .7s ease forwards}"
        "@keyframes in{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}"
    )
    return svg(W, H, c, "Experiências", css)


# ------------------------------------------------------------------ certificações
CERTIFICADOS = [
    ("Google Data Analytics", "Google · Coursera"),
    ("AI Essentials", "Google"),
    ("Habilidades Aplicadas: simplificar fluxos de trabalho de negócios com chat de IA", "Microsoft"),
    ("Power BI", "Microsoft Learn"),
    ("Programa ONE Tech Foundation G9 — Data Science", "Alura"),
    ("Python para Ciência de Dados", "One Tech Foundation"),
    ("Formação Iniciante em Programação G9 — ONE", "Alura"),
    ("Formação Desenvolvimento Pessoal G9 — ONE", "Alura"),
]


def certificacoes():
    W, col_w, lin_h = 880, 412, 84
    rows = (len(CERTIFICADOS) + 1) // 2
    H = 40 + rows * lin_h + 10
    itens = ""
    for i, (nome, emissor) in enumerate(CERTIFICADOS):
        col, row = i % 2, i // 2
        x0, y0 = 30 + col * col_w, 34 + row * lin_h
        linhas = textwrap.wrap(nome, 44)
        itens += f'<g class="in" style="animation-delay:{i * 0.08:.2f}s">'
        itens += f'<rect x="{x0}" y="{y0}" width="{col_w - 20}" height="{lin_h - 12}" rx="14" fill="#fff" fill-opacity=".55" stroke="{BORDA}" stroke-opacity=".7"/>'
        itens += bolha(x0 + 36, y0 + (lin_h - 12) / 2, 20, "workspace_premium", verde=(col == 1))
        ty = y0 + 28 if len(linhas) == 2 else y0 + 34
        itens += "".join(f'<text x="{x0 + 68}" y="{ty + k * 18}" class="n">{txt(l)}</text>' for k, l in enumerate(linhas))
        itens += f'<text x="{x0 + 68}" y="{ty + len(linhas) * 18 + 2}" class="i">{txt(emissor)}</text></g>'
    c = f"<defs>{defs_base()}</defs>{painel(W, H)}{itens}"
    css = (
        f".n{{font:800 13.5px {F};fill:{TITULO}}}.i{{font:600 12.5px {F};fill:{SUAVE}}}"
        ".in{opacity:0;animation:in .6s ease forwards}@keyframes in{to{opacity:1}}"
    )
    return svg(W, H, c, "Certificações", css)


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
    H = 36 + rows * 130
    x_ini = (W - (por_linha - 1) * passo) / 2
    itens = ""
    for i, t in enumerate(TECNOLOGIAS):
        slug, nome = t[0], t[1]
        cx, cy = x_ini + (i % por_linha) * passo, 72 + (i // por_linha) * 130
        marca = logo(slug, cx - 18, cy - 18, 36) if slug else None
        if marca is None:
            marca = icone(t[2] if len(t) > 2 else "code", cx - 20, cy - 20, 40)
        itens += (
            f'<g class="in" style="animation-delay:{i * 0.05:.2f}s">'
            f'<rect x="{cx - 38}" y="{cy - 36}" width="76" height="76" rx="22" fill="{AQUA_3}" opacity=".18"/>'
            f'<rect x="{cx - 38}" y="{cy - 38}" width="76" height="76" rx="22" fill="url(#bolha)" stroke="#fff" stroke-opacity=".8" stroke-width="1.5"/>'
            f"{marca}"
            f'<rect x="{cx - 34}" y="{cy - 35}" width="68" height="32" rx="18" fill="#fff" opacity=".35"/>'
            f'<text x="{cx}" y="{cy + 62}" text-anchor="middle" class="l">{txt(nome)}</text></g>'
        )
    c = f"<defs>{defs_base()}</defs>{painel(W, H, bolhas=False)}{itens}"
    css = f".l{{font:800 13.5px {F};fill:{TITULO}}}.in{{opacity:0;animation:in .5s ease forwards}}@keyframes in{{to{{opacity:1}}}}"
    return svg(W, H, c, "Tecnologias", css)


# ------------------------------------------------------------------ ícones
TITULOS = ["person", "psychology", "work", "workspace_premium", "code", "rocket_launch", "monitoring", "timeline", "forum"]
PROJETOS = {
    "data-sense": "bar_chart", "confere-agora": "fact_check", "ordem-pro": "receipt_long",
    "calcula-clt": "calculate", "site-aroeiras": "storefront", "portfolio": "language",
}


def icone_titulo(nome):
    return svg(40, 40, f"<defs>{defs_base()}</defs>{bolha(20, 19, 17, nome)}", nome)


def icone_projeto(nome, i):
    return svg(72, 72, f"<defs>{defs_base()}</defs>{bolha(36, 34, 30, nome, verde=(i % 2 == 1))}", nome)


# ------------------------------------------------------------------ botões
def botao(icon, rotulo, largura=200, altura=54, verde=False):
    W, H = largura, altura
    g1, g2, g3 = ("#b8f5c9", VERDE, "#1f9d4f") if verde else (AQUA_1, AQUA_2, AQUA_3)
    r = (H - 6) / 2
    c = f"""<defs>
<linearGradient id="f" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{g1}"/><stop offset=".5" stop-color="{g2}"/><stop offset="1" stop-color="{g3}"/></linearGradient>
<linearGradient id="s" x1="0" x2="1"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".45"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="k"><rect x="3" y="2" width="{W - 6}" height="{H - 6}" rx="{r}"/></clipPath></defs>
<rect x="3" y="4" width="{W - 6}" height="{H - 6}" rx="{r}" fill="{g3}" opacity=".25"/>
<rect x="3" y="2" width="{W - 6}" height="{H - 6}" rx="{r}" fill="url(#f)" stroke="#fff" stroke-opacity=".8" stroke-width="1.5"/>
<g clip-path="url(#k)"><rect x="3" y="2" width="{W - 6}" height="{(H - 6) / 2}" fill="#fff" opacity=".35"/>
<rect x="-80" y="0" width="50" height="{H}" fill="url(#s)" transform="skewX(-20)"><animate attributeName="x" values="-80;{W + 60}" dur="3.5s" repeatCount="indefinite"/></rect></g>
{icone(icon, 22, (H - 6) / 2 - 11, 24)}
<text x="{W / 2 + 12}" y="{(H - 6) / 2 + 8}" text-anchor="middle" class="b">{txt(rotulo)}</text>"""
    css = f".b{{font:800 {16 if H > 48 else 14}px {F};fill:#fff;paint-order:stroke;stroke:{g3};stroke-opacity:.35;stroke-width:3px}}"
    return svg(W, H, c, rotulo, css)


# ------------------------------------------------------------------ divisor
def divisor():
    W, H = 880, 44
    c = f"""<defs>{defs_base()}
<linearGradient id="l" x1="0" x2="1"><stop stop-color="{AQUA_2}" stop-opacity="0"/><stop offset=".5" stop-color="{AQUA_2}"/><stop offset="1" stop-color="{AQUA_2}" stop-opacity="0"/></linearGradient></defs>
<path d="M0 22 Q 110 10 220 22 T 440 22 T 660 22 T 880 22" fill="none" stroke="url(#l)" stroke-width="2.5">
<animate attributeName="d" dur="6s" repeatCount="indefinite" values="M0 22 Q 110 10 220 22 T 440 22 T 660 22 T 880 22;M0 22 Q 110 34 220 22 T 440 22 T 660 22 T 880 22;M0 22 Q 110 10 220 22 T 440 22 T 660 22 T 880 22"/></path>
<circle cx="{W / 2}" cy="22" r="9" fill="url(#bolha)" stroke="#fff" stroke-width="1.5"/><ellipse cx="{W / 2}" cy="18" rx="5" ry="2.6" fill="#fff" opacity=".6"/>"""
    return svg(W, H, c, "divisor")


def main():
    os.makedirs(OUT, exist_ok=True)
    salvar("banner.svg", banner())
    salvar("rodape.svg", rodape())
    salvar("intro.svg", intro())
    for i, (slug, icon, titulo, desc) in enumerate(SKILLS):
        salvar(f"skill-{slug}.svg", skill(icon, titulo, desc, round(0.12 * i, 2)))
    salvar("experiencias.svg", experiencias())
    salvar("certificacoes.svg", certificacoes())
    salvar("tecnologias.svg", tecnologias())
    for nome in TITULOS:
        salvar(f"ic-{nome}.svg", icone_titulo(nome))
    for i, (slug, nome) in enumerate(PROJETOS.items()):
        salvar(f"proj-{slug}.svg", icone_projeto(nome, i))
    salvar("btn-linkedin.svg", botao("badge", "LinkedIn"))
    salvar("btn-email.svg", botao("mail", "E-mail"))
    salvar("btn-portfolio.svg", botao("language", "Portfólio"))
    salvar("btn-codigo.svg", botao("code", "Código", 150, 46))
    salvar("btn-aovivo.svg", botao("open_in_new", "Ao vivo", 150, 46, verde=True))
    salvar("divisor.svg", divisor())


if __name__ == "__main__":
    main()
