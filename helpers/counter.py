import threading

# Threadsafe Counter
class AtomicCounter:
    def __init__(self, initial=0):
        self.value = initial
        self._lock = threading.Lock()

    def inc(self, num=1):
        with self._lock:
            self.value += num
            return self.value
