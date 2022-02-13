import os

os.environ["CONTENT_FOLDER"] = "/home/collin/Code/LCHS/lchs/content"

from lchs import create_app

app = create_app()
app.run("0.0.0.0", port=5000, debug=True)
