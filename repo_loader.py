import os
import json

repos_json_path = './repos.json'

def save_repos(repos):
    with open(repos_json_path, 'w') as file:
        json.dump(repos, file, indent=4)

def load_repos():
    if os.path.exists(repos_json_path):
        with open(repos_json_path, 'r') as file:
            return json.load(file)
    return []
