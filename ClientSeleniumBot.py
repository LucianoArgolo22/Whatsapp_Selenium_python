#%%
import time
from typing import Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class SeleniumBot():
  def __init__(self, options:Any, data_dict:dict) -> None:
    self.driver = webdriver.Chrome(options=options)
    self.data_dict = data_dict 
    self.vars = {}
  
  def teardown_method(self) -> None:
    self.driver.quit()

  def wait_for(self, timeout:int=10, values:tuple=(By.CSS_SELECTOR, ".selectable-text") ) -> None:
    WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(values))
  
  def find_elementV2(self, values:tuple) -> Any:
    self.wait_for(timeout=15, values=values)
    return self.driver.find_element(values[0], values[1])

  def find_chat(self, number_or_groupid:str) -> None:
    element = self.find_elementV2(values=(By.CSS_SELECTOR, ".selectable-text"))
    element.click()
    element.send_keys(number_or_groupid)
    element.send_keys(Keys.ENTER)

  def send_message(self, message:str) -> None:
    if isinstance(message, list):
      for msg in message:
          element = self.find_elementV2(values=(By.CSS_SELECTOR, ".\\_3Uu1_ .selectable-text"))
          element.send_keys(msg)
          element.send_keys(Keys.ENTER)
    else:
      element = self.find_elementV2(values=(By.CSS_SELECTOR, ".\\_3Uu1_ .selectable-text"))
      element.send_keys(message)
      element.send_keys(Keys.ENTER)

  def send_message_for_all(self) -> None:
    for key, values in self.data_dict.items():
      self.find_chat(number_or_groupid=key)
      self.send_message(values)

  def close_tab(self) -> None:
      time.sleep(1)
      self.driver.quit()

  def run_sending(self) -> None:
    self.driver.get("https://web.whatsapp.com/")
    self.driver.set_window_size(1936, 1048)
    self.send_message_for_all()
    self.close_tab()




#%%
if __name__ == '__main__':
  data_dict_test = {'tel_number': ['hola', 'cómo', 'estás?'],
                     'name_of_user or name_of_group': ['hi', 'how', 'are', 'you?']}

  options = webdriver.ChromeOptions()
  # Specify the path to your Chrome profile
  options.add_argument("--user-data-dir=C:\\Users\\username\\AppData\\Local\\Google\\Chrome\\User Data")
  bot = SeleniumBot(options=options, data_dict=data_dict_test)
  bot.run_sending()
