from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


from urllib.parse import unquote
import time
import os


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
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.ac = ActionChains(self.driver)
        self.num_files_to_download = 0

        if not os.path.exists(self.download_base_dir):
            os.makedirs(self.download_base_dir)


    def open_folders(self):
        """opens all folders (and subfolders) on screen"""
        job_list = self.driver.find_elements_by_class_name("fa-folder")
        opened = 0
        print("Opening all folders")
        while(len(job_list) > 0):
            job = job_list[0]
            time.sleep(1.5)
            try:
                job.click()
                opened += 1
            except:
                self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
            job_list = self.driver.find_elements_by_class_name("fa-folder")



    def start_download(self):
        """does the scraping"""
        job_list = []
        class_names = ['fa-file-pdf-o', 'fa-file-powerpoint-o', 'fa-file-word-o']

        for class_name in class_names:
            # job_list += self.driver.find_elements_by_class_name(class_name)
            job_list += self.driver.find_elements_by_class_name(class_name)
            # job_list += self.driver.find_elements(by=By.CLASS_NAME, value=class_name)
        i = 0
        while i < len(job_list):
            job = job_list[i]
            try:
                job.click()
                i += 1
            except:
                self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)



    def wait_for_download_to_complete(self, structure):
        downloaded_files = [f for f in os.listdir(self.download_base_dir) if f.endswith('.pdf') or f.endswith('.ppt') or f.endswith('.pptx') or f.endswith(".docx")]
        while len(downloaded_files) != self.num_files_to_download:
            print("downloaded files: ", len(downloaded_files))
            print("number of files needed: ", self.num_files_to_download)
            print("")
            time.sleep(1)
            downloaded_files = [f for f in os.listdir(self.download_base_dir) if f.endswith('.pdf') or f.endswith('.ppt') or f.endswith('.pptx') or f.endswith(".docx")]
        return


    def get_file_structure(self):
        """determines file/folder structure so we can can replicate that structure in the downloaded folders"""
        """returns sorted array containing info from wich file structure can be generated"""
        print("Determining folder structure...")
        job_list = []
        class_names = ['fa-file-pdf-o', 'fa-file-powerpoint-o', 'fa-file-word-o', 'fa-folder-open']
        for class_name in class_names:
            # job_list += self.driver.find_elements_by_class_name(class_name)
            job_list += self.driver.find_elements_by_class_name(class_name)


        job_list = sorted(job_list, key=lambda job: job.location['y'])
        # name_elements = self.driver.find_elements_by_class_name("resource-name")
        # name_elements = self.driver.find_elements(by=By.CLASS_NAME, value="resource-name")
        name_elements = self.driver.find_elements_by_class_name("resource-name")


        names, structure = [], []
        for elem in name_elements:
            names.append((elem.text, elem.location['y']))

        for job in job_list:
            for name, y in names:
                if job.location['y'] == y+3:
                    actual_name = name
                    if job.get_attribute("class") != 'nil fa fa-folder-open':   # if it's not a folder, get the actual name from the href
                        actual_name = unquote(job.get_attribute('href').split("/")[-1])
                    structure.append((job.get_attribute("class"), actual_name, job.location['x']))
                    break

        for elem in structure:
            print(elem)
            if elem[0] == 'fa fa-file-pdf-o' or elem[0]=='fa fa-file-powerpoint-o' or elem[0]=='fa fa-file-word-o':
                self.num_files_to_download += 1

        return structure


    def organize_files(self, structure):
        """reorganizes files once they are all downloaded into folder structure present on collab site"""
        structure = structure[1:]
        # curr_dir = self.download_base_dir
        stack = [(0, self.download_base_dir)]    # stack: [(x_pos, path)]
        # obj: (class_name, name, x_pos)
        for obj in structure:
            class_name, name, x_pos = obj[0], obj[1], obj[2]
            while stack[-1][0] >= x_pos:
                stack.pop()

            if class_name == 'nil fa fa-folder-open':   # it's a folder
                new_path = os.path.join(stack[-1][1], name)
                os.mkdir(new_path)
                stack.append((x_pos, new_path))

            else:   # it's a file, need to save to current directory
                # save file to current path
                curr_dir = os.path.join(self.download_base_dir, name)
                new_dir = os.path.join(stack[-1][1], name)
                os.replace(curr_dir, new_dir)


def main():
    BASE_DIR = input("Enter the path to an empty directory to which you want to download the files to: ")
    my_scraper = Scraper(BASE_DIR)

    done = input("enter something when you have navigated to the page")
    my_scraper.open_folders()
    structure = my_scraper.get_file_structure()
    my_scraper.start_download()
    print(structure)
    my_scraper.wait_for_download_to_complete(structure)
    my_scraper.organize_files(structure)


if __name__ == "__main__":
    main()
