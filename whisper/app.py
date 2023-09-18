from flask import Flask, abort, request
from tempfile import NamedTemporaryFile
import os
import whisper
import openai
import torch


# Whisperモデルをロードする
model = whisper.load_model("base")

# OpenAPI APIキーを設定する
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


@app.route("/")
def welcome():
    return "Welcome to my Blog Post about ChatGPT and Whisper!"


@app.route('/summary', methods=['POST'])
def handler():
    print(request.file)
    if not request.files:
        # ユーザーがファイルを渡さなかった場合は、400 (Bad Request) エラーを返す
        abort(400)

    # ユーザーが渡したすべてのファイルに対してループする
    for filename, handle in request.files.items():
        # 一時ファイルを作成する.
        temp = NamedTemporaryFile()
        # ユーザーがアップロードしたファイルを一時ファイルに書きこむ
        handle.save(temp)
        # Whisperモデルで音声の一時ファイルからテキストを取得する
        result = model.transcribe(temp.name)
        print(result)

    # JSON形式で結果を返却する
    return {'result': result}


def summary_text(transcribed_text):
    if len(transcribed_text) == 0:
        return ""

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            max_tokens=1024,
            stop=None,
            temperature=0.7,
        )
        print(response)

        return response.choices[0].text
    except Exception as e:
        print(e)
        return ""
