from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import openai
import requests
import os
import time

# Configurações e constantes
openai.api_key = "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"  # Substitua pela sua chave real
PASTA_VIDEOS = "videos"
os.makedirs(PASTA_VIDEOS, exist_ok=True)

app = Flask(__name__)
app.secret_key = "uma-chave-secreta-muito-forte"  # Essencial para usar flash messages

def gerar_video(prompt_texto):
    """
    Gera um vídeo via API OpenAI com base no prompt recebido.
    Salva o vídeo na pasta local e retorna o caminho do arquivo salvo.
    """
    try:
        resposta = openai.video.create(
            prompt=prompt_texto,
            duration=10,
            quality="1080p",
            response_format="url"
        )
        url_video = resposta["data"]["url"]

        nome_arquivo = os.path.join(PASTA_VIDEOS, f"{int(time.time())}.mp4")

        resposta_download = requests.get(url_video)
        resposta_download.raise_for_status()  # Levanta exceção em caso de falha no download

        with open(nome_arquivo, "wb") as arquivo:
            arquivo.write(resposta_download.content)

        return nome_arquivo
    except Exception as erro:
        print("[ERRO AO GERAR VÍDEO]:", erro)
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()

        if not prompt:
            flash("Por favor, insira uma descrição para gerar o vídeo.", "error")
            return redirect(url_for("index"))

        caminho_video = gerar_video(prompt)

        if caminho_video:
            nome_arquivo = os.path.basename(caminho_video)
            url_video = url_for("exibir_video", nome=nome_arquivo)
            return render_template("index.html", prompt=prompt, video_url=url_video)
        else:
            flash("Ocorreu um erro ao gerar o vídeo. Por favor, tente novamente mais tarde.", "error")
            return redirect(url_for("index"))

    return render_template("index.html", prompt="", video_url=None)

@app.route("/video/<nome>")
def exibir_video(nome):
    caminho_video = os.path.join(PASTA_VIDEOS, nome)
    if os.path.isfile(caminho_video):
        return send_file(caminho_video, mimetype="video/mp4")
    else:
        return "Vídeo não encontrado.", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
