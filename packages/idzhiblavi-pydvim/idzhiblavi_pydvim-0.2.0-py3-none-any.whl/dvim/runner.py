import os
import subprocess
import contextlib
from contextlib import ExitStack


WORKSPACES_DIR = os.path.expanduser("~/.config/nvim/workspaces")
SESSIONS_DIR = os.path.expanduser("~/.local/share/nvim/sessions")
SOCKETS_DIR = os.path.expanduser("~/.cache/nvim/pipes")


class Runner:
    def __init__(self, debug, executable, workspace, session):
        self.debug = debug
        self.executable = executable
        self.workspace = workspace
        self.session = session

    def ui(self):
        socket_path = find_running_instance_socket_path(self.build_socket_prefix())
        check_socket_exists(socket_path)
        self.execute("--server", socket_path, "--remote-ui")

    def server(self):
        with ExitStack() as stack:
            socket_path = self.build_socket_path()
            stack.callback(lambda: cleanup_socket(socket_path))

            check_socket_does_not_exist(socket_path)
            self.execute("--listen", socket_path)

    def headless(self):
        with ExitStack() as stack:
            socket_path = self.build_socket_path()
            stack.callback(lambda: cleanup_socket(socket_path))

            check_socket_does_not_exist(socket_path)
            self.execute("--headless", "--listen", socket_path)

    def local(self):
        self.execute()

    def execute(self, *nvim_args):
        extra_env = dict()

        if self.workspace is not None:
            extra_env["NVIM_WS"] = self.workspace

        if self.session is not None:
            extra_env["NVIM_SES"] = self.session

        run(
            [
                self.executable,
                *nvim_args,
            ],
            extra_env,
            self.debug,
        )

    def build_socket_prefix(self):
        return f"{self.workspace or ''}"

    def build_socket_path(self):
        return os.path.join(SOCKETS_DIR, f"{self.workspace or ''}.server.pipe")


def cleanup_socket(socket_path):
    with contextlib.suppress(FileNotFoundError):
        os.remove(socket_path)


def run(cmd, extra_env, debug):
    if debug:
        print(extra_env, cmd)
    else:
        subprocess.run(cmd, env=dict(os.environ) | extra_env)


def find_running_instance_socket_path(socket_prefix):
    print(f"prefix: {socket_prefix}")
    sockets = [
        os.path.join(SOCKETS_DIR, path)
        for path in os.listdir(SOCKETS_DIR)
        if path.startswith(socket_prefix)
    ]

    if not sockets:
        raise RuntimeError("Failed to find a running server")
    elif len(sockets) == 1:
        return sockets[0]
    else:
        return choose_one_of(sockets)


def choose_one_of(items):
    import inquirer

    answers = (
        inquirer.prompt(
            [
                inquirer.List(
                    "chosen",
                    message="Choose the running instance",
                    choices=items,
                ),
            ]
        )
        or {}
    )

    return answers["chosen"]


def check_socket_exists(socket_path):
    if not os.path.exists(socket_path):
        raise RuntimeError(f"socket does not exist on {socket_path}")


def check_socket_does_not_exist(socket_path):
    if os.path.exists(socket_path):
        raise RuntimeError(f"socket already exists on {socket_path}")
