# 🚀 Hermes Agent in GitHub Codespaces

A lightweight, **Docker-free** environment for running [Hermes Agent](https://github.com/NousResearch/hermes-agent) inside GitHub Codespaces, with remote access from the **Hermes Desktop App**.

---

## 📁 Repo Layout

```text
/workspaces/GregDavies91/
├── requirements.txt  # Python dependencies
├── setup.py          # Writes ~/.hermes config and shell exports
├── .gitignore        # Prevents committing ~/.hermes/.env
└── README.md         # This file

~/.hermes/                 # Created by setup.py
├── .env                    # Session token + provider keys
├── config.yaml             # terminal.backend: local
└── .session_token          # Persistent dashboard token
```

---

## ⚡ Setup

### 1. Open a Codespace Terminal
Open the terminal in your Codespace (`Ctrl + `` ` / `Cmd + `` `).

---

### 2. Install Dependencies
```bash
pip install -r requirements.txt
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

---

### 3. Authenticate Modal
```bash
modal setup
```
Follow the printed link to authorize Codespaces with Modal.  
Alternatively, export tokens directly:
```bash
export MODAL_TOKEN_ID="your-token-id"
export MODAL_TOKEN_SECRET="your-token-secret"
```

---

### 4. Configure Hermes
Run the repo setup script to create `~/.hermes`, set the local backend, generate a persistent session token, and export the required environment variables:
```bash
python3 setup.py
source ~/.bashrc
```

Link your LLM provider:
```bash
hermes setup
```

---

### 5. Start the Hermes Gateway
```bash
hermes dashboard --host 0.0.0.0 --port 9119 --insecure --tui --no-open
```

---

### 6. Expose Port 9119
1. Open the **Ports** tab in Codespaces.
2. Right-click **9119** → **Port Visibility** → **Public**.
3. Copy the **Forwarded Address** URL, e.g. `https://<codespace-id>-9119.app.github.dev`.

---

### 7. Connect the Hermes Desktop App
1. Open **Hermes Desktop App** → **Settings** → **Gateway** → **Remote Connection**.
2. **Remote URL:** paste your Codespaces forwarded URL.
3. **Token:** the same value stored as `HERMES_DASHBOARD_SESSION_TOKEN` in `~/.hermes/.env`.
4. Click **Save & Reconnect**.

---

## 🔐 Security & Best Practices
* Keep `~/.hermes/.env` private and out of git.
* Only set port **9119** to **Public** while actively using Remote Gateway.
