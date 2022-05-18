from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# #Change chrome driver path accordingly
# path_to_driver = "/Users/saahith/Desktop/uvacollab-scraper/chromedriver"
# driver = webdriver.Chrome(executable_path=path_to_driver, chrome_options=chrome_options)

# job_list = driver.find_elements(by=By.CLASS_NAME, value='fa fa-file-pdf-o')



class Scraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        #Change chrome driver path accordingly
        # self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
        path_to_driver = "/Users/saahith/Desktop/uvacollab-scraper/chromedriver"
        self.driver = webdriver.Chrome(executable_path=path_to_driver, chrome_options=chrome_options)


    #TODO: need to figure out how to get the actual names of the files
    def scrape_documents_on_page(self, class_name='fa-file-pdf-o'):
        """returns links of all documents on page (default document type is pdfs, but can change to powerpoint by changing class_name to fa-file-powerpoint-o
        """
        job_list = self.driver.find_elements_by_class_name(class_name)
        for job in job_list:
            print(job.get_attribute('href'))
            # print(job.text)
    

    # def download_documents(self, links)




def main():
    my_scraper = Scraper()
    pdf_links = my_scraper.scrape_documents_on_page()
    print(pdf_links)

if __name__ == "__main__":
    main()