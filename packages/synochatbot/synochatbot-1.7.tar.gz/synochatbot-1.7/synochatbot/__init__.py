#from .instance import instance
from .bot import app, send_message, run_bot
import threading
import time
time.sleep(1)

class SynoBot:
    def __init__(self, prefix):
        self.prefix = prefix
        self.alias_to_func = {}

    def message(self, alias, arguments=0):
        def decorator(func):
            self.alias_to_func[alias] = func
            return func
        return decorator

    def run(self, **kwargs):
        flask_thread = threading.Thread(target=app.run, kwargs=kwargs)
        flask_thread.start()
def instance(prefix):
    return SynoBot(prefix)