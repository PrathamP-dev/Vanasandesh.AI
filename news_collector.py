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
    # Existing Forestry & Wildlife Keywords
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
    "forest crime prevention tech", "forest mapping AI", "forestry sensors",
    
    # New Updated Tech Keywords for Forestry, Environment & Climate
    "Smart forestry", "precision forestry", "forest inventory", "forestry big data",
    "LiDAR", "SAR", "GIS", "monitoring", "MRV", "IoT", "digital twins",
    "traceability", "ecosystem services monitoring", "digital repository",
    "species identification app", "UAV", "sensors", "smart collars",
    "acoustic monitoring", "Forestry Technology", "Climate Change Technology",
    "Natural Resource Management Technology", "Forest 4.0", "Digital Transformation",
    "AI in Forestry", "Machine Learning in Forestry", "Wireless Sensor Networks (WSN)",
    "Blockchain in Forestry", "RFID", "Digital Survey Tools", "Intelligent Machines",
    "Big Data in Forestry", "Cloud Computing in Forestry", "Real-time Forest Monitoring",
    "Predictive Modeling", "Sustainable Forest Management", "Timber Supply Chain",
    "Forest Health Monitoring", "Ground-based Observations", "Computer Vision",
    "Satellite Imagery", "Drone Imagery", "Sensor Networks", "Blockchain Traceability",
    "Forest Certification", "Decentralized Systems", "Robotics in Forestry",
    "Robotic Automation", "Environmental Monitoring", "Fire Prevention",
    "Autonomous Robotic Systems", "Data Quality", "Human-in-the-Loop",
    "Digital Twin Systems", "Forest Digital Twin", "Carbon Storage Capacity",
    "Biodiversity Monitoring", "Data-driven Management Strategies", "Remote Sensing in Forestry",
    "Radar", "Multispectral Imagery", "Hyperspectral Imagery", "Thermal Remote Sensing",
    "Forest Cover Mapping", "Change Detection", "Biomass Estimation", "Carbon Stock Estimation",
    "Fire Detection", "Damage Assessment", "Habitat Monitoring", "Illegal Logging Detection",
    "Forest Type Classification", "Reforestation Monitoring", "Soil Moisture Analysis",
    "REDD+", "REDD+ MRV", "National Forest Monitoring System", "GIS in Forestry",
    "GIS Applications", "Environmental Management", "Environmental Modeling",
    "Environmental Planning", "Spatial Analysis", "Land Use Change Detection",
    "Water Resource Mapping", "Watershed Analysis", "Land Degradation Assessment",
    "forestry dashboards", "Citizen Science", "Environmental Monitoring Platforms",
    "Big Data Analytics", "Green Data", "Energy Efficiency", "Sustainable Transportation",
    "Smart Grids", "Precision Agriculture", "Traffic Data Analysis",
    "Carbon Capture and Storage", "Waste Management Technology", "Renewable Energy",
    "Wind Power", "Carbon Credits", "Carbon Trading", "Green Blockchain",
    "Proof of Stake (PoS)", "Proof of Work (PoW)", "Net-Zero Carbon Emissions",
    "Biochar Technology", "Climate Change Mitigation tool", "Climate Change Adaptation tool",
    "Regulatory Technologies (RegTech)", "Geospatial Data Platforms",
    "Google Earth Engine", "Open Source Data Repositories", "Environmental IoT",
    "Connected Devices", "Carbon Footprint Reduction", "Edge Computing",
    "Decentralized Data Processing", "Real-time Environmental Insights",
    "Remote Monitoring", "Conservation Technologies", "environmental DNA (eDNA) forestry",
    "forestry innovation", "wildfire detection systems", "biodiversity assessment tools",
    "carbon stock assessment", "climate smart forestry app", "emerging tech in forestry"
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

    # Updated URLs
    "https://www.climatechange.ai/feed",  # Assuming this exists
    "https://www.neonscience.org/rss.xml",
    "https://www.usgs.gov/news/rss.xml",
    "https://climatetrace.org/rss",  # if available
    "https://resourcewatch.org/rss",
    "https://ourworldindata.org/feeds/all.rss",
    "https://www.oecd.org/rss.xml",
    "https://www.irena.org/rss",
    "https://www.fao.org/forest-resources-assessment/en/rss.xml",
    "https://www.un-redd.org/rss.xml",
    "https://www.greenclimate.fund/rss.xml",
    "https://www.ipcc.ch/feed",
    "https://www.ctc-n.org/rss",
    "https://www.dataone.org/rss",
    "https://www.data.gov/rss",
    "https://www.conservation.org/rss",
    "https://www.wri.org/rss.xml",
    "https://www.earthdata.nasa.gov/rss",
    "https://developers.google.com/earth-engine/rss"
]

def collect_articles():
    print("🟢 Collecting new articles from feeds...") 
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            article_title = entry.title.lower()

            if any(keyword.lower() in article_title for keyword in KEYWORDS):
                # Check if article link already exists in the database
                cursor.execute("SELECT * FROM articles WHERE link = ?", (entry.link,))
                existing_article = cursor.fetchone()

                if not existing_article:
                    # If not a duplicate, save it
                    cursor.execute('''
                        INSERT INTO articles (title, link, published)
                        VALUES (?, ?, ?)
                    ''', (entry.title, entry.link, entry.published))

                    print(f"✅ Saved: {entry.title}")
                else:
                    print(f"⚠️ Skipped duplicate: {entry.title}")

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
    collect_articles()  # Call your existing function here

# Schedule the job daily at 11:00 AM
schedule.every().day.at("11:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)

