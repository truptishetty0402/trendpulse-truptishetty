import requests
import pandas as pd

url = "https://api.github.com/search/repositories?q=created:>2024-01-01&sort=stars&order=desc"

response = requests.get(url)
data = response.json()

repos = []

for repo in data['items']:
    repos.append({
        "name": repo['name'],
        "owner": repo['owner']['login'],
        "stars": repo['stargazers_count'],
        "language": repo['language']
    })

df = pd.DataFrame(repos)

df.to_csv("trending_repos_raw.csv", index=False)

print("Data collected and saved as trending_repos_raw.csv")
