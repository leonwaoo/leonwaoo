"""Gera os cards de dados do perfil (estatísticas, linguagens e atividade).

Roda no GitHub Actions. Usa a API GraphQL do GitHub com o token em GH_TOKEN
e grava os SVGs em dist/.
"""
import json
import os
import urllib.request
from datetime import date

from estilo import P, BG, BORDA, ESCALA, F, CLARO, ACENTO, ACENTO_CLARO, SUAVE, svg, txt, T, tam

USER = os.environ.get("GH_USER", "leonwaoo")
TOKEN = os.environ.get("GH_TOKEN", "")
OUT = "dist"

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
    f".t{{font:800 {tam(17)} {T};fill:{ACENTO_CLARO}}}.l{{font:600 13.5px {F};fill:{SUAVE}}}"
    f".v{{font:800 13.5px {F};fill:{CLARO}}}.big{{font:900 28px {F};fill:{CLARO}}}"
    f".s{{font:700 11px {F};fill:{SUAVE}}}"
    ".in{opacity:0;animation:in .6s ease forwards}@keyframes in{to{opacity:1}}"
)


def card(w, h, titulo, corpo):
    c = (
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="{BG}" stroke="{BORDA}"/>'
        f'<text x="24" y="36" class="t">{txt(titulo)}</text>{corpo}'
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
        y = 70 + i * 25
        corpo += (
            f'<g class="in" style="animation-delay:{i * 0.12:.2f}s"><circle cx="30" cy="{y - 4}" r="3.5" fill="{ACENTO}"/>'
            f'<text x="44" y="{y}" class="l">{txt(rotulo)}</text><text x="290" y="{y}" class="v" text-anchor="end">{fmt(val)}</text></g>'
        )
    cx, cy, r = 395, 108, 50
    corpo += (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BORDA}" stroke-width="8"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ACENTO}" stroke-width="8" stroke-linecap="round" '
        f'stroke-dasharray="{2 * 3.1416 * r:.1f}" transform="rotate(-90 {cx} {cy})"/>'
        f'<text x="{cx}" y="{cy + 9}" class="big" text-anchor="middle">{fmt(total)}</text>'
        f'<text x="{cx}" y="{cy + r + 24}" class="s" text-anchor="middle">contribuições no ano</text>'
    )
    return card(495, 195, "Estatísticas no GitHub", corpo)


def langs_card(u):
    totais = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            totais[e["node"]["name"]] = totais.get(e["node"]["name"], 0) + e["size"]
    top = sorted(totais.items(), key=lambda x: -x[1])[:6]
    soma = sum(v for _, v in top) or 1
    x, barra = 24, ""
    for i, (_, v) in enumerate(top):
        w = 302 * v / soma
        barra += f'<rect x="{x:.1f}" y="54" width="{max(w, 2):.1f}" height="10" fill="{ESCALA[i]}"/>'
        x += w
    corpo = f'<clipPath id="cb"><rect x="24" y="54" width="302" height="10" rx="5"/></clipPath><g clip-path="url(#cb)">{barra}</g>'
    for i, (nome, v) in enumerate(top):
        col, row = i % 2, i // 2
        lx, ly = 24 + col * 162, 96 + row * 28
        corpo += (
            f'<g class="in" style="animation-delay:{i * 0.12:.2f}s"><circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{ESCALA[i]}"/>'
            f'<text x="{lx + 16}" y="{ly}" class="v">{txt(nome)}</text>'
            f'<text x="{lx + 136}" y="{ly}" class="l" text-anchor="end">{100 * v / soma:.1f}%</text></g>'
        )
    return card(350, 195, "Linguagens mais usadas", corpo)


def atividade_card(u):
    ds = dias(u)[-31:]
    W, H = 880, 280
    esq, dir_, topo, fundo = 50, 30, 64, 230
    mx = max([d["contributionCount"] for d in ds] + [1])
    passo = (W - esq - dir_) / (len(ds) - 1)
    pts = [(esq + i * passo, fundo - (fundo - topo) * d["contributionCount"] / mx) for i, d in enumerate(ds)]
    linha = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"{esq},{fundo} " + linha + f" {pts[-1][0]:.1f},{fundo}"
    grade = ""
    for k in range(5):
        y = fundo - (fundo - topo) * k / 4
        grade += f'<line x1="{esq}" y1="{y:.1f}" x2="{W - dir_}" y2="{y:.1f}" stroke="{BORDA}"/>'
        grade += f'<text x="{esq - 10}" y="{y + 4:.1f}" class="s" text-anchor="end">{round(mx * k / 4)}</text>'
    rot = ""
    for i, d in enumerate(ds):
        if i % 3 == 0 or i == len(ds) - 1:
            dt = date.fromisoformat(d["date"])
            rot += f'<text x="{pts[i][0]:.1f}" y="{fundo + 22}" class="s" text-anchor="middle">{dt.day:02d}/{dt.month:02d}</text>'
    pontos = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{CLARO}"/>' for x, y in pts)
    corpo = (
        f'<defs><linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ACENTO}" stop-opacity=".45"/>'
        f'<stop offset="1" stop-color="{ACENTO}" stop-opacity="0"/></linearGradient></defs>'
        + grade
        + f'<polygon points="{area}" fill="url(#a)"/>'
        + f'<polyline points="{linha}" fill="none" stroke="{ACENTO}" stroke-width="2.5" stroke-linejoin="round"/>'
        + pontos + rot
        + f'<text x="{W - 24}" y="36" class="s" text-anchor="end">últimos 31 dias</text>'
    )
    return card(W, H, "Atividade de contribuições", corpo)


def main():
    u = fetch()
    os.makedirs(OUT, exist_ok=True)
    for nome, conteudo in [
        ("stats.svg", stats_card(u)),
        ("linguagens.svg", langs_card(u)),
        ("atividade.svg", atividade_card(u)),
    ]:
        with open(os.path.join(OUT, nome), "w", encoding="utf-8") as f:
            f.write(conteudo)
        print("gerado", nome)


if __name__ == "__main__":
    main()
