import json
import os
from sys import platform
from os import path
import gc
import time
import datetime
from base64 import b64decode
from io import BytesIO
from os import path
import socket
from contextlib import closing

import requests
from huggingface_hub import hf_hub_url
from flask import send_file

base_path = os.getenv("BASE_PATH")
cache_path = path.join(base_path, "models")
output_path = path.join(base_path, "output")
aiapps_path = os.getenv("AIAPPS_PATH") or path.join(base_path, ".iai/aiapps")
proxies = {"https": os.getenv("https_proxy")}
os.environ["TRANSFORMERS_CACHE"] = cache_path
os.environ["HF_HUB_CACHE"] = cache_path
os.environ["HF_HOME"] = cache_path
print("Base Path is: ", base_path)
print("Cache Path is: ", cache_path)
print("Output Path is: ", output_path)
is_mac = platform == "darwin"


def get_nowstr():
    return datetime.now().strftime("%Y%m%d%H%M%S")


class timer:
    def __init__(self, method_name="timed process"):
        self.method = method_name

    def __enter__(self):
        self.start = time.time()
        print(f"{self.method} starts")

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        print(f"{self.method} took {str(round(end - self.start, 2))}s")


def dataurl_to_image(data_url):
    from PIL import Image

    _, encoded = data_url.split("base64,")
    data = b64decode(encoded)
    o = BytesIO(data)
    m = Image.open(o)
    return m


def serve_pil_image(pil_img):
    from PIL import Image

    img_io = BytesIO()
    pil_img.save(img_io, "png", quality=70)
    img_io.seek(0)
    pil_img.save(path.join(output_path, get_nowstr() + ".png"))
    return send_file(img_io, mimetype="image/png")


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("localhost", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def clear_memory():
    import torch

    gc.collect()
    # if not is_mac and torch.cuda.is_available():
    #     torch.cuda.empty_cache()
    if is_mac:
        torch.mps.empty_cache()


def parse_port(raw):
    # Example: ###PORT:12345
    return raw.split(":")[1]


def check_model_files_exist(app_name, app_info):
    if not app_info.get("models"):
        return True
    # TODO
    return True


def load_aiapps_json():
    aiapps = []
    for filename in os.listdir(aiapps_path):
        if os.path.isdir(
            os.path.join(aiapps_path, filename)
        ) and not filename.startswith("__"):
            aiapps.append(
                {
                    "name": filename,
                    "info": json.load(
                        open(
                            os.path.join(aiapps_path, filename, "app.json"),
                            "r",
                            encoding="utf-8",
                        )
                    ),
                }
            )
    return aiapps


class DownloadManager:
    def __init__(self, base_model_path) -> None:
        self.base_model_path = base_model_path

    def from_huggingface(self, repo_id, filename, subfolder=None):
        # Don't use hf_hub_download here, beacause no progess handler
        # hf_hub_download(repo_id=repo_id, filename=filename, local_dir=cache_path)
        url = hf_hub_url(repo_id=repo_id, filename=filename, subfolder=subfolder)
        yield from self.from_url(url, filename)

    def from_url(self, url, save_filename):
        try:
            print("Start download from url: ", url)
            response = requests.get(url, stream=True, timeout=300, proxies=proxies)
            total_size_in_bytes = int(response.headers.get("content-length", 0))
            block_size = 1024 * 1024  # 1 Kibibyte * 1024 = 1MB
            downloaded_size = 0
            if total_size_in_bytes == 0:
                yield b"end"
            else:
                with open(
                    os.path.join(self.base_model_path, save_filename), "wb"
                ) as fp:
                    for data in response.iter_content(block_size):
                        fp.write(data)
                        downloaded_size += len(data)
                        yield str(downloaded_size / total_size_in_bytes).encode("utf-8")
                yield b"end"
        except Exception as e:
            print(e)
            yield b"error"


rpc_code = """
\n
import atexit
import xmlrpc.server


def test_connection():
    print("hello world")


def make_frameworks_proxy(frameworks_port):
    if not frameworks_port:
        return
    frameworks = {}
    for name, port in frameworks_port.items():
        frameworks[name] = xmlrpc.client.ServerProxy(
            "http://localhost:" + port, allow_none=True
        )
    return frameworks


def start_server(modelCls, port, frameworks_port=None):
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", port), allow_none=True)
    framework = make_frameworks_proxy(frameworks_port)
    if framework:
        model = modelCls(framework)
    else:
        model = modelCls()
    server.register_instance(model)
    server.register_function(test_connection)
    print(f"###PORT:{port}")
    if hasattr(model, "clear") and callable(getattr(model, "clear")):
        atexit.register(lambda: model.clear())
    server.serve_forever()
\n
"""
