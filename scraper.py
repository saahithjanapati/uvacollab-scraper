from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import urllib
import requests
import time

class Folder:
    def __init__(self, name, parent=None, children=[]):
        self.parent = parent
        self.children = children


class Scraper:
    def __init__(self, download_base_dir):
        """initializes Scraper object"""
        self.download_base_dir = download_base_dir
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": download_base_dir,
                "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally":True}
        options.add_experimental_option('prefs', prefs)
        
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        self.ac = ActionChains(self.driver)


    # def download_documents_on_page(self, class_names=['fa-file-pdf-o', 'fa-file-ppt-o']):
    #     """downloads all documents with given class on page (default document type is pdfs, but can change to powerpoint by changing class_name to fa-file-powerpoint-o"""
    #     job_list = []
    #     names = []
    #     for class_name in class_names:
    #         job_list = job_list + self.driver.find_elements_by_class_name(class_name)
    #     for job in job_list:
    #         names.append(urllib.parse.unquote(job.get_attribute('href').split("/")[-1]))
    #         job.click()
    #     return names
    

    def open_folders(self):
        """opens all folders (and subfolders) on screen"""
        # while(job_list)
        job_list = self.driver.find_elements_by_class_name("fa-folder")
        opened = 0
        while(len(job_list) > 0):
            job = job_list[0]
            # input("next step")
            
            time.sleep(1.5)
            self.ac.move_to_element(job).move_by_offset(-100, 0).click().perform()
            print("opening ", job.get_attribute('href'))
            try:
                job.click()
                opened += 1

            except:
                print("retrying")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # print("opened ", job.get_attribute('href'))
            job_list = self.driver.find_elements_by_class_name("fa-folder")
    


    def scrape(self):
        """does the scraping"""
        job_list = []
        folder_stack = []
        class_names = ['fa-file-pdf-o', 'fa-file-powerpoint-o', 'fa-file-word-o', 'fa-folder-open']
        for class_name in class_names:
            job_list += self.driver.find_elements_by_class_name(class_name)
        job_list = sorted(job_list, key=lambda job: job.location['y'])
        for job in job_list:
            print(job.get_attribute("href"), job.location['y'])
        
        print("\n"*5)

        name_elements = self.driver.find_elements_by_class_name("resource-name")
        names = []
        for elem in name_elements:
            # print(elem.text, elem.location['y'])
            names.append((elem.text, elem.location['y']))
        
        
        for job in job_list:
            for name, y in names:
                if job.location['y'] == y+3:
                    print(job.get_attribute("class"), name, job.location['x'])
                    break




def main():
    BASE_DIR = "/Users/saahith/Desktop/uvacollab-scraper/test/"
    my_scraper = Scraper(BASE_DIR)

    done = input("enter something when you have navigated to the page")
    my_scraper.open_folders()
    my_scraper.scrape()


    # print("waiting time is done")
    # links_with_names = my_scraper.download_documents_on_page()
    # done = input("terminate the program once everything is finished downloaded")

    
    
    # for link, name in links_with_names:
    #     my_scraper.download_file_to_dir(link, base_dir+name)
    

    # print(list(links_with_names))

if __name__ == "__main__":
    main()