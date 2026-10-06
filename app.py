from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

profile_data = None


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def welcome():
    return redirect(url_for("myProfile"))


@app.route("/greet/<uname>")
def greet(uname):
    return f"""
    <center>
        <h2>Good morning, {uname}! ☀️</h2>
        <br>
        <a href="/user">Go to Profile</a>
    </center>
    """


@app.route("/user", methods=["GET", "POST"])
def myProfile():
    global profile_data

    message = None
    message_type = None

    if request.method == "POST":
        username = request.form.get("uname", "").strip()
        email = request.form.get("email", "").strip()
        bio = request.form.get("bio", "").strip()
        image = request.files.get("pic")

        if not username:
            message = "Please enter your username."
            message_type = "error"
            return render_template("base.html", data=profile_data,
                                   message=message, message_type=message_type)

        if not email:
            message = "Please enter your email address."
            message_type = "error"
            return render_template("base.html", data=profile_data,
                                   message=message, message_type=message_type)

        # When editing, allow keeping the existing image.
        if image is None or image.filename == "":
            if not profile_data:
                message = "Please select a profile picture."
                message_type = "error"
                return render_template("base.html", data=profile_data,
                                       message=message, message_type=message_type)
            image_path = profile_data["image_path"]
        else:
            if not allowed_file(image.filename):
                message = (
                    "Invalid image format. Use PNG, JPG, JPEG, GIF or WEBP."
                )
                message_type = "error"
                return render_template("base.html", data=profile_data,
                                       message=message, message_type=message_type)

            # Delete old image if replacing it.
            if profile_data and profile_data.get("image_path"):
                old_filename = os.path.basename(profile_data["image_path"])
                old_path = os.path.join(
                    app.config["UPLOAD_FOLDER"], old_filename
                )
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except OSError:
                        pass

            original_name = secure_filename(image.filename)
            extension = original_name.rsplit(".", 1)[1].lower()
            unique_filename = f"{uuid.uuid4()}.{extension}"

            saved_path = os.path.join(
                app.config["UPLOAD_FOLDER"], unique_filename
            )
            image.save(saved_path)

            image_path = url_for(
                "static",
                filename=f"uploads/{unique_filename}"
            )

        profile_data = {
            "uname": username,
            "email": email,
            "bio": bio,
            "image_path": image_path,
        }

        message = "Profile updated successfully!"
        message_type = "success"

    return render_template(
        "base.html",
        data=profile_data,
        message=message,
        message_type=message_type,
    )


@app.route("/delete-profile")
def delete_profile():
    global profile_data

    if profile_data and profile_data.get("image_path"):
        filename = os.path.basename(profile_data["image_path"])
        image_path = os.path.join(
            app.config["UPLOAD_FOLDER"], filename
        )

        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except OSError:
                pass

    profile_data = None
    return redirect(url_for("myProfile"))


@app.errorhandler(413)
def file_too_large(error):
    return render_template(
        "base.html",
        data=profile_data,
        message="Image is too large. Maximum size is 5 MB.",
        message_type="error",
    ), 413


if __name__ == "__main__":
    app.run(debug=True)
