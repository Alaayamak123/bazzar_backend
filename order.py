from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class order(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String)

    with app.app_context():
        db.create_all()

        @app.route("/users")
        def user_list(self):
            users = db.session.execute(db.select(order).order_by(order.username)).scalars()
            return render_template("user/list.html", users=users)

        @app.route("/users/create", methods=["GET", "POST"])
        def user_create(self):
            if request.method == "POST":
                user = order(
                    username=request.form["username"],
                    email=request.form["email"],
                )
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("user_detail", id=user.id))

            return render_template("user/create.html")

        @app.route("/user/<int:id>")
        def user_detail(id):
            user = db.get_or_404(order, id)
            return render_template("user/detail.html", user=user)

        @app.route("/user/<int:id>/delete", methods=["GET", "POST"])
        def user_delete(id):
            user = db.get_or_404(order, id)

            if request.method == "POST":
                db.session.delete(user)
                db.session.commit()
                return redirect(url_for("user_list"))

            return render_template("user/delete.html", user=user)