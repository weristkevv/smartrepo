import repo_cloner

def remove_local_project(path):
    repo_cloner.remove_local_project(path)

def execute_script(repo):
    project_path = repo['path']
    remove_local_project(project_path)
    repo_cloner.clone_latest_repo(repo['url'], project_path)
