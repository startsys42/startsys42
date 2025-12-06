import requests

USER = "starsys42"

# Obtener todos los repos públicos
repos = requests.get(f"https://api.github.com/users/{USER}/repos").json()
url = f"https://api.github.com/search/issues?q=author:{USER}+type:pr"


# Totales
repos_publicos = [r for r in repos if not r["private"]]
total_stars = sum(r["stargazers_count"] for r in repos_publicos)
total_forks = sum(r["forks_count"] for r in repos_publicos)
total_watchers = sum(r["watchers_count"] for r in repos_publicos)
total_issues = sum(r["open_issues_count"] for r in repos_publicos)


total_repos = len(repos_publicos)

# Top 5 por estrellas
top5_stars = sorted(repos_publicos, key=lambda r: r["stargazers_count"], reverse=True)[:5]
# Top 5 por forks
top5_forks = sorted(repos_publicos, key=lambda r: r["forks_count"], reverse=True)[:5]

# Top 5 por seguidores (watchers)
top5_followers = sorted(repos_publicos, key=lambda r: r["watchers_count"], reverse=True)[:5]

# pull requests

total_prs = 0
for r in repos_publicos:
    prs = requests.get(f"https://api.github.com/repos/{USER}/{r['name']}/pulls?state=all&per_page=100").json()
    total_prs += len(prs)

search = requests.get(url).json()
total_prs_creados = search['total_count']


# Top 5 por issues abiertas
top5_issues = sorted(repos_publicos, key=lambda r: r["open_issues_count"], reverse=True)[:5]

# Datos de usuario públicos
user = requests.get(f"https://api.github.com/users/{USER}").json()
followers = user["followers"]
total_public_repos = user["public_repos"]

# Mermaid gráfico top 5 stars
mermaid_stars = "```mermaid\npie\ntitle Top 5 repos por estrellas\n"
for r in top5_stars:
    mermaid_stars += f'"{r["name"]}" : {r["stargazers_count"]}\n'
mermaid_stars += "```\n"

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

stats_block = f"""
<!-- STATS_START -->
- Total de stars: {total_stars}
- Total de forks: {total_forks}
- Total de watchers: {total_watchers}
- Total de issues abiertas: {total_issues}
- Total PRs en mis repos: {total_prs}
- Total PRs creados: {total_prs_creados}
- Seguidores del perfil: {followers}
- Total de repos públicos: {total_public_repos}

## Top 5 repos por estrellas
{mermaid_stars}
## Top 5 repos por forks
{mermaid_forks}
## Top 5 repos por issues
{mermaid_issues}
## Top 5 repos por seguidores
{mermaid_followers}
<!-- STATS_END -->
"""

import re
readme = re.sub(r'<!-- STATS_START -->.*<!-- STATS_END -->', stats_block, readme, flags=re.DOTALL)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)
