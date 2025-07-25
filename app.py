from flask import Flask, render_template_string, request, send_file
import openai
import requests
import os
import time

openai.api_key = "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"
SAVE_FOLDER = "videos"
os.makedirs(SAVE_FOLDER, exist_ok=True)

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang='pt-br'>
<head>
    <meta charset='UTF-8'>
    <title>Air Flow AI</title>
    <style>
        body { background: #faf7ff; font-family: 'Segoe UI'; text-align: center; padding: 40px; color: #333; }
        textarea, input[type=submit] {
            width: 90%; font-size: 1.1em; padding: 12px; margin-top: 20px;
            background: #f0e8ff; border: 2px solid #d1c4e9; border-radius: 8px;
        }
        video, canvas {
            margin-top: 30px;
            width: 90%; border-radius: 12px; box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }
        .output { margin-top: 30px; background: #f5f0ff; padding: 20px; border-radius: 10px; }
        .purple-btn {
            background: #c084fc; color: white; border: none; padding: 12px 24px;
            border-radius: 8px; font-size: 1em; cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Air Flow AI — Geração de Vídeo</h1>
    <form method="post">
        <textarea name="prompt" placeholder="Descreva o vídeo que deseja gerar...">%s</textarea><br>
        <input type="submit" value="Gerar vídeo" class="purple-btn">
    </form>
    %s
</body>
</html>
"""

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
        with open(nome_arquivo, "wb") as f:
            f.write(r.content)
        return nome_arquivo
    except Exception as e:
        print("[ERRO]:", e)
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    prompt = ""
    resposta_html = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        caminho = gerar_video(prompt)
        if caminho:
            nome = os.path.basename(caminho)
            resposta_html = f'<div class="output"><video controls><source src="/video/{nome}" type="video/mp4"></video></div>'
        else:
            resposta_html = '<p class="output" style="color:red;">Erro ao gerar vídeo</p>'
    return render_template_string(HTML % (prompt, resposta_html))

@app.route("/video/<nome>")
def video(nome):
    return send_file(os.path.join(SAVE_FOLDER, nome), mimetype="video/mp4")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)