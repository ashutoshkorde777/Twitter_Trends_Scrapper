# Twitter_Trends_Scrapper

## Overview
This project is a **Twitter Trends Scraper** built with **Flask**, **Selenium**, and **MongoDB**. It logs into Twitter, navigates to the trending section, scrapes the top trends, and stores the data in a MongoDB database. A Flask web interface allows you to run the scraper and view the results.

---

## Features
- **Scrape Trending Topics**: Automatically logs into Twitter and fetches trending topics.
- **Data Storage**: Stores scraped data in a MongoDB database with timestamp and IP address.
- **Web Interface**: A user-friendly Flask interface to trigger scraping and view results.
- **Proxy Support**: Configured for optional proxy usage to avoid rate limits.

---

## Installation and Running the Project

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/yourusername/twitter-trends-scraper.git
   cd twitter-trends-scraper
   ```
2. **Install Dependencies**
    ```bash
   pip install -r requirements.txt
   ```
3. **Set Up Environment Variables**  
   Create a `.env` file in the project root and add the following:

   ```bash
   MONGO_URI=mongodb://your-mongodb-host:your-port
   DB_NAME=your-database-name
   COLLECTION_NAME=your-collection-name
   TWITTER_USERNAME=your-twitter-username
   TWITTER_PASSWORD=your-twitter-password
   CHROMEDRIVER_PATH=/path/to/your/chromedriver
   ```

4. **Set Up Proxy URLs in config/proxy_config.json file**
 ```bash
   {
  "proxy_urls": [
      "http://USERNAME:PASSWORD@us-dc.proxymesh.com:31280"
      
  ]
}

   ```
5. **Start The Project**
    ```bash
      python app/main.py

   ```

---
## Preview
![Preview Screenshot](https://example.com/screenshot.png "Preview of Application")
