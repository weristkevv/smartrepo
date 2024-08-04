import os
import stat
import shutil
from git import Repo

def remove_local_project(path, remove_write_protection=True):
    if os.path.exists(path):
        if remove_write_protection:
            def on_rm_error(func, path, exc_info):
                os.chmod(path, stat.S_IWRITE)
                os.unlink(path)
        else:
            on_rm_error = None

        shutil.rmtree(path, onerror=on_rm_error)

def clone_latest_repo(repo_url, clone_path):
    remove_local_project(clone_path)
    Repo.clone_from(repo_url, clone_path)
    print(f"Repository wurde erfolgreich in {clone_path} geklont.")
