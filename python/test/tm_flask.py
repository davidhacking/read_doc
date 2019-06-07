# encoding=utf-8
from flask import Flask
import tracemalloc
import json

tracemalloc.start()
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/alloc")
def alloc():
    s = 's' * (1024 * 1024)
    return s
    pass

@app.route('/stat')
def stat():
    snapshot = tracemalloc.take_snapshot()
    stats = snapshot.statistics('lineno')
    ret = [str(s) for s in stats[:5]]
    return json.dumps(ret, indent=4)

if __name__ == "__main__":
    print ("tm_flask")
    app.run()
    pass
