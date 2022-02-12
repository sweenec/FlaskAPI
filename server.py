from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import linked_list
import hash_table
import random
import binary_search_tree
import custom_queue
import stack

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0


# config sqlite to enforce foreign key constraints
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


db = SQLAlchemy(app)
now = datetime.now()


# models
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost", cascade="all, delete")  # deletes reference rows to deleted data


class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


# creates new user 
@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(
        name=data["name"],
        email=data["email"],
        address=data["address"],
        phone=data["phone"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 200


# gets users in descending order  
@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    users = User.query.all()  # query returns users in ASCENDING order
    all_users_llist = linked_list.LinkedList()

    for user in users:
        # inserted at beginning each time so end result is in DESCENDING order
        all_users_llist.insert_head(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone
            }
        )

    return jsonify(all_users_llist.to_list())


# gets users in ascending order    
@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    users = User.query.all()  # query returns users in ASCENDING order
    all_users_llist = linked_list.LinkedList()

    for user in users:
        # inserted at end each time so end result is in ASCENDING order
        all_users_llist.insert_tail(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone
            }
        )

    return jsonify(all_users_llist.to_list())


# gets one user by ID
@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    users = User.query.all()
    all_users_llist = linked_list.LinkedList()

    for user in users:
        all_users_llist.insert_head(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone
            }
        )

    user = all_users_llist.get_user_by_id(user_id)

    return jsonify(user), 200


# deletes a user
@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200


# creates a blog post
@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    data = request.get_json()   # Set data type of body in postman to JSON - Otherwise this will be set to None

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User does not exist!"}), 400

    ht = hash_table.HashTable(10)

    ht.add_key_value_pair("title", data["title"])
    ht.add_key_value_pair("body", data["body"])
    ht.add_key_value_pair("date", now)
    ht.add_key_value_pair("user_id", user_id)

    new_blog_post = BlogPost(
        title=ht.get_value("title"),
        body=ht.get_value("body"),
        date=ht.get_value("date"),
        user_id=ht.get_value("user_id")
    )
    db.session.add(new_blog_post)
    db.session.commit()
    return jsonify({"message": "New Blog Post Created"}), 200


# returns blog post with specified id
@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    blog_posts = BlogPost.query.all()   # returns in ascending order by ID
    random.shuffle(blog_posts)   # shuffle data so it's inserted into tree randomly (better chance of a balanced tree)

    bst = binary_search_tree.BinarySearchTree()

    for post in blog_posts:
        bst.insert({
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "user_id": post.user_id
        })

    post = bst.search(blog_post_id)

    if not post:
        return jsonify({"message": "Post not found"}), 404

    return jsonify(post), 200


# converts blog post body to numeric value containing total of each char's ASCII decimal equivalent
@app.route("/blog_post/numeric_body", methods=["GET"])
def get_numeric_post_bodies():
    blog_posts = BlogPost.query.all()

    q = custom_queue.Queue()
    for post in blog_posts:
        q.enqueue(post)     # oldest posts at front of queue

    post_list = []

    for _ in range(len(blog_posts)):
        post = q.dequeue()
        numeric_body = 0
        for char in post.data.body:
            numeric_body += ord(char)

        post.data.body = numeric_body

        post_list.append(
            {
                "id": post.data.id,
                "title": post.data.title,
                "body": post.data.body,
                "user_id": post.data.user_id
            }
        )

    return jsonify(post_list), 200


# deletes last 5 blog posts
@app.route("/blog_post/delete_last_5", methods=["DELETE"])
def delete_last_5():
    blog_posts = BlogPost.query.all()

    s = stack.Stack()

    for post in blog_posts:
        s.push(post)    # most recent posts at top of stack

    for _ in range(5):
        post_to_delete = s.pop()
        db.session.delete(post_to_delete.data)
        db.session.commit()

    return jsonify({"message": "Last 5 posts deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
