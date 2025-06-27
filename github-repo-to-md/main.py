import requests
from urllib.parse import urlparse
import os

GITHUB_API = "https://api.github.com"

def extract_owner_repo(url):
    path = urlparse(url).path.strip("/").split("/")
    if len(path) < 2:
        raise ValueError("Invalid GitHub repo URL")
    return path[0], path[1]

def get_repo_info(owner, repo):
    resp = requests.get(f"{GITHUB_API}/repos/{owner}/{repo}")
    resp.raise_for_status()
    data = resp.json()
    return {
        "title": data["name"],
        "creator": data["owner"]["login"],
        "description": data.get("description", ""),
        "branch": data["default_branch"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "license": data["license"]["name"] if data.get("license") else None,
    }

def recurse_structure(owner, repo, branch, path="", indent=0):
    structure = []
    resp = requests.get(f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}?ref={branch}")
    resp.raise_for_status()
    for item in resp.json():
        item_path = item["path"]
        url = f"https://github.com/{owner}/{repo}/tree/{branch}/{item_path}"
        if item["type"] == "dir":
            structure.append(("  " * indent + f"{item['name']}/", None))
            structure.extend(recurse_structure(owner, repo, branch, item_path, indent + 1))
        else:
            structure.append(("  " * indent + f"{item['name']} -> {url}", item_path))
    return structure

def fetch_all_file_contents(owner, repo, branch, path=""):
    contents = []
    resp = requests.get(f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}?ref={branch}")
    resp.raise_for_status()
    for item in resp.json():
        if item["type"] == "file":
            file_resp = requests.get(item["download_url"])
            file_resp.raise_for_status()
            contents.append((item["path"], file_resp.text))
        elif item["type"] == "dir":
            contents.extend(fetch_all_file_contents(owner, repo, branch, item["path"]))
    return contents

def generate_markdown(repo_url):
    owner, repo = extract_owner_repo(repo_url)
    info = get_repo_info(owner, repo)
    structure = recurse_structure(owner, repo, info["branch"])
    contents = fetch_all_file_contents(owner, repo, info["branch"])

    md_lines = [
        f"# Repository Overview",
        f"**Repo link**: [{repo_url}]({repo_url})",
        f"**Repo title**: {info['title']}",
        f"**Creator**: {info['creator']}",
        f"**Description**: {info['description']}",
        f"**Default branch**: {info['branch']}",
        f"**Stars**: {info['stars']}",
        f"**Forks**: {info['forks']}",
        f"**License**: {info['license']}",
        "\n---\n",
        "## Directory structure:\n"
    ]

    for line, _ in structure:
        md_lines.append(f"- {line}")

    md_lines.append("\n---\n")
    md_lines.append("## Contents:\n")

    for path, code in contents:
        md_lines.append(f"### `{path}`\n")
        md_lines.append("```python" if path.endswith(".py") else "```")
        md_lines.append(code)
        md_lines.append("```\n")

    return "\n".join(md_lines)

# Replace this with any public GitHub repo URL
response = str(input(f"Enter the repo url in format 'https://github.com/user/repo'\n> "))
repo_url = response
markdown_output = generate_markdown(repo_url)

with open("repo_summary.md", "w", encoding="utf-8") as f:
    f.write(markdown_output)

print("✅ Markdown file 'repo_summary.md' generated successfully.")