# historical-bot
# 🧠 Histomind: Conversational Historical Roleplay Bot

Histomind is an interactive AI-powered chatbot that allows users to engage in realistic conversations with famous historical figures like Mahatma Gandhi, Albert Einstein, B. R. Ambedkar, and Nelson Mandela.

Using Groq's LLaMA 3 model, each character responds in a style that reflects their **real-life experiences, ideologies, and speech patterns**, making it perfect for educational and immersive roleplay experiences.

---

## 🚀 Features

- 🎭 Realistic historical roleplay from multiple personalities
- 💬 Dynamic conversation interface with Tailwind CSS styling
- 🔄 AI-generated responses via [Groq API](https://groq.com)
- ⚡️ Fast and lightweight (No login or user auth)
- 🖼️ Custom UI with historical-themed design
- 🧠 Separate system prompt logic per character

---

## 📁 Project Structure

historical-bot/
├── backend/
│ ├── views.py
│ ├── urls.py
│ ├── settings.py
│ └── ...
├── templates/
│ └── index.html
├── static/
│ └── images/
│ ├── logo.jpg
│ └── logo2.jpg
├── db.sqlite3
└── manage.py


---

## 🛠️ Requirements

This project does **not** use a `requirements.txt`, but make sure the following Python packages are installed:

```bash
cd path/to/historical-bot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

or

pip install django
pip install djangorestframework
pip install groq
pip install python-dotenv

## ⚙️ Environment Setup



GROQ_API_KEY=your_groq_api_key



python manage.py makemigrations
python manage.py migrate



python manage.py runserver
##  Open your browser and visit:

http://127.0.0.1:8000/
