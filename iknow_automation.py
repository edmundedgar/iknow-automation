from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import platform
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    
    # Handle Linux installation
    if platform.system() == 'Linux':
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Use system Chrome if available
        try:
            service = Service('/usr/bin/chromedriver')
            return webdriver.Chrome(service=service, options=chrome_options)
        except:
            # Fall back to webdriver-manager
            service = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=chrome_options)
    else:
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

def login(driver):
    try:
        print("Navigating to login page...")
        driver.get("https://iknow.jp/login")
        time.sleep(2)  # Give page time to load
        
        print("Looking for login form...")
        # Try multiple possible selectors for username field
        username_selectors = [
            "#user_login",
            "input[name='user[login]']",
            "input[name='login']",
            "input[type='text']"
        ]
        
        username_input = None
        for selector in username_selectors:
            try:
                print(f"Trying selector: {selector}")
                username_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if username_input:
                    print(f"Found username field with selector: {selector}")
                    break
            except:
                continue
        
        if not username_input:
            raise Exception("Could not find username field")
            
        print("Entering username...")
        username_input.clear()
        username_input.send_keys(os.getenv('IKNOW_USERNAME'))
        
        print("Looking for password field...")
        # Try multiple possible selectors for password field
        password_selectors = [
            "#user_password",
            "input[name='user[password]']",
            "input[name='password']",
            "input[type='password']"
        ]
        
        password_input = None
        for selector in password_selectors:
            try:
                print(f"Trying selector: {selector}")
                password_input = driver.find_element(By.CSS_SELECTOR, selector)
                if password_input:
                    print(f"Found password field with selector: {selector}")
                    break
            except:
                continue
                
        if not password_input:
            raise Exception("Could not find password field")
            
        print("Entering password...")
        password_input.clear()
        password_input.send_keys(os.getenv('IKNOW_PASSWORD'))
        
        print("Looking for submit button...")
        # Try multiple possible selectors for submit button
        submit_selectors = [
            "input[type='submit']",
            "button[type='submit']",
            ".submit",
            "input.submit"
        ]
        
        submit_button = None
        for selector in submit_selectors:
            try:
                print(f"Trying selector: {selector}")
                submit_button = driver.find_element(By.CSS_SELECTOR, selector)
                if submit_button:
                    print(f"Found submit button with selector: {selector}")
                    break
            except:
                continue
                
        if not submit_button:
            raise Exception("Could not find submit button")
            
        print("Clicking submit...")
        submit_button.click()
        
        print("Waiting for login to complete...")
        time.sleep(5)  # Give more time for login to complete
        
        # Check if we're logged in by looking for elements that only appear when logged in
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".user_badge"))
            )
            print("Login successful!")
        except:
            print("Login may have failed - could not find user badge")
            raise
        
    except Exception as e:
        print(f"Error during login: {e}")
        print("Current URL:", driver.current_url)
        print("Page source:", driver.page_source[:1000])  # Print first 1000 chars of page source
        raise

def add_vocabulary(driver, word, pinyin, meaning):
    try:
        print("Navigating to add item page...")
        course_id = os.getenv('IKNOW_COURSE_ID')
        driver.get(f"https://iknow.jp/custom/courses/{course_id}#!/new")
        time.sleep(2)  # Give page time to load
        
        print("Looking for form fields...")
        # Try multiple possible selectors for each field
        word_selectors = [
            "input[data-field='cue']",
            "input[name='cue']",
            "input.word"
        ]
        
        word_input = None
        for selector in word_selectors:
            try:
                print(f"Trying word selector: {selector}")
                word_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if word_input:
                    print(f"Found word field with selector: {selector}")
                    break
            except:
                continue
                
        if not word_input:
            raise Exception("Could not find word field")
            
        print("Entering word...")
        word_input.clear()
        word_input.send_keys(word)
        
        pinyin_selectors = [
            "input[data-field='transliteration']",
            "input[name='transliteration']",
            "input.pinyin"
        ]
        
        pinyin_input = None
        for selector in pinyin_selectors:
            try:
                print(f"Trying pinyin selector: {selector}")
                pinyin_input = driver.find_element(By.CSS_SELECTOR, selector)
                if pinyin_input:
                    print(f"Found pinyin field with selector: {selector}")
                    break
            except:
                continue
                
        if not pinyin_input:
            raise Exception("Could not find pinyin field")
            
        print("Entering pinyin...")
        pinyin_input.clear()
        pinyin_input.send_keys(pinyin)
        
        meaning_selectors = [
            "input[data-field='response']",
            "input[name='response']",
            "input.meaning"
        ]
        
        meaning_input = None
        for selector in meaning_selectors:
            try:
                print(f"Trying meaning selector: {selector}")
                meaning_input = driver.find_element(By.CSS_SELECTOR, selector)
                if meaning_input:
                    print(f"Found meaning field with selector: {selector}")
                    break
            except:
                continue
                
        if not meaning_input:
            raise Exception("Could not find meaning field")
            
        print("Entering meaning...")
        meaning_input.clear()
        meaning_input.send_keys(meaning)
        
        print("Looking for submit button...")
        # Wait for the new_item form to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li#new_item"))
        )
        
        # Find the submit button within li#new_item
        submit_button = driver.find_element(By.CSS_SELECTOR, "li#new_item input[type='submit']")
        if not submit_button:
            raise Exception("Could not find submit button in new_item form")
            
        print("Clicking submit...")
        submit_button.click()
        
        print("Waiting for submission to complete...")
        time.sleep(2)
        
    except Exception as e:
        print(f"Error adding vocabulary: {e}")
        print("Current URL:", driver.current_url)
        print("Page source:", driver.page_source[:1000])  # Print first 1000 chars of page source
        raise

def main():
    driver = setup_driver()
    
    # Login first
    login(driver)
    
    # Example usage
    vocabulary_items = [
        ("你好", "nǐ hǎo", "hello"),
        # Add more items here
    ]
    
    for word, pinyin, meaning in vocabulary_items:
        add_vocabulary(driver, word, pinyin, meaning)
    
    driver.quit()

if __name__ == "__main__":
    main() 