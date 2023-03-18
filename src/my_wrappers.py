from io import StringIO
from contextlib import redirect_stdout

def capture_output(func):
    def wrapper(*args, **kwargs):
        output = StringIO()
        with redirect_stdout(output):
            result = func(*args, **kwargs)
        return result, output
    
    return wrapper