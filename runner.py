from lchs import create_app

app = create_app()
app.run("0.0.0.0", port=4000)
