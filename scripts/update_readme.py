import requests

USER = "starsys42"

# Obtener todos los repos públicos
repos = requests.get(f"https://api.github.com/users/{USER}/repos").json()

# Totales
repos_publicos = [r for r in repos if not r["private"]]
total_stars = sum(r["stargazers_count"] for r in repos_publicos)
total_forks = sum(r["forks_count"] for r in repos_publicos)
total_issues = sum(r["open_issues_count"] for r in repos_publicos)
total_repos = len(repos_publicos)

# Top 5 por estrellas
top5_stars = sorted(repos_publicos, key=lambda r: r["stargazers_count"], reverse=True)[:5]
# Top 5 por forks
top5_forks = sorted(repos_publicos, key=lambda r: r["forks_count"], reverse=True)[:5]

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

# Escribir README
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"# Estadísticas públicas de GitHub de {USER}\n\n")
    f.write(f"- Total de stars: {total_stars}\n")
    f.write(f"- Total de forks: {total_forks}\n")
    f.write(f"- Total de issues abiertas: {total_issues}\n")
    f.write(f"- Total de repos públicos: {total_repos}\n")
    f.write(f"- Seguidores: {followers}\n\n")
    f.write("## Top 5 repos públicos por estrellas\n")
    f.write(mermaid_stars)
