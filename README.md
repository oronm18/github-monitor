# GitHub Monitor

A minimal Python webhook server that detects suspicious GitHub org events and logs alerts.

## Setup & Run

1. **Clone & install dependencies**
   ```bash
   git clone https://github.com/oronm18/github-monitor.git
   cd github-monitor
   pip install -r requirements.txt
   ```

2. **Install & configure ngrok**
   ```bash
   # macOS (Homebrew) or download from ngrok.com
   brew install ngrok/ngrok/ngrok    

   # Add your auth token
   ngrok config add-authtoken YOUR_NGROK_AUTH_TOKEN

   # Start tunneling to port 5001
   ngrok http 5001
   ```

3. **Set your webhook secret**
   ```bash
   export WEBHOOK_SECRET="your_webhook_secret_here"
   ```

4. **Configure GitHub webhook**
   - **Payload URL:** `https://<your-ngrok-domain>/webhook`
   - **Content type:** `application/json`
   - **Secret:** same as `WEBHOOK_SECRET`
   - **Events:** push, team, repository

5. **Run the server**
   ```bash
   python main.py
   ```

Any suspicious event will be logged to your console.
