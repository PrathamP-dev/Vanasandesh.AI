from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key="AIzaSyCnNw-CNK0xvBynnY5BWobT9_aX9uNtj8A")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

app = Flask(__name__)

# Load environment variables (for email)
load_dotenv()

@app.route('/')
def index():
    status_filter = request.args.get('status', 'All')

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    if status_filter == 'All':
        cursor.execute("SELECT * FROM articles")
    else:
        cursor.execute("SELECT * FROM articles WHERE approval_status = ?", (status_filter,))

    articles = cursor.fetchall()
    connection.close()

    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Moderation Dashboard</title>
        <link rel="stylesheet"
              href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
        <style>
            body { background-color: #f5f5f5; padding: 30px; }
            .article-card {
                background: #fff; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                padding: 20px; margin-bottom: 20px;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .article-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            }
            .article-title { font-size: 1.4rem; font-weight: bold; }
            .published-date { font-size: 0.9rem; color: #888; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="mb-4"> Forestry News Moderation Dashboard</h1>

            <form method="get" action="/" class="mb-4">
                <select name="status" class="form-select w-25 d-inline-block">
                    <option value="All" {% if status_filter=='All' %}selected{% endif %}>All</option>
                    <option value="Pending" {% if status_filter=='Pending' %}selected{% endif %}>Pending</option>
                    <option value="Approved" {% if status_filter=='Approved' %}selected{% endif %}>Approved</option>
                    <option value="Rejected" {% if status_filter=='Rejected' %}selected{% endif %}>Rejected</option>
                </select>
                <button type="submit" class="btn btn-primary">Filter</button>
            </form>

            {% for article in articles %}
                <div class="article-card">
                    <div class="article-title">{{ article[1] }}</div>
                    <p class="published-date">Published: {{ article[3] }}</p>
                    <p><strong>Status:</strong> {{ article[4] }}</p>
                    <a href="{{ article[2] }}" class="btn btn-sm btn-primary mb-2" target="_blank">🔗 Read Article</a>
                    <div>
                        <a href="/approve/{{ article[0] }}" class="btn btn-success btn-sm"> Approve</a>
                        <a href="/reject/{{ article[0] }}" class="btn btn-danger btn-sm"> Reject</a>
                        <a href="/summarize/{{ article[0] }}" class="btn btn-warning btn-sm"> Summarize</a>
                    </div>
                    {% if article[5] %}
                        <p><strong>Summary:</strong> {{ article[5] }}</p>
                    {% endif %}
                </div>
            {% else %}
                <p>No articles available.</p>
            {% endfor %}
        </div>
    </body>
    </html>
    '''

    return render_template_string(html_template, articles=articles, status_filter=status_filter)


@app.route('/approve/<int:article_id>')
def approve_article(article_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    # Get article details
    cursor.execute("SELECT title, link FROM articles WHERE id = ?", (article_id,))
    result = cursor.fetchone()

    if result:
        title, link = result
        send_notification_email(title, link)

    # Update approval status
    cursor.execute("UPDATE articles SET approval_status = 'Approved' WHERE id = ?", (article_id,))
    connection.commit()
    connection.close()
    return "<script>window.location.href='/'</script>"


@app.route('/reject/<int:article_id>')
def reject_article(article_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("UPDATE articles SET approval_status = 'Rejected' WHERE id = ?", (article_id,))
    connection.commit()
    connection.close()
    return "<script>window.location.href='/'</script>"


@app.route('/summarize/<int:article_id>')
def summarize_article(article_id):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title, content FROM articles WHERE id=?", (article_id,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            print(f"⚠️ No article found with ID {article_id}")
            return redirect(url_for("index"))

        title, content = result
        print(f"🔍 Summarizing: {title}")

        # Gemini prompt
        prompt = f"""
Summarize this news article in under 250 words. Keep it factual and readable:

Title: {title}
Content: {content}
"""

        # Generate summary from Gemini
        response = model.generate_content(prompt)
        summary = response.text.strip()
        print(f"✅ Summary Generated: {summary[:100]}...")  # Show first 100 chars for debug

        # Save summary to DB
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE articles SET summary=? WHERE id=?", (summary, article_id))
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"❌ Error summarizing: {e}")

    return redirect(url_for("index"))


def send_notification_email(title, link):
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    portal_url = os.getenv("PORTAL_URL")

    msg = EmailMessage()
    msg['Subject'] = f'✅ New Approved Forestry Article: {title}'
    msg['From'] = email_user
    msg['To'] = email_user

    msg.set_content(f'''
A new article has been approved!

Title: {title}
Original Link: {link}

View it on the portal: {portal_url}
''')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)


if __name__ == '__main__':
    app.run(debug=True)
