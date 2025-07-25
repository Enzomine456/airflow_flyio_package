from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import openai
import requests
import os
import time

openai.api_key = "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"  # sua chave aqui
SAVE_FOLDER = "videos"
os.makedirs(SAVE_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = "uma-chave-secreta-muito-forte"  # para mensagens flash

def gerar_video(prompt):
    try:
        response = openai.video.create(
            prompt=prompt,
            duration=10,
            quality="1080p",
            response_format="url"
        )
        url = response["data"]["url"]
        nome_arquivo = f"{SAVE_FOLDER}/{int(time.time())}.mp4"
        r = requests.get(url)
        r.raise_for_status()
        with open(nome_arquivo, "wb") as f:
            f.write(r.content)
        return nome_arquivo
    except Exception as e:
        print("[ERRO]:", e)
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
        if not prompt:
            flash("Por favor, escreva uma descrição para gerar o vídeo.", "error")
            return redirect(url_for("index"))

        caminho = gerar_video(prompt)
        if caminho:
            nome = os.path.basename(caminho)
            video_url = url_for("video", nome=nome)
            return template("index.html", prompt=prompt, video_url=video_url)
        else:
            flash("Erro ao gerar vídeo. Tente novamente mais tarde.", "error")
            return redirect(url_for("index"))

    return template("index.html", prompt="", video_url=None)

@app.route("/video/<nome>")
def video(nome):
    caminho = os.path.join(SAVE_FOLDER, nome)
    if os.path.exists(caminho):
        return send_file(caminho, mimetype="video/mp4")
    else:
        return "Vídeo não encontrado", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
