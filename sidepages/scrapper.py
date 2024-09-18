import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os, platform, subprocess, shutil
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def is_chrome_installed():
    system = platform.system().lower()
    if system == "darwin":
        return os.path.exists("/Applications/Google Chrome.app")
    elif system == "windows":
        return os.path.exists(r"C:\Program Files\Google\Chrome\Application\chrome.exe") or \
               os.path.exists(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
    elif system == "linux":
        return shutil.which("google-chrome") is not None
    else:
        print(f"Unsupported operating system: {system}")
        return False

def install_chrome():
    system = platform.system().lower()
    if system == "darwin":
        print("Installing Chrome for macOS...")
        subprocess.run(["brew", "install", "--cask", "google-chrome"], check=True)
    elif system == "windows":
        print("Installing Chrome for Windows...")
        subprocess.run(["powershell", "-Command", 
                        "Invoke-WebRequest -Uri 'https://dl.google.com/chrome/install/latest/chrome_installer.exe' -OutFile 'chrome_installer.exe'"], 
                       check=True)
        subprocess.run(["chrome_installer.exe", "/silent", "/install"], check=True)
        os.remove("chrome_installer.exe")
    elif system == "linux":
        print("Installing Chrome for Linux...")
        commands = [
            ["apt-get", "install", "-y", "sudo"],
            ["sudo", "apt-get", "update"],
            ["sudo", "apt-get", "install", "-y", "wget", "unzip"],
            ["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"],
            ["sudo", "apt", "install", "-y", "./google-chrome-stable_current_amd64.deb"],
            ["rm", "google-chrome-stable_current_amd64.deb"],
            ["sudo", "apt-get", "clean"]
        ]
        for cmd in commands:
            subprocess.run(cmd, check=True)
    else:
        print(f"Unsupported operating system: {system}")
        return

# Check if Chrome is installed, if not, install it
if not is_chrome_installed():
    print("Chrome not found. Installing...")
    install_chrome()
else:
    print("Chrome is already installed. Proceeding...")


def setup_driver():
    try:
        options = Options()
        driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)


        print("Driver initialized")
        return driver
    except:
        raise Exception("Failed to initialize driver")

def login_to_upwork(driver, username, password):
    try:
        driver.get("https://www.upwork.com/ab/account-security/login")
        print("Navigating to login page")

        time.sleep(5)

        # Wait for username field and enter username
        driver.find_element(By.ID, "login_username").send_keys(username)
        driver.find_element(By.ID, "login_password_continue").click()
        print("Clicked on continue button")
        time.sleep(5)
        # Wait for password field and enter password
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login_password")))
        driver.find_element(By.ID, "login_password").send_keys(password)
        driver.find_element(By.ID, "login_control_continue").click()
        print("Clicked on login button")
        # Wait for login to complete
        time.sleep(5)
        print("Logged in successfully")
    except:
        raise Exception("Failed to login to Upwork")

def search_and_extract_jobs(driver, search_query):
    try:
        driver.get(f"https://www.upwork.com/nx/jobs/search/?q={search_query}&sort=recency")
        # Wait for the page to load
        time.sleep(5) 

        job_elements = driver.find_elements(By.TAG_NAME, "article")
        jobs = []
        for job in job_elements:
            job_data = {}
            
            try:
                job_data["title"] = job.find_element(By.CSS_SELECTOR, "h2.job-tile-title").text
            except:
                job_data["title"] = None

            try:
                job_data["link"] = job.find_element(By.CSS_SELECTOR, "a.up-n-link").get_attribute("href")
            except:
                job_data["link"] = None

            try:
                job_data["description"] = job.find_element(By.CSS_SELECTOR, "p.mb-0.text-body-sm").text
            except:
                job_data["description"] = None

            try:
                client_info = job.find_element(By.CSS_SELECTOR, "ul[data-test='JobInfoClient']")
                job_data["payment_verified"] = bool(client_info.find_elements(By.CSS_SELECTOR, "li[data-test='payment-verified']"))
            except:
                job_data["payment_verified"] = None

            try:
                rating_elem = client_info.find_elements(By.CSS_SELECTOR, "div.air3-rating-foreground")
                job_data["client_rating"] = rating_elem[0].get_attribute("style").split(":")[-1].strip() if rating_elem else "N/A"
            except:
                job_data["client_rating"] = None

            try:
                job_data["total_spent"] = client_info.find_element(By.CSS_SELECTOR, "li[data-test='total-spent'] strong").text
            except:
                job_data["total_spent"] = None

            try:
                job_data["client_location"] = client_info.find_element(By.CSS_SELECTOR, "li[data-test='location']").text.strip()
            except:
                job_data["client_location"] = None

            try:
                job_info = job.find_element(By.CSS_SELECTOR, "ul[data-test='JobInfo']")
                job_data["job_type"] = job_info.find_element(By.CSS_SELECTOR, "li[data-test='job-type-label']").text
            except:
                job_data["job_type"] = None

            try:
                job_data["experience_level"] = job_info.find_element(By.CSS_SELECTOR, "li[data-test='experience-level']").text
            except:
                job_data["experience_level"] = None

            try:
                job_data["duration"] = job_info.find_element(By.CSS_SELECTOR, "li[data-test='duration-label']").text
            except:
                job_data["duration"] = None

            jobs.append(job_data)
        
        # close the driver
        print("driver closing")
        # driver.quit()
        print("driver closed")
        return jobs
    except:
        raise Exception("Failed to search and extract jobs")


def scrape_upwork_jobs(username, password, search_query):
    try:
        driver = setup_driver()
        login_to_upwork(driver, username, password)
        all_jobs = search_and_extract_jobs(driver, search_query)
        return all_jobs
    except Exception as e:
        print(f"An error occurred in scrape_upwork_jobs: {e}")
        return []
    finally:
        print("Closing the driver")
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error while closing the driver: {e}")
    

if __name__ == "__main__":
    try:
        # Example usage:
        username = ""
        password = ""
        search_query = "python developer"
        jobs = scrape_upwork_jobs(username, password, search_query)
        print(jobs)
        time.sleep(10)
    except:
        print("error")



