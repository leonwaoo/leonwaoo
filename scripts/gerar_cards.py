"""Gera os cards de dados do perfil (estatísticas, linguagens, sequência e atividade).

Roda no GitHub Actions. Usa a API GraphQL do GitHub com o token em GH_TOKEN
e grava os SVGs em dist/, no mesmo estilo dos demais elementos.
"""
import json
import os
import urllib.request
from datetime import date

from estilo import (
    AQUA_2, AQUA_3, BORDA, ESCALA, SANS, SUAVE, TEXTO, TITULO, VERDE,
    bolha, defs_base, painel, pilha, svg, txt,
)

USER = os.environ.get("GH_USER", "leonwaoo")
TOKEN = os.environ.get("GH_TOKEN", "")
OUT = "dist"
F = pilha(SANS)

QUERY = """
query($login: String!) {
  user(login: $login) {
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
  }
}
"""


def fetch():
    body = json.dumps({"query": QUERY, "variables": {"login": USER}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body,
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"Erro na API: {data['errors']}")
    return data["data"]["user"]


def fmt(n):
    return f"{n:,}".replace(",", ".")


CSS = (
    f".t{{font:800 18px {F};fill:{TITULO}}}.l{{font:600 14px {F};fill:{TEXTO}}}"
    f".v{{font:800 14px {F};fill:{TITULO}}}.big{{font:900 30px {F};fill:{TITULO}}}"
    f".s{{font:700 11.5px {F};fill:{SUAVE}}}"
    ".in{opacity:0;animation:in .6s ease forwards}@keyframes in{to{opacity:1}}"
)


def base(w, h, titulo, icone_titulo, corpo):
    c = (
        f"<defs>{defs_base()}</defs>{painel(w, h)}"
        + bolha(38, 38, 16, icone_titulo)
        + f'<text x="64" y="44" class="t">{txt(titulo)}</text>{corpo}'
    )
    return svg(w, h, c, titulo, CSS)


def dias(u):
    return [d for w in u["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]


def stats_card(u):
    c = u["contributionsCollection"]
    repos = u["repositories"]
    estrelas = sum(n["stargazerCount"] for n in repos["nodes"])
    total = c["contributionCalendar"]["totalContributions"]
    linhas = [
        ("Commits no último ano", c["totalCommitContributions"]),
        ("Pull requests", c["totalPullRequestContributions"]),
        ("Issues", c["totalIssueContributions"]),
        ("Repositórios públicos", repos["totalCount"]),
        ("Estrelas recebidas", estrelas),
    ]
    corpo = ""
    for i, (rotulo, val) in enumerate(linhas):
        y = 84 + i * 26
        corpo += (
            f'<g class="in" style="animation-delay:{i * 0.1:.1f}s"><circle cx="34" cy="{y - 5}" r="4" fill="{AQUA_2}"/>'
            f'<text x="48" y="{y}" class="l">{txt(rotulo)}</text><text x="292" y="{y}" class="v" text-anchor="end">{fmt(val)}</text></g>'
        )
    cx, cy, r = 400, 120, 52
    corpo += (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" fill-opacity=".6" stroke="{BORDA}" stroke-width="9"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#bolha)" stroke-width="9" stroke-linecap="round" '
        f'stroke-dasharray="{2 * 3.1416 * r:.1f}" transform="rotate(-90 {cx} {cy})"/>'
        f'<text x="{cx}" y="{cy + 10}" class="big" text-anchor="middle">{fmt(total)}</text>'
        f'<text x="{cx}" y="{cy + r + 24}" class="s" text-anchor="middle">contribuições no ano</text>'
    )
    return base(495, 215, "Estatísticas no GitHub", "monitoring", corpo)


def langs_card(u):
    totais = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            totais[e["node"]["name"]] = totais.get(e["node"]["name"], 0) + e["size"]
    top = sorted(totais.items(), key=lambda x: -x[1])[:6]
    soma = sum(v for _, v in top) or 1
    x, barra = 28, ""
    for i, (_, v) in enumerate(top):
        w = 294 * v / soma
        barra += f'<rect x="{x:.1f}" y="66" width="{max(w, 2):.1f}" height="12" fill="{ESCALA[i]}"/>'
        x += w
    corpo = (
        '<clipPath id="cb"><rect x="28" y="66" width="294" height="12" rx="6"/></clipPath>'
        f'<g clip-path="url(#cb)">{barra}<rect x="28" y="66" width="294" height="5" fill="#fff" opacity=".4"/></g>'
    )
    for i, (nome, v) in enumerate(top):
        col, row = i % 2, i // 2
        lx, ly = 28 + col * 156, 112 + row * 30
        corpo += (
            f'<g class="in" style="animation-delay:{i * 0.1:.1f}s"><circle cx="{lx + 6}" cy="{ly - 5}" r="6" fill="{ESCALA[i]}" stroke="#fff" stroke-width="1.5"/>'
            f'<text x="{lx + 18}" y="{ly}" class="v">{txt(nome)}</text>'
            f'<text x="{lx + 140}" y="{ly}" class="l" text-anchor="end">{100 * v / soma:.1f}%</text></g>'
        )
    return base(350, 215, "Linguagens mais usadas", "code", corpo)


def sequencia_card(u):
    ds = dias(u)
    hoje = ds[-1]
    atual, i = 0, len(ds) - 1
    if hoje["contributionCount"] == 0:
        i -= 1  # o dia de hoje ainda pode receber contribuições
    while i >= 0 and ds[i]["contributionCount"] > 0:
        atual += 1
        i -= 1
    maior = run = 0
    for d in ds:
        run = run + 1 if d["contributionCount"] > 0 else 0
        maior = max(maior, run)
    ativos = sum(1 for d in ds if d["contributionCount"] > 0)
    blocos = [
        ("local_fire_department", "Sequência atual", f"{atual} dias", False),
        ("emoji_events", "Maior sequência", f"{maior} dias", True),
        ("calendar_month", "Dias com contribuição", f"{ativos} no ano", False),
    ]
    corpo = ""
    for k, (ic, rot, val, verde) in enumerate(blocos):
        x = 36 + k * 278
        corpo += (
            f'<g class="in" style="animation-delay:{k * 0.12:.2f}s">'
            f'<rect x="{x}" y="66" width="258" height="84" rx="16" fill="#fff" fill-opacity=".6" stroke="{BORDA}" stroke-opacity=".8"/>'
            + bolha(x + 42, 108, 24, ic, verde=verde)
            + f'<text x="{x + 80}" y="102" class="big" style="font-size:24px">{txt(val)}</text>'
            f'<text x="{x + 80}" y="126" class="s">{txt(rot)}</text></g>'
        )
    return base(880, 172, "Constância", "timeline", corpo)


def atividade_card(u):
    ds = dias(u)[-31:]
    W, H = 880, 290
    esq, dir_, topo, fundo = 56, 36, 76, 236
    mx = max([d["contributionCount"] for d in ds] + [1])
    passo = (W - esq - dir_) / (len(ds) - 1)
    pts = [(esq + i * passo, fundo - (fundo - topo) * d["contributionCount"] / mx) for i, d in enumerate(ds)]
    linha = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"{esq},{fundo} " + linha + f" {pts[-1][0]:.1f},{fundo}"
    grade = ""
    for k in range(5):
        y = fundo - (fundo - topo) * k / 4
        grade += f'<line x1="{esq}" y1="{y:.1f}" x2="{W - dir_}" y2="{y:.1f}" stroke="{BORDA}" stroke-opacity=".6"/>'
        grade += f'<text x="{esq - 10}" y="{y + 4:.1f}" class="s" text-anchor="end">{round(mx * k / 4)}</text>'
    rot = ""
    for i, d in enumerate(ds):
        if i % 3 == 0 or i == len(ds) - 1:
            dt = date.fromisoformat(d["date"])
            rot += f'<text x="{pts[i][0]:.1f}" y="{fundo + 22}" class="s" text-anchor="middle">{dt.day:02d}/{dt.month:02d}</text>'
    pontos = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#fff" stroke="{AQUA_3}" stroke-width="2"/>' for x, y in pts)
    corpo = (
        f'<defs><linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{AQUA_2}" stop-opacity=".45"/>'
        f'<stop offset="1" stop-color="{VERDE}" stop-opacity=".08"/></linearGradient></defs>'
        + grade
        + f'<polygon points="{area}" fill="url(#ar)"/>'
        + f'<polyline points="{linha}" fill="none" stroke="{AQUA_3}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
        + pontos + rot
        + f'<text x="{W - 36}" y="44" class="s" text-anchor="end">últimos 31 dias</text>'
    )
    return base(W, H, "Atividade de contribuições", "insights", corpo)


def main():
    u = fetch()
    os.makedirs(OUT, exist_ok=True)
    for nome, conteudo in [
        ("stats.svg", stats_card(u)),
        ("linguagens.svg", langs_card(u)),
        ("sequencia.svg", sequencia_card(u)),
        ("atividade.svg", atividade_card(u)),
    ]:
        with open(os.path.join(OUT, nome), "w", encoding="utf-8") as f:
            f.write(conteudo)
        print("gerado", nome)


if __name__ == "__main__":
    main()
