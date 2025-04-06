import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Set up Selenium WebDriver
options = Options()
options.headless = True  # Run headless browser (no GUI)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Function to extract company info
def extract_companies_data(driver):
    companies = []

    # Find all rows containing company details (this is based on inspecting the website's structure)
    rows = driver.find_elements(By.XPATH, "//div[@class='qfc-informationResult']")
#//div[@class='qfc-informationResult']
    for row in rows:
        try:
            name = row.find_element(By.XPATH, ".//div[@class='EngFirmname']/a").text
            address = row.find_element(By.XPATH, ".//div[@class='description-item location-icon']/span").text
            companies.append([name, address])
        except Exception as e:
            print(f"Error extracting data: {e}")

    return companies


# Open the initial page
url = "https://eservices.qfc.qa/qfcpublicregister/publicregister.aspx"
driver.get(url)
time.sleep(5)  # Wait for the page to load

# List to store all companies and addresses
all_companies = []

# Loop through each page
for page_num in range(1, 3):  # 118 pages
    print(f"Scraping page {page_num}...")

    # Extract data from current page
    companies_on_page = extract_companies_data(driver)
    all_companies.extend(companies_on_page)

    # Check if data is being extracted
    if companies_on_page:
        for company in companies_on_page:
            print(f"Company Name: {company[0]}")
            print(f"Address: {company[1]}")
            print("-" * 40)
    else:
        print(f"No data found on page {page_num}")


    # Navigate to the next page (assuming there is a "Next" button)
    next_button = driver.find_element(By.XPATH, "//a[text()='>']")
    next_button.click()
    time.sleep(3)  # Wait for the next page to load

# Close the driver
driver.quit()

# Save the data to a CSV file
df = pd.DataFrame(all_companies, columns=["Company Name", "Address"])
df.to_csv("qfc_companies.csv", index=False)

print("Data extraction complete. Saved to qfc_companies.csv")