import os, sys, subprocess, pathlib, textwrap
PROJECT = "/workspaces/GregDavies91"
HERMES_HOME = pathlib.Path.home() / ".hermes"
ENV_FILE = HERMES_HOME / ".env"
CONFIG_FILE = HERMES_HOME / "config.yaml"
TOKEN_FILE = HERMES_HOME / ".session_token"
SHELL_RC = pathlib.Path.home() / ".bashrc"
PORT = "9119"
def run(cmd: str) -> subprocess.CompletedProcess:
    print(f"$ {cmd}")
    return subprocess.run(cmd, shell=True, check=False, text=True, capture_output=True)
def main() -> int:
    print("Setting up Hermes Codespace gateway...\n")
    HERMES_HOME.mkdir(parents=True, exist_ok=True)
    if not TOKEN_FILE.exists():
        token = subprocess.check_output(
            ["python3", "-c", "import secrets; print(secrets.token_urlsafe(32))"],
            text=True,
        ).strip()
        TOKEN_FILE.write_text(token, encoding="utf-8")
    else:
        token = TOKEN_FILE.read_text(encoding="utf-8").strip()
    if ENV_FILE.exists():
        env = {}
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    else:
        env = {}
    for k, v in {
        "HERMES_PROJECT_PATH": PROJECT,
        "HERMES_TERMINAL_BACKEND": "local",
        "SHELL": "/bin/bash",
        "HERMES_DASHBOARD_HOST": "0.0.0.0",
        "HERMES_DASHBOARD_PORT": PORT,
        "HERMES_DASHBOARD_SESSION_TOKEN": token,
    }.items():
        env.setdefault(k, v)
        os.environ.setdefault(k, v)
    lines = [f"{k}={v}" for k, v in sorted(env.items()) if k]
    ENV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    CONFIG_FILE.write_text(
        textwrap.dedent(f"""\
        terminal:
          backend: local
        projects:
          - path: {PROJECT}
            name: GregDavies91
        """),
        encoding="utf-8",
    )
    marker = "# >>> Hermes Codespace gateway setup >>>"
    rc = SHELL_RC.read_text(encoding="utf-8") if SHELL_RC.exists() else ""
    if marker not in rc:
        with SHELL_RC.open("a", encoding="utf-8") as f:
            f.write(
                textwrap.dedent(f"""
                {marker}
                export HERMES_PROJECT_PATH={PROJECT}
                export HERMES_TERMINAL_BACKEND=local
                export SHELL=/bin/bash
                export HERMES_DASHBOARD_HOST=0.0.0.0
                export HERMES_DASHBOARD_PORT={PORT}
                export HERMES_DASHBOARD_SESSION_TOKEN={token}
                # <<< Hermes Codespace gateway setup <<<
                """) + "\n"
            )
    start_cmd = f"hermes dashboard --host 0.0.0.0 --port {PORT} --insecure --tui --no-open"
    print("Setup complete.")
    print("Next:\n")
    print("  source ~/.bashrc")
    print("  " + start_cmd)
    print("\nThen expose port 9119 in Codespaces.")
    run("hermes status")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())