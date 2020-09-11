import os
import time
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
load_dotenv()

# set up twilio
client = Client(os.getenv('ACCOUNT_SID'), os.getenv('AUTH_TOKEN'))

# set up selenium
browser = webdriver.Chrome(executable_path=r'C:\\Users\\Me\\chromedriver_win32\\chromedriver.exe')
browser.get('https://app.acuityscheduling.com/schedule.php?owner=20339976')

# dict feels better than list
location_dict = {
  0: 'Howell',
  1: 'Rochester Hills',
  2: 'Detroit',
  3: 'Westland'
}

def send_sms(location):
  '''
  Sends two texts.
  '''
  for dummy_int in range(2):
    client.api.account.messages.create(
      to = os.getenv('MY_PHONE'),
      from_ = os.getenv('TWILIO_PHONE'),
      body = f'{location}: appointment available!'
    )

def loop_locations(location_keys):
  '''
  Checks each location for available appointments every 60 seconds.
  Exits script after sending texts.
  '''
  location_elements = browser.find_elements_by_class_name('calendar-select-box')
  reset_element = location_elements.pop(0)

  while True:
    print(f'--- {time.strftime("%I:%M:%S%p", time.localtime())} ---')

    for i in range(len(location_keys)):
      location_elements[location_keys[i]].send_keys('seleniumhq' + Keys.RETURN)
      time.sleep(2)
      actions_element = browser.find_element_by_class_name('choose-time-actions')

      if actions_element.value_of_css_property('display') != 'none':
        print(f'{location_dict[location_keys[i]]}: appointment available!')
        send_sms(location_dict[location_keys[i]])
        return

      else:
        print(f'{location_dict[location_keys[i]]}: no appointments 😔')
        location_elements[location_keys[i]].send_keys('seleniumhq' + Keys.RETURN)
        time.sleep(2)

        # Use reset element to trigger network call if only one location
        if len(location_keys) == 1:
          for dummy_int in range(2):
            reset_element.send_keys('seleniumhq' + Keys.RETURN)
            time.sleep(2)

    time.sleep(60)

loop_locations([1, 3])
browser.quit()