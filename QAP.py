import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class QuickAdminPanel:
    def __init__(self, email=None, password=None, url=None):
        self.email = email
        self.password = password
        self.url = url
        self.file_failed = []
        self.path = []
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 100)

    def get_code(self):
        self._log_in()
        self._show_code()
        app_nav = self.wait.until(
            ec.presence_of_element_located(
                (By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/div[1]/div/div[1]/div')))
        app_nav.click()
        self._sleep(2)
        menu = self.wait.until(
            ec.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/div[1]/div')))
        files = menu.find_elements_by_class_name('fs-file')
        folders = menu.find_elements_by_class_name('fs-dir-closed')
        self.create_files(files_list=files, folder_name=None)
        self.create_folder(folder_list=folders)
        self._close()

    def create_files(self, files_list, folder_name=None):
        if folder_name is not None:
            os.system(f'mkdir {folder_name}')
        if len(files_list) > 0:
            for file in files_list:
                time.sleep(2)
                file.click()
                file_name = self.driver.find_element_by_xpath(
                    "/html/body/div[3]/div[1]/div/div/header/h5").text
                file_code = self.driver.find_element_by_xpath(
                    "/html/body/div[3]/div[1]/div/div/div/div/div[2]/pre/code").text
                try:
                    if folder_name is not None:
                        new_file = open(f'{folder_name}\\{file_name}', 'bw')
                        new_file.write(bytearray(file_code, encoding='utf8'))
                        new_file.close()
                    else:
                        new_file = open(f'{file_name}', 'bw')
                        new_file.write(bytearray(file_code, encoding='utf8'))
                        new_file.close()
                except UnicodeError:
                    self.file_failed.append(f'{folder_name}\\{file_name}')

    def create_folder(self, folder_list):
        if len(folder_list) > 0:
            for folder in folder_list:
                if folder.text not in self.path:
                    self.path.append(folder.text)
                time.sleep(2)
                folder.click()
                files = folder.find_element(
                    By.XPATH, '..').find_elements_by_class_name('fs-file')
                self.create_files(files, '\\'.join(self.path))
                folders = folder.find_element(
                    By.XPATH, '..').find_elements_by_class_name('fs-dir-closed')
                self.create_folder(folders)
                self.path.pop(-1)
                if len(self.path) == 1:
                    print(
                        "=====================================================================")
                    print(f"{folder.text} ==> Done")
                    print(
                        "=====================================================================")

    def _log_in(self):
        self._load_page()
        email_input = self.wait.until(
            ec.presence_of_element_located((By.ID, 'email')))
        email_input.clear()
        email_input.send_keys(self.email)
        password_input = self.wait.until(
            ec.presence_of_element_located((By.ID, 'password')))
        password_input.clear()
        password_input.send_keys(self.password)
        self.wait.until(ec.presence_of_element_located(
            (By.TAG_NAME, 'button'))).click()

    @staticmethod
    def _sleep(sec):
        time.sleep(sec)

    def _load_page(self):
        self.driver.get(self.url)
        time.sleep(5)

    def _show_code(self):
        # Get View Code nav bar
        view_code = self.wait.until(
            ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/aside/div/nav/ul/div[3]/li[3]')))
        view_code.click()
        self._sleep(20)

    def _close(self):
        print('==========================================\nEnd\n==========================================')
        self.driver.close()


if __name__ == '__main__':
    QAP = QuickAdminPanel(
        email='cedix84400@oramail.net',
        password='cedix84400@oramail.netas',
        url='https://2019.quickadminpanel.com/builder/30770/menu/index'
    )
    QAP.get_code()
