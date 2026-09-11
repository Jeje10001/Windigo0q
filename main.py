import os
import sys
import time
import threading
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer

# ---------- 1. HEALTH SERVER (keeps Railway happy) ----------
def run_health_server():
    port = int(os.environ.get("PORT", 8080))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")

        def log_message(self, *args):
            pass

    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


# ---------- 2. BOT ----------
def run_bot():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")

    if not token:
        print("FATAL: TELEGRAM_BOT_TOKEN variable is missing.", flush=True)
        # Keep the container alive so Railway shows the message in logs
        while True:
            time.sleep(60)

    try:
        from telegram.ext import Application, CommandHandler

        async def start(update, context):
            await update.message.reply_text("Hello! I'm Wingo. Type /help.")

        async def help_cmd(update, context):
            await update.message.reply_text(
                "/start - Welcome\n/help - Help\n/about - Info"
            )

        async def about(update, context):
            await update.message.reply_text("Simple assistant bot.")

        print("Starting bot...", flush=True)
        app = Application.builder().token(token).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_cmd))
        app.add_handler(CommandHandler("about", about))
        print("Bot is polling now.", flush=True)
        app.run_polling(drop_pending_updates=True)

    except Exception:
        print("BOT CRASHED WITH ERROR:", flush=True)
        traceback.print_exc()
        sys.stdout.flush()
        # Keep container alive so Railway shows the error
        while True:
            time.sleep(60)


# ---------- 3. ENTRY ----------
if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    run_bot()
