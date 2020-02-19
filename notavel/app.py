import connexion

app = connexion.App(__name__, specification_dir="../openapi")
app.add_api("notavel-api.yml")

@app.route("/")
def home():
    return "Hello world!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)