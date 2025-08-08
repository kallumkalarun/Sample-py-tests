
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 


# chrome_driver_path = r"C:\My Work Folder\Python\GE Projects\chromedriver.exe"

# # Create a Service object with the executable_path
# service = Service(executable_path=chrome_driver_path)

# # Pass the service object to the Chrome WebDriver
# driver = webdriver.Chrome(service=service)

# try:
#     driver.get("https://www.gianteagle.com")
#     print("Successfully opened GE.com!")
#     time.sleep(10)
#     # Your further scraping code goes here
#     search_box_xpath = "//input[@id='searchInput']" # Or "//textarea[@name='q']"
#     search_box = driver.find_element(By.XPATH, search_box_xpath)
#     search_box.send_keys("Milk")
#     search_box.submit()
#     time.sleep(15)
# except Exception as e:
#     print(f"An error occurred: {e}")

# finally:
#     if driver:
#         driver.quit()





driver = webdriver.Chrome()  
driver.get("https://www.gianteagle.com")


time.sleep(5)

driver.get("https://www.gianteagle.com")
print("Successfully opened GE.com!")
time.sleep(2)

search_box_xpath = "//input[@id='searchInput']" 
search_box = driver.find_element(By.XPATH, search_box_xpath)
search_box.send_keys("Milk")
search_box.submit()
time.sleep(10)

# # Scroll down to load more products if needed
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# time.sleep(3)

# soup = BeautifulSoup(driver.page_source, 'html.parser')

# products = soup.select("div.product-card")  # update selector
# for p in products:
#     desc = p.select_one(".product-title").text.strip()
#     price = p.select_one(".price").text.strip()
#     size = p.select_one(".product-size").text.strip()
#     print({"description": desc, "price": price, "size": size})

driver.quit()

