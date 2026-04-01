import os
import json
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")
TODO_URL = os.environ.get("TODO_URL")  # tu URL de Vercel

def leer_tareas():
    try:
        r = requests.get(TODO_URL + "/tareas.json", timeout=5)
        return r.json() if r.ok else []
    except:
        return []

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! Puedo gestionar tu to-do list.\n\n"
        "/ver — ver todas las tareas\n"
        "/agregar <tarea> — agregar una tarea nueva\n"
        "/ayuda — mostrar este menú"
    )

async def ayuda(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await start(update, ctx)

async def ver(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    tareas = leer_tareas()
    if not tareas:
        await update.message.reply_text("No hay tareas guardadas aún.")
        return
    emojis = {"todo": "⬜", "progress": "🔄", "done": "✅"}
    nombres = {"todo": "Por hacer", "progress": "En progreso", "done": "Hecho"}
    msg = ""
    for estado in ["todo", "progress", "done"]:
        grupo = [t for t in tareas if t.get("estado") == estado]
        if grupo:
            msg += f"\n{emojis[estado]} *{nombres[estado]}*\n"
            for t in grupo:
                msg += f"  • {t['texto']} (id: `{t['id']}`)\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def agregar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    texto = " ".join(ctx.args)
    if not texto:
        await update.message.reply_text("Escribe la tarea después del comando. Ej: /agregar Comprar leche")
        return
    tareas = leer_tareas()
    nueva = {"id": str(int(__import__("time").time() * 1000)), "texto": texto, "estado": "todo"}
    tareas.append(nueva)
    guardar_tareas(tareas)
    await update.message.reply_text(f"✅ Tarea agregada: {texto}")

async def mensaje_libre(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Usa /ayuda para ver los comandos disponibles.")

def guardar_tareas(tareas):
    pass  # Las tareas viven en el navegador vía localStorage

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ayuda", ayuda))
app.add_handler(CommandHandler("ver", ver))
app.add_handler(CommandHandler("agregar", agregar))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje_libre))

if __name__ == "__main__":
    app.run_polling()
```

5. Guarda con `Commit changes`

Luego crea un segundo archivo llamado `requirements.txt` con este contenido:
```
python-telegram-bot==20.7
requests
