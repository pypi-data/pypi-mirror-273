from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import importlib
import atexit
import time
import os


class ReloadCfgHandler(FileSystemEventHandler):
    def __init__(self, module):
        self.module = module
        self.last_modified_time = 0
        observer = Observer()
        observer.schedule(self, path=os.path.dirname(module.__file__), recursive=False)
        observer.start()
        atexit.register(observer.stop)

    def on_modified(self, event):
        if event.src_path == self.module.__file__:
            current_time = time.time()
            if current_time - self.last_modified_time < 3:
                return
            self.last_modified_time = current_time
            try:
                importlib.reload(self.module)
                print(f"Module {self.module.__name__} reloaded")
            except Exception as e:
                print(f"Error reloading module: {e}")
