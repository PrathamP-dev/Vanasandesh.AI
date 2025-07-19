from newspaper import Article
import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Select articles where content is missing
cursor.execute("SELECT id, link FROM articles WHERE content IS NULL")
rows = cursor.fetchall()

print(f"Found {len(rows)} articles without content...")

for article_id, url in rows:
    try:
        print(f"Processing article ID: {article_id}")
        article = Article(url)
        article.download()
        article.parse()
        content = article.text.strip()

        if content:
            cursor.execute("UPDATE articles SET content = ? WHERE id = ?", (content, article_id))
            conn.commit()
            print(f"✅ Updated article {article_id}")
        else:
            print(f"⚠️ No content found for article {article_id}")
    except Exception as e:
        print(f"❌ Failed to process article ID {article_id}, URL: {url}, Error: {e}")

# Close the DB connection
conn.close()
print("Done filling content.")
