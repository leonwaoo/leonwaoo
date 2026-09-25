"""Gera os cards SVG do perfil (estatísticas, linguagens e atividade).

Roda no GitHub Actions. Usa a API GraphQL do GitHub com o token disponível
em GH_TOKEN e grava os arquivos em dist/.
"""
import json
import os
import urllib.request
from datetime import date

USER = os.environ.get("GH_USER", "leonwaoo")
TOKEN = os.environ["GH_TOKEN"]
OUT = "dist"

BG = "#0d1117"
BORDER = "#2a1a4a"
TITLE = "#c084fc"
TEXT = "#e9d5ff"
MUTED = "#9ca3af"
ACCENT = "#a855f7"
SHADES = ["#a855f7", "#c084fc", "#7c3aed", "#e9d5ff", "#6d28d9", "#d8b4fe", "#5b21b6", "#f5f3ff"]
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Sans-Serif"

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch():
    body = json.dumps({"query": QUERY, "variables": {"login": USER}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"Erro na API: {data['errors']}")
    return data["data"]["user"]


def fmt(n):
    return f"{n:,}".replace(",", ".")


def card(width, height, title, inner):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{title}">
<style>
  .t {{ font: 600 17px {FONT}; fill: {TITLE}; }}
  .l {{ font: 400 13px {FONT}; fill: {MUTED}; }}
  .v {{ font: 700 13px {FONT}; fill: {TEXT}; }}
  .big {{ font: 700 26px {FONT}; fill: {TEXT}; }}
  .s {{ font: 400 11px {FONT}; fill: {MUTED}; }}
  .fade {{ opacity: 0; animation: in .6s ease forwards; }}
  @keyframes in {{ to {{ opacity: 1; }} }}
</style>
<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="{BG}" stroke="{BORDER}"/>
<text x="24" y="36" class="t">{title}</text>
{inner}
</svg>
"""


def stats_card(u):
    c = u["contributionsCollection"]
    repos = u["repositories"]
    stars = sum(n["stargazerCount"] for n in repos["nodes"])
    total = c["contributionCalendar"]["totalContributions"]
    rows = [
        ("Commits no último ano", c["totalCommitContributions"]),
        ("Pull requests", c["totalPullRequestContributions"]),
        ("Issues", c["totalIssueContributions"]),
        ("Repositórios públicos", repos["totalCount"]),
        ("Estrelas recebidas", stars),
    ]
    inner = ""
    for i, (label, val) in enumerate(rows):
        y = 70 + i * 25
        inner += (
            f'<g class="fade" style="animation-delay:{i * 120}ms">'
            f'<circle cx="30" cy="{y - 4}" r="3.5" fill="{ACCENT}"/>'
            f'<text x="44" y="{y}" class="l">{label}</text>'
            f'<text x="290" y="{y}" class="v" text-anchor="end">{fmt(val)}</text></g>'
        )
    # anel com o total de contribuições
    cx, cy, r = 395, 108, 50
    inner += (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BORDER}" stroke-width="8"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ACCENT}" stroke-width="8" '
        f'stroke-linecap="round" stroke-dasharray="{2 * 3.1416 * r:.1f}" '
        f'transform="rotate(-90 {cx} {cy})"/>'
        f'<text x="{cx}" y="{cy + 8}" class="big" text-anchor="middle">{fmt(total)}</text>'
        f'<text x="{cx}" y="{cy + r + 24}" class="s" text-anchor="middle">contribuições no ano</text>'
    )
    return card(495, 195, "Estatísticas no GitHub", inner)


def langs_card(u):
    totals = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            totals[e["node"]["name"]] = totals.get(e["node"]["name"], 0) + e["size"]
    top = sorted(totals.items(), key=lambda x: -x[1])[:6]
    soma = sum(v for _, v in top) or 1
    x, bar = 24, ""
    for i, (name, v) in enumerate(top):
        w = 302 * v / soma
        bar += f'<rect x="{x:.1f}" y="54" width="{max(w, 2):.1f}" height="10" fill="{SHADES[i]}"/>'
        x += w
    bar = (
        '<clipPath id="c"><rect x="24" y="54" width="302" height="10" rx="5"/></clipPath>'
        f'<g clip-path="url(#c)">{bar}</g>'
    )
    legend = ""
    for i, (name, v) in enumerate(top):
        col, row = i % 2, i // 2
        lx, ly = 24 + col * 162, 96 + row * 28
        legend += (
            f'<g class="fade" style="animation-delay:{i * 120}ms">'
            f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{SHADES[i]}"/>'
            f'<text x="{lx + 16}" y="{ly}" class="v">{name}</text>'
            f'<text x="{lx + 136}" y="{ly}" class="l" text-anchor="end">{100 * v / soma:.1f}%</text></g>'
        )
    return card(350, 195, "Linguagens mais usadas", bar + legend)


def activity_card(u):
    days = [d for w in u["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    days = days[-31:]
    W, H = 880, 280
    left, right, top, bottom = 50, 30, 64, 230
    mx = max([d["contributionCount"] for d in days] + [1])
    step = (W - left - right) / (len(days) - 1)
    pts = [
        (left + i * step, bottom - (bottom - top) * d["contributionCount"] / mx)
        for i, d in enumerate(days)
    ]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"{left},{bottom} " + line + f" {pts[-1][0]:.1f},{bottom}"
    grid = ""
    for k in range(5):
        y = bottom - (bottom - top) * k / 4
        grid += f'<line x1="{left}" y1="{y:.1f}" x2="{W - right}" y2="{y:.1f}" stroke="{BORDER}"/>'
        grid += f'<text x="{left - 10}" y="{y + 4:.1f}" class="s" text-anchor="end">{round(mx * k / 4)}</text>'
    labels = ""
    for i, d in enumerate(days):
        if i % 3 == 0 or i == len(days) - 1:
            dt = date.fromisoformat(d["date"])
            labels += f'<text x="{pts[i][0]:.1f}" y="{bottom + 22}" class="s" text-anchor="middle">{dt.day:02d}/{dt.month:02d}</text>'
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{TEXT}"/>' for x, y in pts)
    inner = (
        '<defs><linearGradient id="a" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{ACCENT}" stop-opacity=".45"/>'
        f'<stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></linearGradient></defs>'
        + grid
        + f'<polygon points="{area}" fill="url(#a)"/>'
        + f'<polyline points="{line}" fill="none" stroke="{ACCENT}" stroke-width="2.5" stroke-linejoin="round"/>'
        + dots
        + labels
        + f'<text x="{W - 24}" y="36" class="s" text-anchor="end">últimos 31 dias</text>'
    )
    return card(W, H, "Atividade de contribuições", inner)


def main():
    u = fetch()
    os.makedirs(OUT, exist_ok=True)
    for nome, svg in [
        ("stats.svg", stats_card(u)),
        ("linguagens.svg", langs_card(u)),
        ("atividade.svg", activity_card(u)),
    ]:
        with open(os.path.join(OUT, nome), "w", encoding="utf-8") as f:
            f.write(svg)
        print("gerado", nome)


if __name__ == "__main__":
    main()
