from pathlib import Path
import os
from uuid import uuid4

from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024

Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        photos = [request.files.get("photo1"), request.files.get("photo2")]
        if any(photo is None or not photo.filename for photo in photos):
            return render_template("index.html", error="Please choose both photos to save your memory."), 400

        saved_paths = []
        for photo in photos:
            safe_name = secure_filename(photo.filename)
            if not safe_name:
                return render_template("index.html", error="One of those filenames could not be used. Please choose another photo."), 400
            filename = f"{uuid4().hex}_{safe_name}"
            photo.save(Path(app.config["UPLOAD_FOLDER"]) / filename)
            saved_paths.append(url_for("static", filename=f"uploads/{filename}"))

        return render_template("result.html", photos=saved_paths)

    return render_template("index.html")


@app.route("/maybe")
def maybe():
    return render_template("maybe.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False,
    )
