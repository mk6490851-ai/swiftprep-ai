import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq
import pdfplumber

load_dotenv()

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend/templates")
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_memory = []

# ================= FRONTEND =================
@app.route("/")
def index():
    return send_from_directory("../frontend/templates", "index.html")

@app.route("/recruiter")
def recruiter():
    return send_from_directory("../frontend/templates", "recruiter.html")

# ================= AI =================
def ask_ai(messages):
    try:
        try:
            chat = client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile"
            )
        except:
            chat = client.chat.completions.create(
                messages=messages,
                model="llama-3.1-8b-instant"
            )

        return chat.choices[0].message.content

    except Exception as e:
        return "Error: " + str(e)

# ================= INTERVIEW =================
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    job = data.get("job")
    skills = data.get("skills")

    messages = [
        {"role": "user", "content": f"I am a {job}. Skills: {skills}. Give 5 interview questions."}
    ]

    return jsonify({"text": ask_ai(messages)})

# ================= ATS =================
@app.route("/ats", methods=["POST"])
def ats():
    file = request.files.get("resume")
    job = request.form.get("job")

    resume_text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            resume_text += page.extract_text() or ""

    messages = [
        {"role": "user", "content": f"""
Compare resume with job description.

Resume:
{resume_text[:3000]}

Job:
{job}

Give score %, missing skills, suggestions
"""}
    ]

    return jsonify({"text": ask_ai(messages)})

# ================= AI INTERVIEW =================
@app.route("/interview", methods=["POST"])
def interview():
    data = request.get_json()
    answer = data.get("answer")

    conversation_memory.append({"role": "user", "content": answer})

    messages = [{"role": "system", "content": "You are an interviewer. Ask follow-up questions."}] + conversation_memory

    reply = ask_ai(messages)

    conversation_memory.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})

# ================= RESUME FIX =================
@app.route("/fix-resume", methods=["POST"])
def fix_resume():
    data = request.get_json()
    text = data.get("resume")

    messages = [{"role": "user", "content": f"Improve this resume:\n{text}"}]

    return jsonify({"fixed": ask_ai(messages)})

# ================= RESUME FIX PDF =================
@app.route("/fix-resume-pdf", methods=["POST"])
def fix_resume_pdf():
    file = request.files.get("resume")

    resume_text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            resume_text += page.extract_text() or ""

    messages = [{"role": "user", "content": f"Improve this resume:\n{resume_text[:3000]}"}]

    return jsonify({"fixed": ask_ai(messages)})
@app.route("/health")
def health():
    return {"status": "ok"}, 200

# ================= RUN =================
if __name__ == "__main__":
 app.run(host="0.0.0.0", port=10000)
