# 🚀 Hermes Agent + Modal in GitHub Codespaces

A lightweight, **Docker-free** environment for running [Hermes Agent](https://github.com/NousResearch/hermes-agent) inside GitHub Codespaces. All code execution and command sandboxing are offloaded to [Modal.com](https://modal.com), with remote connectivity for the **Hermes Desktop App**.

---

## 📁 Repository File Structure

```text
/workspaces/gregdavies91/
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # Workspace documentation

~/.hermes/                      # Global Hermes Config (Home Directory)
├── .env                        # Session tokens & API keys (outside repo)
└── config.yaml                 # Agent settings (backend set to modal)
```

---

## ⚡ Quick Start Guide

### 1. Install Dependencies
In your Codespace terminal, run:
```bash
pip install -r requirements.txt
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

### 2. Authenticate Modal
Authenticate your Modal account so Hermes can run execution sandboxes in the cloud:
```bash
modal setup
```
*(Alternatively, set `MODAL_TOKEN_ID` and `MODAL_TOKEN_SECRET` in `~/.hermes/.env`)*

### 3. Configure Hermes for Local Backend
Open `~/.hermes/config.yaml` and set the execution backend to `local`:
```yaml
terminal:
  backend: local
```

Run interactive setup to link your model provider API key:
```bash
hermes setup
```

---

## 🌐 Connecting via Hermes Desktop App (Remote Gateway)

Interface with this Cloud Codespaces deployment from any device running the **Hermes Desktop App**.

### Step 1: Set a Persistent Session Token
Add a session token to `~/.hermes/.env`:
```env
HERMES_DASHBOARD_SESSION_TOKEN=your-secure-random-token
```
*(Tip: Generate one with `openssl rand -base64 32`)*

### Step 2: Start the Hermes Gateway
Run the dashboard process with network binding enabled:
```bash
hermes dashboard --host 0.0.0.0 --port 9119 --insecure --tui --no-open
```

### Step 3: Expose Port 9119 in Codespaces
1. Open the **Ports** tab in Codespaces (bottom panel).
2. Right-click port **9119** → **Port Visibility** → Change to **Public**.
3. Copy the **Forwarded Address** URL (e.g., `https://<codespace-id>-9119.app.github.dev`).

### Step 4: Link Desktop App
1. Open the **Hermes Desktop App** on your device.
2. Go to **Settings** → **Gateway** → **Remote Connection**.
3. Set **Remote URL** to your Codespaces forwarded URL.
4. Set **Token** to your `HERMES_DASHBOARD_SESSION_TOKEN`.
5. Click **Save & Reconnect**.

---

## 🔐 Security & Best Practices
* **Keep `.env` Private:** Ensure `~/.hermes/.env` is listed in `.gitignore` so tokens and API keys are never committed.
* **Port Visibility:** Only expose port `9119` publicly while actively using the Remote Gateway connection.

Here is a step-by-step guide to deploying **Hermes Agent** using **Modal.com** within **GitHub Codespaces**, followed by instructions on connecting to it remotely via the **Hermes Desktop app**.

---

## Part 1: Deploy Hermes Agent with Modal in GitHub Codespaces

### Step 1: Set Up your GitHub Codespace

1. Open your repository (or fork [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)) on GitHub.
2. Click **Code** > **Codespaces** > **Create codespace on main**.
3. Once the environment loads in your browser, open the terminal (`Ctrl + \`` / `Cmd + ``).

---

### Step 2: Install and Authenticate Modal

1. Install the Modal Python package:
```bash
pip install modal

```


2. Authenticate Modal with your account:
```bash
modal setup

```


*Follow the printed link to authorize Codespaces with Modal. Alternatively, you can export your API tokens directly in your environment:*
```bash
export MODAL_TOKEN_ID="your-token-id"
export MODAL_TOKEN_SECRET="your-token-secret"

```



---

### Step 3: Install Hermes Agent

Run the official Hermes Agent install script inside your Codespace:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

```

*(This sets up Python, `uv`, dependencies, and the `hermes` CLI automatically)*

---

### Step 4: Configure Modal as the Execution Backend

By default, Hermes runs code locally. To route command execution and sandbox instances to **Modal**:

1. Open your Hermes configuration file:
```bash
nano ~/.hermes/config.yaml

```


2. Set the terminal backend to `local`:
```yaml
terminal:
  backend: local

```


*(Or add `HERMES_TERMINAL_BACKEND=local` to `~/.hermes/.env`)*
3. Run interactive setup to link your LLM provider (e.g., Nous Portal, OpenRouter, or OpenAI API key):
```bash
hermes config

```



---

## Part 2: Connect the Hermes Desktop App via Remote Gateway

To interface with this cloud-hosted Hermes deployment across multiple devices using the **Remote Gateway** feature in the Hermes Desktop App, follow these steps:

### Step 1: Pin a Session Token on the Remote Server

By default, Hermes generates a temporary session token every time it restarts. To ensure your desktop app stays connected permanently:

1. Open (or create) the `.env` file in `~/.hermes/`:
```bash
nano ~/.hermes/.env

```


2. Add a persistent session token:
```env
HERMES_DASHBOARD_SESSION_TOKEN=your-long-random-secret-token

```


*(Tip: You can generate a random token in terminal using `openssl rand -base64 32`)*

---

### Step 2: Start the Hermes Gateway / Dashboard Server

Run the dashboard process with network binding enabled:

```bash
hermes dashboard --host 0.0.0.0 --port 9119 --insecure --tui --no-open

```

> **What these flags do:**
> * `--host 0.0.0.0`: Binds the backend to all network interfaces so remote clients can reach it.
> * `--port 9119`: The default port for the Hermes Gateway.
> * `--insecure`: Enables session-token auth for remote desktop clients.
> * `--tui`: Enables WebSocket streaming for real-time terminal & desktop chat interaction.
> 
> 

---

### Step 3: Expose the Port in GitHub Codespaces

Because GitHub Codespaces runs in the cloud, you need to make port `9119` accessible to your desktop app:

1. In Codespaces, open the **Ports** tab at the bottom panel.
2. Locate port **`9119`**.
3. Right-click on port `9119` > **Port Visibility** > Change to **Public**.
4. Copy the **Forwarded Address** URL (it will look like `https://<codespace-id>-9119.app.github.dev`).

---

### Step 4: Configure the Hermes Desktop App

You can now connect to this deployment from any device running the Hermes Desktop App:

1. Open the **Hermes Desktop App** on your device.
2. Go to **Settings** > **Gateway** > **Remote connection** (or **Remote Gateway**).
3. Fill in the connection credentials:
* **Remote URL:** Paste your Codespaces forwarded URL (e.g., `https://<codespace-id>-9119.app.github.dev`).
* **Token / Session Token:** Enter the token value set in `HERMES_DASHBOARD_SESSION_TOKEN`.


4. Click **Save & Reconnect**.

Your Hermes Desktop App is now connected to your Modal-backed agent running inside GitHub Codespaces. You can repeat Step 4 on as many secondary devices as you like to share control of the same remote session.
