from quart import Quart, render_template, request, session
from dotenv import load_dotenv
from openai import OpenAI
import httpx
import random
import html
import os
import logging

load_dotenv()
client = OpenAI()
app = Quart(__name__)
app.secret_key = os.getenv("SECRET_KEY", "trivia-secret")
logging.basicConfig(level=logging.DEBUG)

TRIVIA_API_BASE = "https://opentdb.com/api.php?amount=1&type=multiple"
TRIVIA_CATEGORIES_API = "https://opentdb.com/api_category.php"

# Fetch list of categories
async def get_categories():
    async with httpx.AsyncClient() as client:
        response = await client.get(TRIVIA_CATEGORIES_API)
        data = response.json()
        return data["trivia_categories"]

# Fetch a trivia question
async def get_trivia_question(difficulty="medium", category_id=None):
    url = f"{TRIVIA_API_BASE}&difficulty={difficulty}"
    if category_id:
        url += f"&category={category_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        result = data["results"][0]

        question = html.unescape(result["question"])
        correct = html.unescape(result["correct_answer"])
        incorrect = [html.unescape(ans) for ans in result["incorrect_answers"]]
        all_answers = incorrect + [correct]
        random.shuffle(all_answers)

        return {
            "question": question,
            "correct_answer": correct,
            "answers": all_answers,
            "category": result["category"],
            "difficulty": difficulty
        }

# GPT explanation
async def get_gpt_explanation(question, correct_answer):
    prompt = (
        f"Explain why this trivia answer is correct:\n"
        f"Question: {question}\n"
        f"Correct answer: {correct_answer}"
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a trivia assistant who explains correct answers in 2-3 sentences."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

@app.route('/')
async def index():
    categories = await get_categories()
    return await render_template("index.html", trivia=None, feedback=None, explanation=None, categories=categories)

@app.route('/select_difficulty', methods=['POST'])
async def select_difficulty():
    form = await request.form
    difficulty = form.get("difficulty", "medium")
    category_id = form.get("category", None)
    session["difficulty"] = difficulty
    session["category"] = category_id
    trivia = await get_trivia_question(difficulty, category_id)
    categories = await get_categories()
    return await render_template("index.html", trivia=trivia, feedback=None, explanation=None, categories=categories)

@app.route('/submit', methods=['POST'])
async def submit():
    form = await request.form
    selected = form.get("answer")
    correct = form.get("correct_answer")
    question = form.get("question")
    category = form.get("category")
    difficulty = form.get("difficulty")
    answers = form.getlist("answers")

    feedback = "✅ Correct!" if selected == correct else f"❌ Wrong! The correct answer was: {correct}"
    explanation = await get_gpt_explanation(question, correct)
    categories = await get_categories()

    return await render_template(
        "index.html",
        trivia={
            "question": question,
            "correct_answer": correct,
            "answers": answers,
            "category": category,
            "difficulty": difficulty
        },
        feedback=feedback,
        explanation=explanation,
        categories=categories
    )

@app.route('/new', methods=['POST'])
async def new_question():
    difficulty = session.get("difficulty", "medium")
    category_id = session.get("category", None)
    trivia = await get_trivia_question(difficulty, category_id)
    categories = await get_categories()
    return await render_template("index.html", trivia=trivia, feedback=None, explanation=None, categories=categories)

@app.route('/reset', methods=['POST'])
async def reset():
    session.clear()
    categories = await get_categories()
    return await render_template("index.html", trivia=None, feedback=None, explanation=None, categories=categories)

if __name__ == '__main__':
    app.run(debug=True)
