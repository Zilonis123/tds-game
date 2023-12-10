import time

def timer(f):
    def wrapper(*args, **kwargs):
        start = time.time()
        a = f(*args, **kwargs)
        end = time.time()
        print(f"Took {round(end-start, 5)}s")
        return a
    return wrapper