# uvacollab-scraper
This is a script to scrape resources from UVACollab sites.

## Usage
Make sure you have a version of Python 3 installed. Then, install the required dependencies using:
`pip install -r requirements.txt `

Then run the scraper.py file:
`python scraper.py`

The script will prompt you to enter the path of the directory where you want to download files to. Pass in a path to a nonexistent or empty directory (if the directory does not currently exist, the script will create it).

The script will then spawn a new Chrome window. Navigate to the resources page of the Collab site you want to scrape in this new window. Do not open up any new tabs in this window. Once you have have navigated to the resources page of the site you want to scrape, press any key and let the script run till termination.

View this video for an explanation of how the script works and a sample run: https://youtu.be/3vp0LaQL09Q
