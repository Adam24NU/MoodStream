import re
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models.user import User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Handle user registration.

    :return: Rendered register.html on GET or unsuccessful POST,
             or redirect to home page on success.
    """
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user_exists = User.query.filter((User.email == email) | (User.username == username)).first()

        # Check if user exists
        if user_exists:
            flash("User already exists.", "error")
            return redirect(url_for("auth.register"))

        # Validate new password strength
        if not validate_password(password):
            flash("Password must be at least 8 characters long and contain upper, lower, and numeric characters.",
                  "error")
            return redirect(url_for("auth.register"))

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords must match.", "error")
            return redirect(url_for("auth.register"))

        # Create new user
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("main.home"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login.

    :return: Rendered login.html on GET or unsuccessful POST,
             or redirect to home page on success.
    """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if user exists
        user = User.query.filter_by(email=email).first()

        # Compare passwords
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main.home"))
        else:
            flash("Invalid login details.", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """
    Handle user logout.

    :return: Redirect to home page.
    """
    logout_user()
    return redirect(url_for("main.home"))


@auth_bp.route("/manage_account")
@login_required
def manage_account():
    """
    User account.

    :return: Rendered account.html.
    """
    return render_template("account.html")


@auth_bp.route("/update_email", methods=["POST"])
@login_required
def update_email():
    """
    Handle email update.

    :return: Rendered account.html.
    """
    new_email = request.form.get("email")

    user_exists = User.query.filter(User.email == new_email).first()

    # Check if user exists
    if user_exists:
        flash("Email already in use.", "error")
        return redirect(url_for("auth.manage_account"))

    # Update email
    current_user.email = new_email
    db.session.commit()

    flash("Email updated successfully!", "success")
    return redirect(url_for('auth.manage_account'))


@auth_bp.route("/change_password", methods=["POST"])
@login_required
def change_password():
    """
    Handle password change.

    :return: Rendered account.html.
    """
    old_password = request.form.get("old_password")
    new_password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    # Check current password
    if not check_password_hash(current_user.password, old_password):
        flash("Current password is incorrect.", "error")
        return redirect(url_for('auth.manage_account'))

    # Validate new password strength
    if not validate_password(new_password):
        flash("Password must be at least 8 characters long and contain upper, lower, and numeric characters.", "error")
        return redirect(url_for("auth.manage_account"))

    # Check if new passwords matches old password
    if check_password_hash(current_user.password, new_password):
        flash("New passwords cannot be the same as current password.", "error")
        return redirect(url_for("auth.manage_account"))

    # Check if passwords match
    if new_password != confirm_password:
        flash("Passwords must match.", "error")
        return redirect(url_for("auth.manage_account"))

    # Update password
    current_user.password = generate_password_hash(new_password)
    db.session.commit()

    flash("Password updated successfully!", "success")
    return redirect(url_for('auth.manage_account'))


@auth_bp.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    """
    Handle account deletion.

    :return: Redirect to home page if account is deleted.
    """
    user = db.session.get(User, current_user.id)

    # Delete user
    db.session.delete(user)
    db.session.commit()

    flash("Account deleted successfully!", "success")
    return redirect(url_for('auth.login'))


def validate_password(pw: str):
    """
    Handle password validation.

    :param pw: Password.

    :return: True if password is valid, otherwise False.
    """
    if len(pw) < 8:
        return False
    if not re.search(r"[A-Z]", pw):
        return False
    if not re.search(r"[a-z]", pw):
        return False
    if not re.search(r"[0-9]", pw):
        return False
    return True
