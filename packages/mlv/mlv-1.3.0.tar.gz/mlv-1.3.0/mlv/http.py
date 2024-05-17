from .util import (
    check_model_files_exist,
    load_aiapps_json,
    find_free_port,
    cache_path,
    aiapps_path,
    output_path,
    DownloadManager,
    rpc_code,
)


### SPLIT


import time
import xmlrpc.client
import subprocess
import atexit
import os
from flask import Flask, request, abort
from os import path
import threading
from flask_cors import CORS


lock = threading.Lock()

if not path.exists(cache_path):
    os.makedirs(cache_path, exist_ok=True)

infer = {"pipe": None}
app = Flask(__name__)
CORS(app)
context = {"app": {}}
aiapps = load_aiapps_json()
print("Load aiapps", [app["name"] for app in aiapps])


def get_frameworks_port():
    result = {}
    for name, app_manager in context["app"].items():
        if app_manager.is_framework:
            result[name] = app_manager.app_port
    return result


class AppRunner:
    app_name: None
    process: None
    proxy: None
    app_port: None
    is_framework: None

    def __init__(self, app_name, process, port, is_framework) -> None:
        self.is_framework = is_framework
        self.app_port = port
        self.app_name = app_name
        self.process = process
        self.proxy = xmlrpc.client.ServerProxy(
            "http://localhost:" + port, allow_none=True
        )

        # wait for the app process finish setup
        max_retries = 5
        success = False
        while max_retries:
            time.sleep(1)
            try:
                self.proxy.test_connection()
                print("App is connected, ", app_name)
                success = True
                break
            except Exception:
                print("test connection fail, retry")
            finally:
                max_retries -= 1
        if not success:
            raise Exception("App can not connect, " + app_name)


@app.route("/download_file", methods=["POST"])
def download_file():
    data = request.get_json()
    dl = DownloadManager(os.path.join(cache_path, data.get("app_name")))
    if data.get("from_huggingface"):
        generator = dl.from_huggingface(**data.get("from_huggingface"))
    else:
        generator = dl.from_url(data.get("url"), data.get("filename"))
    return app.response_class(generator, mimetype="text/html")


@app.route("/run_app", methods=["POST"])
def run_app():
    try:
        with lock:
            data = request.get_json()
            action = data["action"]
            app = context["app"].get(data["model"])
            if not app:
                abort(404)
            if action == "load_model":
                result = app.proxy.load_model(data.get("args", {}))
            elif action == "run_model":
                result = app.proxy.run_model(data.get("args", {}))
            return {"success": True, "result": result}
    except Exception as exc:
        return {"success": False, "error": "run task error, " + str(exc)}


@app.route("/start_app", methods=["POST"])
def start_app():
    global context
    global aiapps
    data = request.get_json()
    app = None
    for app_ in aiapps:
        if app_["name"] == data.get("model", ""):
            app = app_
    if not app:
        abort(404)
    app_source_path = os.path.join(aiapps_path, app["name"])
    app_port = find_free_port()

    app_model_path = os.path.join(cache_path, app["name"])
    app_output_path = os.path.join(output_path, app["name"])

    # mkdir anyway
    os.makedirs(app_model_path, exist_ok=True)
    os.makedirs(app_output_path, exist_ok=True)

    if not check_model_files_exist(app["name"], app["info"]):
        return {"success": False, "error": "model files missing"}

    # frameworks app 找出来，暴露给light app来通信
    running_frameworks = get_frameworks_port()
    running_frameworks_json = (
        "{" + ",".join([f'"{k}":"{v}"' for k, v in running_frameworks.items()]) + "}"
        if running_frameworks
        else "None"
    )
    print("Current running frameworks: ", running_frameworks_json)

    if not app["info"].get("is_framework"):
        if not app["info"].get("framework"):
            abort(500, "App config error, no framework found")
        need_framework = app["info"]["framework"]
        if not all(running_frameworks.get(f) for f in need_framework):
            abort(500, "Needed framework not start")

    model_process = subprocess.Popen(
        f"venv/bin/python3 -c '{rpc_code}\nfrom main import Model;start_server(Model, {app_port}, {running_frameworks_json})'",
        cwd=app_source_path,
        shell=True,
        # set env OLLAMA_MODELS=models path
        env={
            "APP_SOURCE_PATH": app_source_path,
            "APP_MODEL_PATH": app_model_path,
            "APP_OUTPUT_PATH": app_output_path,
            **os.environ,
        },
    )

    try:
        context["app"][app["name"]] = AppRunner(
            app["name"],
            model_process,
            str(app_port),
            app["info"].get("is_framework", None),
        )
        return {"success": True}
    except Exception:
        return {"success": False}


@app.route("/test_connection", methods={"POST"})
def tecn():
    data = request.get_json()
    client = xmlrpc.client.ServerProxy(
        "http://localhost:" + data.get("port"), allow_none=True
    )
    result = client.test_connection()
    return {"result": result}


@app.route("/stop_app", methods=["POST"])
def stop_app():
    data = request.get_json()
    with lock:
        global context
        if context["app"].get(data["model"]):
            context["app"][data["model"]].process.kill()
            context["app"].pop(data["model"])
            return {"success": True}
        else:
            abort(404)


@app.route("/is_app_running", methods=["POST"])
def is_app_running():
    data = request.get_json()
    if data and data.get("model"):
        return "yes" if context["app"][data["model"]] else "no"
    abort(404)


@app.route("/hello", methods=["GET"])
def hello():
    return "success"


def run_app():
    port = os.getenv("PORT") or find_free_port()
    print(f"###PORT:{port}")
    app.run(host="localhost", port=port)


def onexit():
    global context
    for name, app in context["app"].items():
        print("kill app process " + name)
        app.process.kill()


atexit.register(onexit)
