import curses
import repo_loader
import repo_manager

TITLE = """
\_______               __  ___              
  / __/_ _  ___ _____/ /_/ _ \\___ ___  ___ 
 _\\ \\/  ' \\/ _ `/ __/ __/ , _/ -_) _ \\/ _ \\
/___/_/_/_/\\_,_/_/  \\__/_/|_|\\__/ .__/\\___/
                       /_/         
"""

def draw_menu(stdscr, current_row, menu, enabled):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    box_width = max(len(item) for item in menu) + 4
    box_height = len(menu) + 4

    box_top_left_x = (width - box_width) // 2
    box_top_left_y = (height - box_height) // 2 + len(TITLE.strip().split('\n')) + 2

    for i, line in enumerate(TITLE.strip().split('\n')):
        stdscr.addstr(i, (width // 2) - (len(line) // 2), line, curses.color_pair(3))

    stdscr.addstr(box_top_left_y, box_top_left_x, "╔" + "═" * (box_width - 2) + "╗")
    for i in range(box_height - 2):
        stdscr.addstr(box_top_left_y + i + 1, box_top_left_x, "║")
        stdscr.addstr(box_top_left_y + i + 1, box_top_left_x + box_width - 1, "║")
    stdscr.addstr(box_top_left_y + box_height - 1, box_top_left_x, "╚" + "═" * (box_width - 2) + "╝")

    for idx, row in enumerate(menu):
        x = box_top_left_x + 2
        y = box_top_left_y + 2 + idx
        if idx == current_row:
            stdscr.addstr(y, x, row, curses.A_REVERSE)
        elif not enabled[idx]:
            stdscr.addstr(y, x, row, curses.color_pair(2))
        else:
            stdscr.addstr(y, x, row)

def get_new_repo_input(stdscr):
    height, width = stdscr.getmaxyx()
    box_width = 70
    box_height = 7
    box_top_left_x = (width - box_width) // 2
    box_top_left_y = (height - box_height) // 2

    stdscr.clear()
    stdscr.addstr(box_top_left_y, box_top_left_x, "╔" + "═" * (box_width - 2) + "╗")
    for i in range(box_height - 2):
        stdscr.addstr(box_top_left_y + i + 1, box_top_left_x, "║")
        stdscr.addstr(box_top_left_y + i + 1, box_top_left_x + box_width - 1, "║")
    stdscr.addstr(box_top_left_y + box_height - 1, box_top_left_x, "╚" + "═" * (box_width - 2) + "╝")

    stdscr.addstr(box_top_left_y + 2, box_top_left_x + 2, "- [URL] >> ")
    curses.echo()
    url = stdscr.getstr(box_top_left_y + 2, box_top_left_x + 12, 50).decode('utf-8').strip()
    stdscr.addstr(box_top_left_y + 3, box_top_left_x + 2, "- [PATH] >> ")
    path = stdscr.getstr(box_top_left_y + 3, box_top_left_x + 12, 50).decode('utf-8').strip()
    curses.noecho()

    if not url or not path:
        return None
    return {"url": url, "path": path}

def menu(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    current_row = 0

    while True:
        repos = repo_loader.load_repos()
        menu = ["- [ADD] >", "- [DEL] >", "- [EXE] >", "- [EXT] >"]
        enabled = [True, bool(repos), bool(repos), True]
        
        draw_menu(stdscr, current_row, menu, enabled)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0 and enabled[current_row]:
                new_repo = get_new_repo_input(stdscr)
                if new_repo:
                    repos.append(new_repo)
                    repo_loader.save_repos(repos)
            elif current_row == 1 and enabled[current_row]:
                delete_repo_menu(stdscr)
            elif current_row == 2 and enabled[current_row]:
                execute_repo_menu(stdscr)
            elif current_row == 3:
                break
        stdscr.refresh()

def delete_repo_menu(stdscr):
    repos = repo_loader.load_repos()
    current_row = 0
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        stdscr.addstr(0, width // 2 - 7, "Delete Repo", curses.A_BOLD | curses.color_pair(1))

        box_width = max(len(repo['url']) + len(repo['path']) + 7 for repo in repos) + 4
        box_height = len(repos) + 4

        box_top_left_x = (width - box_width) // 2
        box_top_left_y = (height - box_height) // 2

        stdscr.addstr(box_top_left_y, box_top_left_x, "╔" + "═" * (box_width - 2) + "╗")
        for i in range(box_height - 2):
            stdscr.addstr(box_top_left_y + i + 1, box_top_left_x, "║")
            stdscr.addstr(box_top_left_y + i + 1, box_top_left_x + box_width - 1, "║")
        stdscr.addstr(box_top_left_y + box_height - 1, box_top_left_x, "╚" + "═" * (box_width - 2) + "╝")

        for idx, repo in enumerate(repos):
            row = f"{idx + 1}. {repo['url']} -> {repo['path']}"
            x = box_top_left_x + 2
            y = box_top_left_y + 2 + idx
            if idx == current_row:
                stdscr.addstr(y, x, row, curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, row)

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(repos) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            repo_manager.remove_local_project(repos[current_row]["path"])
            repos.pop(current_row)
            repo_loader.save_repos(repos)
            break
        elif key == 27:
            break
        stdscr.refresh()

def execute_repo_menu(stdscr):
    repos = repo_loader.load_repos()
    current_row = 0
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        stdscr.addstr(0, width // 2 - 8, "Execute Script", curses.A_BOLD | curses.color_pair(1))

        box_width = max(len(repo['url']) + len(repo['path']) + 7 for repo in repos) + 4
        box_height = len(repos) + 4

        box_top_left_x = (width - box_width) // 2
        box_top_left_y = (height - box_height) // 2

        stdscr.addstr(box_top_left_y, box_top_left_x, "╔" + "═" * (box_width - 2) + "╗")
        for i in range(box_height - 2):
            stdscr.addstr(box_top_left_y + i + 1, box_top_left_x, "║")
            stdscr.addstr(box_top_left_y + i + 1, box_top_left_x + box_width - 1, "║")
        stdscr.addstr(box_top_left_y + box_height - 1, box_top_left_x, "╚" + "═" * (box_width - 2) + "╝")

        for idx, repo in enumerate(repos):
            row = f"{idx + 1}. {repo['url']} -> {repo['path']}"
            x = box_top_left_x + 2
            y = box_top_left_y + 2 + idx
            if idx == current_row:
                stdscr.addstr(y, x, row, curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, row)

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(repos) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            repo_manager.execute_script(repos[current_row])
            break
        elif key == 27:
            break
        stdscr.refresh()

def main(stdscr):
    curses.wrapper(menu)

if __name__ == "__main__":
    curses.wrapper(main)
