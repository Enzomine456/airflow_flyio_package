import os
import time
import requests
from django.shortcuts import render
from django.conf import settings
import openai

openai.api_key = "SUA_OPENAI_KEY"

SAVE_FOLDER = os.path.join(settings.BASE_DIR, 'media/videos')
os.makedirs(SAVE_FOLDER, exist_ok=True)

def gerar_video(prompt):
    try:
        response = openai.video.create(
            prompt=prompt,
            duration=10,
            quality="1080p",
            response_format="url"
        )
        url = response["data"]["url"]
        nome_arquivo = f"{int(time.time())}.mp4"
        caminho_arquivo = os.path.join(SAVE_FOLDER, nome_arquivo)

        r = requests.get(url)
        with open(caminho_arquivo, "wb") as f:
            f.write(r.content)

        return f"/media/videos/{nome_arquivo}"
    except Exception as e:
        print("[ERRO]:", e)
        return None

def index(request):
    prompt = ""
    video_path = None
    error = None

    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        resultado = gerar_video(prompt)
        if resultado:
            video_path = resultado
        else:
            error = "Erro ao gerar vídeo. Tente novamente."

    return render(request, "index.html", {
        "prompt": prompt,
        "video_path": video_path,
        "error": error
    })
