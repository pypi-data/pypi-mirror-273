import time
import os, sys
from watchdog.observers import Observer
import http.server
import socketserver
import webbrowser
import threading
import shutil

from ..util import colorify


def watch_directory(directory, event_handler):
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    print(f"{colorify.green("[   OK   ]")} watching '{directory}' for changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


class MyHTTPServer(threading.Thread):
    def __init__(self, directory, port=8000):
        super().__init__()
        self.directory = directory
        self.port = port
        self.server = None

    def run(self):
        directory = self.directory
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=directory, **kwargs)

        with socketserver.TCPServer(("", self.port), Handler) as self.server:
            print(f"{colorify.yellow("[ SERVER ]")} Serving HTTP on 0.0.0.0 port {self.port} (http://0.0.0.0:{self.port}/) ...")
            webbrowser.open(f"http://localhost:{self.port}")
            try:
                self.server.serve_forever()
            except KeyboardInterrupt:
                print(f"\n{colorify.gray("[ SERVER ]")} Shutting down the server...")
                self.server.server_close()



def clean_directory(directory, exceptions=[]):
    for item in os.listdir(directory):
        if item not in exceptions:
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)


def path_join(*args):
    return os.path.join(*args).replace("\\", "/")


def is_file_under_folder(path, filepath):
    paths = []
    for subdir, dirs, files in os.walk(path):
        for file in files:
            src_path = path_join(subdir, file)
            paths.append(src_path)
    
    if filepath in paths:
        return True
    
    return False
