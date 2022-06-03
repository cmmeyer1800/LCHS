import sys

if "--prod" in sys.argv:
    prod = True
    debug = False
else:
    prod = False
    debug = True

from lchs import create_app

app = create_app(prod)
app.run("0.0.0.0", port=4000, debug=debug)
