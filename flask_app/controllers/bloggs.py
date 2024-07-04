from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.blogg import Blogg
from flask_app.models.user import User
from flask import Flask, render_template, redirect, request, session, flash,jsonify
import logging
import os
from datetime import datetime
from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from werkzeug.utils import secure_filename


#check if the formau is right
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/bloggs/new")
def addBlogg():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("addBlogg.html", loggeduser=loggeduser)


@app.route("/marketing")
def Marketing():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("marketing.html", loggeduser=loggeduser)

@app.route("/about")
def aboutAs():
    return render_template("about.html")

@app.route("/news")
def news():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("news.html", loggeduser=loggeduser)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/politics")
def politics():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("politics.html", loggeduser=loggeduser)

@app.route("/art")
def art():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("art.html", loggeduser=loggeduser)

@app.route("/health")
def health():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("health.html", loggeduser=loggeduser)

@app.route("/sport")
def sport():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("sport.html", loggeduser=loggeduser)

@app.route("/recipe")
def recipe():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("recipe.html", loggeduser=loggeduser)

@app.route("/travel")
def travel():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    return render_template("travel.html", loggeduser=loggeduser)


@app.route("/add/blogg", methods=["POST"])
def createBlogg():
    if "user_id" not in session:
        return redirect("/")
    if not Blogg.validate_blogg(request.form):
        return redirect(request.referrer)
    if not request.files['image']:
        flash('Show image is required!', 'image')
        return redirect(request.referrer)
    image = request.files['image']
    if not allowed_file(image.filename):
        flash('Image should be in png, jpg, jpeg format!', 'image')
        return redirect(request.referrer)
    if image and  allowed_file(image.filename):
        filename1 = secure_filename(image.filename)
        time = datetime.now().strftime("%d%m%Y%S%f")
        time+= filename1
        filename1 = time
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
    data = {
        "description": request.form["description"],
        "image": filename1,
        'user_id': session['user_id']
    }
    Blogg.create(data)
    return redirect("/bloggs")


@app.route("/blogg/<int:id>")
def viewBlogg(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"blogg_id": id, "id": session["user_id"]}
    blogg = Blogg.get_blogg_by_id(data)
    loggeduser = User.get_user_by_id(data)
    usersWhoLiked = Blogg.get_users_who_liked(data)
    return render_template("blogg.html", blogg=blogg, loggeduser=loggeduser, usersWhoLiked=usersWhoLiked, numOfLikes=len(Blogg.get_users_who_liked(data)))


@app.route("/delete/blogg/<int:id>")
def deleteBlogg(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"blogg_id": id, "id": session["user_id"]}
    blogg = Blogg.get_blogg_by_id(data)
    loggeduser = User.get_user_by_id(data)
    if blogg["user_id"] == loggeduser["id"]:
        Blogg.delete_all_likes(data)
        Blogg.delete_blogg(data)
        Blogg.delete_all_comments(data)
    return redirect("/bloggs")


@app.route("/blogg/edit/<int:id>")
def editBlogg(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"blogg_id": id, "id": session["user_id"]}
    blogg = Blogg.get_blogg_by_id(data)
    if not blogg:
        return redirect('/')
    loggeduser = User.get_user_by_id(data)
    if blogg['user_id'] != loggeduser['id']:
        return redirect('/')
    return render_template("editBlogg.html", blogg=blogg, loggeduser=loggeduser)


@app.route("/update/blogg/<int:id>", methods=["POST"])
def updateBlogg(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"blogg_id": id, "id": session["user_id"]}
    blogg = Blogg.get_blogg_by_id(data)
    if not blogg:
        return redirect('/')
    loggeduser = User.get_user_by_id(data)
    if blogg['user_id'] != loggeduser['id']:
        return redirect('/')
    if (
        len(request.form["description"]) < 1
    ):
        flash("All fields required", "allRequired")
        return redirect(request.referrer)
    updateData={
        'description': request.form['description'],
        'blogg_id':id
    }
    Blogg.update_blogg(updateData)
    return redirect('/blogg/'+ str(id))


@app.route('/like/<int:id>')
def addLike(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'blogg_id': id,
        'id': session['user_id']
    }
    usersWhoLiked = Blogg.get_users_who_liked(data)
    if session['user_id'] not in usersWhoLiked:
        Blogg.addLike(data)
        return redirect(request.referrer)
    return redirect(request.referrer)


@app.route('/unlike/<int:id>')
def removeLike(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'blogg_id': id,
        'id': session['user_id']
    }    
    Blogg.removeLike(data)
    return redirect(request.referrer)




@app.route('/like/<int:blogg_id>', methods=['POST'])
def like(blogg_id):
    if 'user_id' not in session:
        return jsonify(status='error', message='User not logged in'), 403

    user_id = session['user_id']
    query = "INSERT INTO likes (user_id, blogg_id) VALUES (%(user_id)s, %(blogg_id)s)"
    data = {'user_id': user_id, 'blogg_id': blogg_id}
    connectToMySQL('blogg').query_db(query, data)

    return jsonify(status='success')

@app.route('/unlike/<int:blogg_id>', methods=['POST'])
def unlike(blogg_id):
    if 'user_id' not in session:
        return jsonify(status='error', message='User not logged in'), 403

    user_id = session['user_id']
    query = "DELETE FROM likes WHERE user_id = %(user_id)s AND blogg_id = %(blogg_id)s"
    data = {'user_id': user_id, 'blogg_id': blogg_id}
    connectToMySQL('blogg').query_db(query, data)

    return jsonify(status='success')


@app.route('/comment/<int:blogg_id>', methods=['POST'])
def comment(blogg_id):
    if 'user_id' not in session:
        return jsonify(status='error', message='User not logged in'), 403

    user_id = session['user_id']
    comment_text = request.form.get('comment_text')

    query = "INSERT INTO comments (user_id, blogg_id, comment_text) VALUES (%(user_id)s, %(blogg_id)s, %(comment_text)s)"
    data = {'user_id': user_id, 'blogg_id': blogg_id, 'comment_text': comment_text}
    connectToMySQL('blogg').query_db(query, data)

    return jsonify(status='success')

@app.route('/comments/<int:blogg_id>', methods=['GET'])
def get_comments(blogg_id):
    # Fetch comments with user_id and other necessary details
    query = """
        SELECT comments.id, comments.user_id, comments.comment_text, users.username
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE comments.blogg_id = %s
    """
    comments = connectToMySQL('blogg').query_db(query, (blogg_id,))
    
    # Fetch current user's ID from session
    current_user_id = session.get('user_id')

    return jsonify(comments=comments, current_user_id=current_user_id)


@app.route('/comment/delete/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    if 'user_id' not in session:
        return jsonify(status='error', message='User not logged in'), 403

    user_id = session['user_id']

    try:
        query = "DELETE FROM comments WHERE id = %s AND user_id = %s"
        result = connectToMySQL('blogg').query_db(query, (comment_id, user_id))

        if result:
            return jsonify(status='success'), 200
        else:
            return jsonify(status='error', message='Failed to delete comment'), 400

    except Exception as e:
        print(f"Exception occurred while deleting comment {comment_id}: {e}")
        return jsonify(status='error', message='An error occurred while deleting comment'), 500

