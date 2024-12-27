import random
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from pymongo import MongoClient
from datetime import datetime
from uuid import uuid4
import os
import random
from dotenv import load_dotenv

# Load configurations
base_dir = os.path.dirname(os.path.abspath(__file__))
proxy_config_path = os.path.join(base_dir, '../config/proxy_config.json')


with open(proxy_config_path, 'r') as f:
    proxy_config = json.load(f)



# Load environment variables from .env file
load_dotenv()

# Get the MongoDB configuration from environment variables
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")  
db_name = os.getenv("DB_NAME", "twitter_trends") 
collection_name = os.getenv("COLLECTION_NAME", "trends") 
account_username = os.getenv("TWITTER_USERNAME", "none")  
account_password = os.getenv("TWITTER_PASSWORD", "none")  
account_mail = os.getenv("TWITTER_MAIL", "none")  

# MongoDB setup
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]


# Test MongoDB connection
try:
    client.server_info()  
    print("Connected to MongoDB successfully.")
except Exception as e:
    print(f"MongoDB connection failed: {e}")

# Get proxy URLs
proxy_urls = proxy_config.get("proxy_urls", [])



# Selenium setup
def get_driver(proxy_url=None):
    def is_proxy_responsive(driver):
        """Check if the proxy driver is responsive."""
        try:
            driver.get("http://www.google.com")
            time.sleep(5)  
            
            driver.find_element(By.NAME, "q")  # Google's search box
            print("Proxy is responsive.")
            return True
        except (WebDriverException, NoSuchElementException):
            print("Proxy is not responsive.")
            return False
        
    # Create driver with proxy if proxy_url is provided
    options = webdriver.ChromeOptions()
    if proxy_url:
        options.add_argument(f"--proxy-server={proxy_url}")
        print(f"Trying to use proxy: {proxy_url}")
    else:
        print("No proxy is being used.")
    
    # Common options
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")

    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to chromedriver.exe
    chromedriver_path = os.path.join(current_dir, "../chromedriver-win64/chromedriver-win64/chromedriver.exe")
    
    driver_service = Service(chromedriver_path)

    driver = webdriver.Chrome(service=driver_service, options=options)
    
    # Check if the proxy is responsive
    if proxy_url and not is_proxy_responsive(driver):
        print("Proxy is not responsive. Retrying without proxy...")
        driver.quit()  # Close the proxy-enabled driver
        
        # Create a new driver without proxy
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-extensions")
        driver = webdriver.Chrome(service=driver_service, options=options)
    
    return driver


def get_ip_address(driver):
    """Retrieve the public IP address using a WebDriver."""
    try:
        # Navigate to a site that shows the public IP
        driver.get("https://httpbin.org/ip")
        
        # Extract the IP address from the page's body
        body_text = driver.find_element(By.TAG_NAME, "body").text
        print(f"Response body: {body_text}")  # Debug output
        
        # Assuming the response is in JSON format: {"origin":"<IP Address>"}
        ip_address = eval(body_text).get("origin") 
        return ip_address
    except Exception as e:
        print(f"Error retrieving IP address: {e}")
        return None




def scrape_trending_topics():
    print("Function called")
    # Randomly select one proxy URL or None for no proxy
    proxie_to_try = random.choice(proxy_urls) if proxy_urls else None
    

    try:
            # Use proxy if available, otherwise fallback to no proxy
            proxy_url = proxie_to_try if proxie_to_try else None
            driver = get_driver(proxy_url)
            
            # Scraping logic
            driver.get("https://twitter.com/login")
            time.sleep(3)

            # Twitter login logic
            try:
                # Wait for username input field and enter the username
                username = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, "//input[@name='text']"))
                )
                username.send_keys(account_username)
                
                # Click the 'Next' button
                next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
                next_button.click()
                time.sleep(3)

                try:
                    # Try to find the email input field, if it exists
                    mail = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, "//input[@name='text']"))
                    )
                    if mail.is_displayed():
                        # If the email field is visible, fill in the email
                        mail.send_keys("ashutoshkorde411@gmail.com")
                        next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
                        next_button.click()
                        time.sleep(3)
                except Exception as e:
                    # If email field is not found, continue to the password page
                    print("No email field, proceeding to password.")

                # Wait for password input field and enter the password
                password = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, "//input[@name='password']"))
                )
                password.send_keys(account_password)

                # Click the 'Log in' button
                log_in = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
                log_in.click()
                time.sleep(5)
                
                print("Login successful.")

            except Exception as e:
                print("Error during login:", e)
                raise

            # Navigate to the Explore section
            try:
                explore_link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Search and explore']"))
                )
                explore_link.click()
                print("Navigated to 'Explore' section.")
            
            except Exception as e:
                print("Failed to navigate to 'Explore':", e)


            # Waiting for the "Trending" link to be visible
        
            try:
                trending_section = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//a[contains(@href, '/explore/tabs/trending') and contains(., 'Trending')]")
                    )
                )
                print("Trending section located.")
                
                # Click on the "Trending" link
                trending_section.click()
                print("Navigated to the 'Trending' section.")
            except Exception as e:
                print(f"An error occurred while navigating to the Trending section: {e}")

            # Scrape trending topics
            text_list = []
            try:
                div_elements = WebDriverWait(driver, 30).until(
                    EC.visibility_of_all_elements_located(
                        (By.XPATH, "//div[@data-testid='trend']")
                    )
                )
                print(f"Number of div elements found: {len(div_elements)}")

                for outer_div in div_elements:
                    try:
                        inner_div = outer_div.find_element(By.XPATH, "./div")
                        number = inner_div.find_element(By.XPATH, "./div[1]/div[1]/span").text
                        print(number)
                        text = inner_div.find_element(By.XPATH, "./div[2]/span").text
                        text_list.append(text)
                    except Exception as e:
                        print(f"Error extracting text from a div: {e}")

                print("Extracted Texts:", text_list)

            except Exception as e:
                print(f"An error occurred while scraping: {e}")

            # Generate record
            unique_id = str(uuid4())
            ip_address =  get_ip_address(driver)
            record = {
                "_id": unique_id,
                "trends": text_list[0:5],
                "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ip_address": ip_address
            }

            # Store in MongoDB
            try:
                collection.insert_one(record)
                print("Record inserted into MongoDB successfully.")
            except Exception as e:
                print(f"Failed to insert record into MongoDB: {e}")

            return record

    except Exception as e:
        print(f"Failed to extract trends: {e}")
        driver.quit()
    

    finally:
        driver.quit()

    
        