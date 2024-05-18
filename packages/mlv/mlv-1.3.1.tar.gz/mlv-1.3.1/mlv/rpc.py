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
