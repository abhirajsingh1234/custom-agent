from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import urllib.parse
import os

def send_whatsapp_message( phone_number, message,country_code="91", headless=True):
    """
    Send a WhatsApp message using Selenium with automatic session expiration detection.
    
    Parameters:
    country_code (str): Country code without any + sign (e.g., "1" for US/Canada)
    phone_number (str): Phone number without country code
    message (str): The message to be sent
    headless (bool): Whether to run in headless mode (default: True)
    
    Returns:
    bool: True if successful, False otherwise
    """
    driver = None
    try:
        # Create profile directory if it doesn't exist
        profile_dir = os.path.join(os.getcwd(), "chrome_profile")
        os.makedirs(profile_dir, exist_ok=True)
        if len(phone_number) != 10:
            return 'context: tell user to provide a valid phone number'
        # Prepare full phone number and encode message
        full_phone = f"{country_code}{phone_number}"
        encoded_message = urllib.parse.quote(message)
        
        # Configure Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")  # Updated headless flag
        
        # Common options to make Chrome more stable
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1280,720")
        
        # Path to store user data to maintain login sessions
        chrome_options.add_argument(f"--user-data-dir={profile_dir}")
        
        # Service object to configure the driver
        service = Service()
        
        print("Starting Chrome browser...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Use direct WhatsApp API URL to open chat
        wa_url = f"https://web.whatsapp.com/send?phone={full_phone}&text={encoded_message}"
        print(f"Opening WhatsApp Web for {full_phone}...")
        driver.get(wa_url)
        
        # First check if we need to scan QR code
        try:
            # Check if QR code is present (session expired)
            qr_code_wait = WebDriverWait(driver, 5)
            qr_code = qr_code_wait.until(
                EC.presence_of_element_located((By.XPATH, '//canvas[@aria-label="Scan me!"]'))
            )
            
            if headless:
                print("\n*** SESSION EXPIRED - QR CODE NEEDS SCANNING ***")
                print("Please run the script again with headless=False to scan the QR code.")
                print("Example: send_whatsapp_message(country_code, phone_number, message, headless=False)")
                driver.quit()
                return False
            else:
                print("\nPlease scan the QR code with your WhatsApp app.")
                print("Waiting for scan...")
                # Wait longer for user to scan QR code
                WebDriverWait(driver, 120).until(
                    EC.invisibility_of_element_located((By.XPATH, '//canvas[@aria-label="Scan me!"]'))
                )
                print("QR code scanned successfully!")
        except TimeoutException:
            # QR code not found, session is likely active
            pass
        
        # Now wait for the send button to appear
        print("Waiting for WhatsApp Web to load...")
        send_button_xpath = '//span[@data-icon="send"]'
        wait = WebDriverWait(driver, 60)
        send_button = wait.until(EC.element_to_be_clickable((By.XPATH, send_button_xpath)))
        
        # Click send button
        time.sleep(2)  # Small delay to ensure everything is ready
        send_button.click()
        print("Message sent successfully!")
        
        # Wait a bit before closing to ensure message is sent
        time.sleep(3)
        driver.quit()
        return f'whatsapp message " {message}" was sent to number {full_phone}'

        
    except TimeoutException:
        if headless:
            print("\n*** SESSION MAY HAVE EXPIRED ***")
            print("Failed to load WhatsApp Web or send button not found.")
            print("Please run the script again with headless=False to check if you need to scan the QR code.")
            print("Example: send_whatsapp_message(country_code, phone_number, message, headless=False)")
        else:
            print("\nFailed to load WhatsApp Web or send button not found.")
            print("Please check your internet connection and try again.")
        
        if driver:
            driver.quit()
        return False
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if driver:
            try:
                driver.quit()
            except:
                pass
        return False


# # Example usage
# if __name__ == "__main__":
#     print("WhatsApp Message Sender")
#     print("=======================")
    
#     # Set headless to False for first run or if you need to scan the QR code again
#     # Set headless to True for background operation after successful authentication
#     result = send_whatsapp_message(
#         country_code="91",      # Replace with your country code
#         phone_number="8450995752",  # Replace with the recipient's phone number
#         message="Hello! This is a test message sent using Python.",
#         headless=True  # Set to False if you need to scan QR code
#     )
    
#     if not result:
#         print("\nMessage sending failed. Please check the error messages above.")
#     else:
#         print("\nOperation completed successfully.")