import requests


def make_mermaid_pie(title, items, key, total_value):
    mermaid = f"```mermaid\npie\ntitle {title}\n"

    # Top 5
    for r in items:
        value = r[key]
        percentage = round((value / total_value) * 100, 2) if total_value else 0
        mermaid += f'"{r["name"]} ({percentage}%)" : {value}\n'

    # Resto agrupado
    others_value = total_value - sum(r[key] for r in items)
    if others_value > 0:
        percentage = round((others_value / total_value) * 100, 2)
        mermaid += f'"Otros ({percentage}%)" : {others_value}\n'

    mermaid += "```\n"
    return mermaid


USER = "starsys42"

# Obtener todos los repos públicos
repos = requests.get(f"https://api.github.com/users/{USER}/repos").json()



# Totales repos públicos estrellas, forks y seguidores de repos
repos_publicos = [r for r in repos if not r["private"]]
total_repos = len(repos_publicos)
total_stars = sum(r["stargazers_count"] for r in repos_publicos)
total_forks = sum(r["forks_count"] for r in repos_publicos)
total_watchers = sum(r["watchers_count"] for r in repos_publicos)

# Top 5 por estrellas
top5_stars = sorted(repos_publicos, key=lambda r: r["stargazers_count"], reverse=True)[:5]
# Top 5 por forks
top5_forks = sorted(repos_publicos, key=lambda r: r["forks_count"], reverse=True)[:5]

# Top 5 por seguidores (watchers)
top5_followers = sorted(repos_publicos, key=lambda r: r["watchers_count"], reverse=True)[:5]




# Pull requests

all_prs = []

for r in repos_publicos:
    repo_name = r["name"]
    page = 1
    while True:
        url = f"https://api.github.com/repos/{USER}/{repo_name}/pulls?state=all&per_page=100&page={page}"
        prs = requests.get(url).json()
        if not prs:  # Si no hay más resultados, salimos
            break
        all_prs.extend(prs)
        page += 1


pr enmis repos mios de otros aceptados rechazados, pr en otrs repos,,...

quiero contar en mis repos públicos  el total de pr ,
el total de pr  abiertos y cerrados, el  total de mis pr en 
mis propios repos  publcios,  el total de mis pr  en mis repos abiertos y el ottal de mis pr en mis repos cerrados, el total de pr de otros en mis repos publicos, el total de pr de otros en mis repos cerrados y el total
de pr abiertos de otros en mis repos publicos, ademas quiero saber el total de pr mios en repos de otros  y el total de mis pr abiertos en repos de otros, el total de mis pr en repos de otros  cerrados y de los cerrados el nuemro de rechazads y el nuemro de aceptados


# Inicializamos contadores
total_prs_my_repos = len(all_prs)
total_prs_open_my_repos =  sum(1 for pr in all_prs if pr["state"]=="open")
total_prs_closed_my_repos = sum(1 for pr in all_prs if pr["state"]=="closed")

my_prs = 0
my_prs_open = 0
my_prs_closed = 0

others_prs = 0
others_prs_open = 0
others_prs_closed = 0

# PRs en mis repos
for r in repos_publicos:
    repo_name = r["name"]
    prs = requests.get(f"https://api.github.com/repos/{USER}/{repo_name}/pulls?state=all&per_page=100").json()
    
    total_prs += len(prs)
    total_prs_open += sum(1 for pr in prs if pr["state"]=="open")
    total_prs_closed += sum(1 for pr in prs if pr["state"]=="closed")
    
    my_prs += sum(1 for pr in prs if pr["user"]["login"]==USER)
    my_prs_open += sum(1 for pr in prs if pr["user"]["login"]==USER and pr["state"]=="open")
    my_prs_closed += sum(1 for pr in prs if pr["user"]["login"]==USER and pr["state"]=="closed")
    
    others_prs += sum(1 for pr in prs if pr["user"]["login"]!=USER)
    others_prs_open += sum(1 for pr in prs if pr["user"]["login"]!=USER and pr["state"]=="open")
    others_prs_closed += sum(1 for pr in prs if pr["user"]["login"]!=USER and pr["state"]=="closed")

# Mis PRs en repos de otros (búsqueda global)
url = f"https://api.github.com/search/issues?q=type:pr+author:{USER}+state:all"
search_all = requests.get(url).json()
my_prs_others_total = search_all['total_count']

url_open = f"https://api.github.com/search/issues?q=type:pr+author:{USER}+state:open"
search_open = requests.get(url_open).json()
my_prs_others_open = search_open['total_count']

url_closed = f"https://api.github.com/search/issues?q=type:pr+author:{USER}+state:closed"
search_closed = requests.get(url_closed).json()
my_prs_others_closed = search_closed['total_count']

# Para saber cuántas fueron aceptadas o rechazadas
url_closed_details = f"https://api.github.com/search/issues?q=type:pr+author:{USER}+state:closed&per_page=100"
closed_prs = requests.get(url_closed_details).json()['items']

my_prs_others_merged = sum(1 for pr in closed_prs if pr.get("pull_request") and requests.get(pr["pull_request"]["url"]).json().get("merged_at"))
my_prs_others_rejected = my_prs_others_closed - my_prs_others_merged

# Mostrar
print("=== PRs en mis repos ===")
print(f"Total PRs: {total_prs}, Abiertas: {total_prs_open}, Cerradas: {total_prs_closed}")
print(f"Mis PRs: {my_prs}, Abiertas: {my_prs_open}, Cerradas: {my_prs_closed}")
print(f"PRs de otros: {others_prs}, Abiertas: {others_prs_open}, Cerradas: {others_prs_closed}")

print("=== Mis PRs en repos de otros ===")
print(f"Total: {my_prs_others_total}, Abiertas: {my_prs_others_open}, Cerradas: {my_prs_others_closed}")
print(f"Aceptadas: {my_prs_others_merged}, Rechazadas: {my_prs_others_rejected}")



# Commits
quiero saber el neurmod e commits hechos por mi enr epos ajenos, os commits hechos por mi en mis repos totales, commits hechos por otros en mis repos, commits totales en mis repos propis y de otros
# issues

url = f"https://api.github.com/search/issues?q=author:{USER}+type:pr"

total_issues = sum(r["open_issues_count"] for r in repos_publicos)

-total issus , total issues abeirtos,c erradios
total issues top 5 
total issues en otros repso d eotrsio

# lienas

#idioams 

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


# Mermaid gráfico top 5 stars
mermaid_stars = make_mermaid_pie(
    "Distribución de estrellas (Top 5 + Otros)",
    top5_stars,
    "stargazers_count",
    total_stars
)


mermaid_forks = make_mermaid_pie(
    "Distribución de forks (Top 5 + Otros)",
    top5_forks,
    "forks_count",
    total_forks
)

mermaid_followers = make_mermaid_pie(
    "Distribución de watchers (Top 5 + Otros)",
    top5_followers,
    "watchers_count",
    total_watchers
)



with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

stats_block = f"""
<!-- STATS_START -->
- Seguidores del perfil: {followers}
- Total de repos públicos: {total_public_repos}
- Total de stars: {total_stars}
- Total de forks: {total_forks}
- Total de watchers: {total_watchers}
- Total de issues abiertas: {total_issues}
- Total PRs en mis repos: {total_prs}
- Total PRs creados: {total_prs_creados}



## Top 5 repos por estrellas
{mermaid_stars}
## Top 5 repos por forks
{mermaid_forks}
## Top 5 repos por seguidores
{mermaid_followers}


## Top 5 repos por issues
{mermaid_issues}
<!-- STATS_END -->
"""

import re
readme = re.sub(r'<!-- STATS_START -->.*<!-- STATS_END -->', stats_block, readme, flags=re.DOTALL)

with open("READMEE.md", "w", encoding="utf-8") as f:
    f.write(readme)
