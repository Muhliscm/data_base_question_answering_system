from flask import Blueprint, render_template, request, flash
from .langchain_helper import few_shot_query_selector

db_chain, db_info = few_shot_query_selector()

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    return render_template("home.html")


@views.route('/chat-bot', methods=["GET", "POST"])
def chat_bot():
    result = ""
    if request.method == "POST":
        question = request.form.get('question')
        if not question:
            flash("Field is empty", category='error')
        else:
            flash("Question submitted", category='success')
            result = db_chain.run(question)

    return render_template('chat_bot.html', result=result)
