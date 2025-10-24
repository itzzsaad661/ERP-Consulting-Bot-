import os
from flask import Flask, request, jsonify, Response
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Configuration
ENDPOINT = "https://models.github.ai/inference"
MODEL = "meta/Llama-4-Scout-17B-16E-Instruct"
SYSTEM_PROMPT = (
    """
You are an AI ERP Consultant Assistant.
Your role is to guide businesses on ERP (Enterprise Resource Planning) systems.
Explain ERP modules, implementation strategies, customization, integration with CRMs,
and provide advice on how ERP improves operational efficiency.
Always respond professionally and clearly.
"""
).strip()

# Flask automatically serves files from the ./static directory at /static/<file>
# Save your bot image as: static/bot.png
app = Flask(__name__)

_client = None
_token_warned = False

def get_client():
    """Lazily initialize and cache the ChatCompletionsClient."""
    global _client, _token_warned
    if _client is not None:
        return _client

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        # Avoid spamming logs repeatedly
        if not _token_warned:
            app.logger.error(
                "GITHUB_TOKEN not found. Set it in your environment before using the chat endpoint."
            )
            _token_warned = True
        return None

    _client = ChatCompletionsClient(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(token),
    )
    return _client

INDEX_HTML = """
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>AI ERP Consultant</title>
  <style>
    :root {
      --bg: #0f172a;
      --panel: #111827;
      --accent: #22c55e;
      --accent-2: #16a34a;
      --text: #e5e7eb;
      --muted: #9ca3af;
      --user: #2563eb;
      --bot: #374151;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0; padding: 0; background: var(--bg); color: var(--text);
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell,
                   Noto Sans, \"Helvetica Neue\", Arial, \"Apple Color Emoji\", \"Segoe UI Emoji\";
      height: 100vh; display: grid; grid-template-rows: auto 1fr auto; overflow: hidden;
    }
    header { display: flex; align-items: center; gap: 12px; padding: 16px 20px; background: var(--panel); border-bottom: 1px solid #1f2937; }
    header h1 { margin: 0; font-size: 18px; font-weight: 600; }
    header p { margin: 6px 0 0 0; color: var(--muted); font-size: 13px; }

    #chat {
      overflow-y: auto; padding: 16px; scroll-behavior: smooth;
    }
    .msg { display: flex; gap: 10px; margin-bottom: 14px; align-items: flex-start; }
    .bubble { max-width: 900px; padding: 12px 14px; border-radius: 10px; line-height: 1.4; white-space: pre-wrap; }
    .user .bubble { background: var(--user); color: #fff; border-top-right-radius: 4px; }
    .bot .bubble { background: var(--bot); color: var(--text); border-top-left-radius: 4px; }

    .avatar { width: 36px; height: 36px; border-radius: 50%; object-fit: cover; flex: 0 0 36px; border: 1px solid #1f2937; background: #0b1220; }
    .header-avatar { width: 32px; height: 32px; border-radius: 50%; object-fit: cover; border: 1px solid #1f2937; }

    footer {
      padding: 12px; background: var(--panel); border-top: 1px solid #1f2937;
    }
    .input-row { display: flex; gap: 10px; align-items: center; }
    .input-row input[type=\"text\"] {
      flex: 1; padding: 12px 12px; border-radius: 8px; border: 1px solid #1f2937; background: #0b1220; color: var(--text);
      outline: none; font-size: 14px;
    }
    .input-row button {
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      color: #07120e; border: none; padding: 11px 14px; border-radius: 8px; font-weight: 700; cursor: pointer;
    }
    .input-row button:disabled { opacity: 0.6; cursor: not-allowed; }

    .status { font-size: 12px; color: var(--muted); margin-top: 6px; }
    .error { color: #fca5a5; }
  </style>
</head>
<body>
  <header>
    <img src=\"/static/bot.png\" alt=\"Bot avatar\" class=\"header-avatar\" />
    <div>
      <h1>AI ERP Consultant</h1>
      <p>Ask about ERP modules, implementation, integrations, customization, and best practices.</p>
    </div>
  </header>

  <main id=\"chat\" aria-live=\"polite\" aria-busy=\"false\"></main>

  <footer>
    <div class=\"input-row\">
      <input id=\"message\" type=\"text\" placeholder=\"Ask anything about ERP...\" autocomplete=\"off\" />
      <button id=\"send\">Send</button>
    </div>
    <div id=\"status\" class=\"status\"></div>
  </footer>

  <script>
    const chat = document.getElementById('chat');
    const input = document.getElementById('message');
    const sendBtn = document.getElementById('send');
    const status = document.getElementById('status');

    function appendMessage(role, text) {
      const msg = document.createElement('div');
      msg.className = `msg ${role}`;

      if (role === 'bot') {
        const avatar = document.createElement('img');
        avatar.className = 'avatar';
        avatar.src = '/static/bot.png';
        avatar.alt = 'Bot';
        avatar.onerror = () => { avatar.style.display = 'none'; };
        msg.appendChild(avatar);
      }

      const bubble = document.createElement('div');
      bubble.className = 'bubble';
      bubble.textContent = text;
      msg.appendChild(bubble);

      chat.appendChild(msg);
      chat.scrollTop = chat.scrollHeight;
    }

    function setBusy(isBusy, message = '') {
      document.querySelector('main').setAttribute('aria-busy', isBusy ? 'true' : 'false');
      status.textContent = message;
    }

    async function sendMessage() {
      const text = input.value.trim();
      if (!text) return;

      appendMessage('user', text);
      input.value = '';
      input.focus();

      sendBtn.disabled = true;
      setBusy(true, 'Thinking...');

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text })
        });

        const data = await res.json();
        if (!res.ok) {
          const msg = data && data.error ? data.error : 'Unexpected error.';
          appendMessage('bot', `Error: ${msg}`);
        } else {
          appendMessage('bot', data.reply);
        }
      } catch (err) {
        appendMessage('bot', 'Network error. Check server logs.');
      } finally {
        sendBtn.disabled = false;
        setBusy(false, '');
      }
    }

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });

    // Intro message
    appendMessage('bot', 'Hello! I am your AI ERP Consultant. How can I help you today?');
  </script>
</body>
</html>
"""


@app.get("/")
def index():
    return Response(INDEX_HTML, mimetype="text/html")


@app.post("/api/chat")
def api_chat():
    try:
        data = request.get_json(silent=True) or {}
        user_input = (data.get("message") or "").strip()
        if not user_input:
            return jsonify({"error": "Message is required."}), 400

        client = get_client()
        if client is None:
            return (
                jsonify(
                    {
                        "error": (
                            "Server is not configured. Set the GITHUB_TOKEN environment variable and restart."
                        )
                    }
                ),
                500,
            )

        response = client.complete(
            messages=[SystemMessage(SYSTEM_PROMPT), UserMessage(user_input)],
            temperature=0.7,
            top_p=0.9,
            max_tokens=1024,
            model=MODEL,
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        app.logger.exception("Error in /api/chat")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # If running locally, enable debug for auto-reload during development
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
