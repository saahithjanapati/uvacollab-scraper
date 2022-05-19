from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import urllib
import requests
import time

# chrome_options = Options()
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# #Change chrome driver path accordingly
# path_to_driver = "/Users/saahith/Desktop/uvacollab-scraper/chromedriver"
# driver = webdriver.Chrome(executable_path=path_to_driver, chrome_options=chrome_options)

# job_list = driver.find_elements(by=By.CLASS_NAME, value='fa fa-file-pdf-o')



class Scraper:
    def __init__(self, download_base_dir):

        self.download_base_dir = download_base_dir
        """initializes Scraper object"""

        options = webdriver.ChromeOptions()

        prefs = {"download.default_directory": download_base_dir,
                "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally":True,
        }

        options.add_experimental_option('prefs', prefs)
        # options.add_argument('--remote-debugging-port=9222')
        # options2.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # options2.add_experimental_option("download.prompt_for_download", False)
        # options2.add_experimental_option("download.directory_upgrade", True)
        # options2.add_experimental_option("plugins.always_open_pdf_externally", True) #It will not show PDF directly in chrome
        # options2.add_experimental_option("download.default_directory", download_base_dir)
        # # chrome_options.add_experimental_option('prefs', {"download.default_directory": download_base_dir, #Change default directory for downloads
        #"download.prompt_for_download": False, #To auto download the file
        # "download.directory_upgrade": True,
        # options2.add_experimental_option('prefs', {"debuggerAddress": "127.0.0.1:9222",
        #     "download.default_directory": download_base_dir, #Change default directory for downloads
        # "download.prompt_for_download": False, #To auto download the file
        # "download.directory_upgrade": True,
        # "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
        # "plugins.always_open_pdf_externally": True, #It will not show PDF directly in chrome
        # "download.extensions_to_open": "applications/pdf"
        # })
        
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        

        # path_to_driver = "/Users/saahith/Desktop/uvacollab-scraper/chromedriver"
        # self.driver = webdriver.Chrome(executable_path=path_to_driver, chrome_options=chrome_options)


    def download_documents_on_page(self, class_name='fa-file-pdf-o'):
        """downloads all documents with given class on page (default document type is pdfs, but can change to powerpoint by changing class_name to fa-file-powerpoint-o"""
        job_list = self.driver.find_elements_by_class_name(class_name)
        for job in job_list:
            job.click() # to download


def main():
    BASE_DIR = "/Users/saahith/Desktop/uvacollab-scraper/test/"
    my_scraper = Scraper(BASE_DIR)

    done = input("enter something when you have navigated to the page")
    print("waiting time is done")
    links_with_names = my_scraper.download_documents_on_page()
    
    
    # for link, name in links_with_names:
    #     my_scraper.download_file_to_dir(link, base_dir+name)
    

    # print(list(links_with_names))

if __name__ == "__main__":
    main()