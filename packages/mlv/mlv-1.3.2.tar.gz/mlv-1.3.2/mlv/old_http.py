from sys import platform
import time

from base64 import b64decode
import socket
from contextlib import closing
import os
from flask import Flask, request, send_file
from PIL import Image
from os import path
import threading
import gc
import traceback
from mlv.util import get_nowstr
from .setting import cache_path, is_mac, output_path
import torch
from .old_stable_diffusion import load_models_backend


lock = threading.Lock()

if not path.exists(cache_path):
    os.makedirs(cache_path, exist_ok=True)

infer = {"pipe": None}

app = Flask(__name__)


def clear_memory():
    global infer
    if infer.get("pipe"):
        del infer["pipe"]
    gc.collect()
    if not is_mac and torch.cuda.is_available():
        torch.cuda.empty_cache()
    if is_mac:
        torch.mps.empty_cache()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/load_models", methods=["POST"])
def load_models():
    """
    load and update is the same thing
    """

    try:
        data = request.get_json()
        if data["model"]:
            global infer
            with lock:
                clear_memory()
                infer["pipe"] = load_models_backend(
                    data["model"],
                    data["technique"],
                    data["safety_checker"],
                    data["lora_weights"],
                )
                infer["pipe"].technique = data["technique"]
        return {"success": True}
    except Exception as err:
        tb_str = "".join(traceback.format_exception(None, err, err.__traceback__))
        return {
            "success": False,
            "error": str(err),
            "traceback": tb_str,
        }


@app.route("/unload_models", methods=["POST"])
def unload_models():
    try:
        with lock:
            clear_memory()
            return {"success": True}
    except:
        return {"success": False}


@app.route("/areyoufree", methods=["GET"])
def areyoufree():
    return "no" if lock.locked() else "yes"


@app.route("/is_model_loaded", methods=["POST"])
def is_model_loaded():
    data = request.get_json()
    if infer.get("pipe") and data and data.get("technique"):
        return "yes" if data["technique"] == infer["pipe"].technique else "no"
    return "no" if not infer.get("pipe") else "yes"


@app.route("/img2img", methods=["POST"])
def img2img():
    data = request.get_json()
    global infer

    try:
        if data["image"].startswith("data:image"):
            image = dataurl_to_image(data["image"])
            data["image"] = image
        if infer.get("pipe"):
            with lock:
                img = infer["pipe"](**data)
                print(img)
                return serve_pil_image(img)
        else:
            return {"success": False, "error": "Please load models first"}
    except Exception as err:
        tb_str = "".join(traceback.format_exception(None, err, err.__traceback__))
        return {
            "success": False,
            "error": str(err),
            "traceback": tb_str,
        }


@app.route("/txt2img", methods=["POST"])
def txt2img():
    data = request.get_json()
    global infer

    try:
        if infer.get("pipe"):
            with lock:
                data["mode"] = "t2i"
                img = infer["pipe"](**data)
                print(img)
                return serve_pil_image(img)
        else:
            return {"success": False, "error": "Please load models first"}
    except Exception as err:
        tb_str = "".join(traceback.format_exception(None, err, err.__traceback__))
        return {
            "success": False,
            "error": str(err),
            "traceback": tb_str,
        }


from io import BytesIO


def dataurl_to_image(data_url):
    _, encoded = data_url.split("base64,")
    data = b64decode(encoded)
    o = BytesIO(data)
    m = Image.open(o)
    return m


def serve_pil_image(pil_img: Image.Image):
    img_io = BytesIO()
    pil_img.save(img_io, "png", quality=70)
    img_io.seek(0)
    pil_img.save(os.path.join(output_path, get_nowstr() + ".png"))
    return send_file(img_io, mimetype="image/png")


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("localhost", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def run_app():
    port = os.getenv("PORT") or find_free_port()
    print(f"###PORT:{port}")
    app.run(host="localhost", port=port)
