import threading


class AtomicInteger:

    def __init__(self, value):
        self.value = value
        self._lock = threading.Lock()

    def get(self):
        return self.value

    def add_and_get(self, increment=1):
        with self._lock:
            self.value += increment
        return self.value

    def set_to(self, value):
        with self._lock:
            self.value += value