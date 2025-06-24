import sqlite3

def create_database():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT,
            published TEXT
        )
    ''')

    connection.commit()
    connection.close()


KEYWORDS = [
    "forest", "forestry", "wildlife", "forest department", "forest conservation",
    "afforestation", "deforestation", "biodiversity", "wildlife sanctuary",
    "national park", "nature reserve", "ecotourism", "forest officers",
    "forest cover", "green cover", "environmental clearance", "tree plantation",
    "environment ministry", "AI in forestry", "technology in forestry",
    "forest surveillance", "drones in forest", "satellite mapping", "remote sensing",
    "forest fire detection", "forest crime monitoring", "smart forest management",
    "forest monitoring systems", "smart cameras", "anti-poaching technology",
    "wildlife tracking", "camera traps", "GIS mapping", "forest innovation",
    "forest carbon mapping", "satellite imagery forestry", "environmental sensors",
    "geospatial analytics", "AI-powered surveillance", "forest tech startup",
    "forest AI project", "forest drone program", "forest data analytics",
    "AI in environmental conservation", "eco-monitoring", "environmental drones",
    "drone surveillance wildlife", "thermal imaging forest", "forest intelligence",
    "wildlife conservation technology", "technology for wildlife protection",
    "green technology", "environmental data analytics", "drone-based monitoring",
    "forest resource management", "forest data platform", "open forest data",
    "forest governance technology", "forest biodiversity AI", "forestry innovation",
    "forest crime prevention tech", "forest mapping AI", "forestry sensors"
]

import feedparser

# List of RSS feed URLs
rss_feeds = [
    # Indian News Sources
    "https://www.downtoearth.org.in/rss/news.xml",
    "https://www.thehindu.com/sci-tech/technology/feeder/default.rss",
    "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
    "https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml",
    
    # Global Environmental / Forestry News
    "https://news.mongabay.com/feed/",
    "https://www.unep.org/rss.xml",
    "https://www.environmentalleader.com/feed/",
    "https://earthobservatory.nasa.gov/blog/feed",
    "https://www.wwf.org.uk/rss.xml"
]

def collect_articles():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            article_title = entry.title.lower()

            if any(keyword.lower() in article_title for keyword in KEYWORDS):
                # Insert article into the database
                cursor.execute('''
                    INSERT INTO articles (title, link, published)
                    VALUES (?, ?, ?)
                ''', (entry.title, entry.link, entry.published))

                print(f"Saved: {entry.title}")

    connection.commit()
    connection.close()

# Create the database & table
create_database()

# Collect articles and save them
collect_articles()

import schedule
import time

def job():
    print("Running scheduled news collection...")
    collect_and_store_articles()  # Call your existing function here

# Schedule the job daily at 11:00 AM
schedule.every().day.at("11:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)

