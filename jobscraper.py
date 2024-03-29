import requests
from bs4 import BeautifulSoup
import pandas as pd


class JobScraper:
    """A class to scrape job listings from a remote job website."""

    def __init__(self, base_url):
        self.base_url = base_url
        self.parsed_content = None
    
    """
    Initialize the JobScraper object.

    Parameters:
    - base_url (str): The base URL of the remote job website. """
    

    def scrape_main_page(self):
    
        """
        Scrape the main page of the job website for job listings.

        Returns:
        - job_listing_df (DataFrame): DataFrame containing job listings.
        - next_page_url (str): URL of the next page of job listings, if available.
        """
        page = requests.get(self.base_url)
        self.parsed_content = BeautifulSoup(page.content, "html.parser")        
        results = self.parsed_content.find("div", class_="card bg-white m-0") # Finds card containing all jobs
        job_elements = results.find_all("div", class_="col position-static") # Finds individual jobs
        links = results.find_all("a", class_="card") # Finds job links to find more

        job_data = [] # List contianing title of job and company
        job_links = [] # List containing job links

        for job in job_elements:
            job_title = job.find("span", class_="font-weight-bold larger").text.strip() # Finds job title
            job_company = job.find("p", class_="m-0 text-secondary").text.strip().split("|")[0].strip() # Finds job company

            if job_title is not None and job_company is not None:
                job_data.append({
                    "Title": job_title,
                    "Company": job_company
                }) # Appends a dictionary of the Job title and company

        for job in links:
            job_link = job.get("href") # Extract job links
            if job_link is not None:
                job_link = f"https://remote.co{job_link}" # Corrects job link so it can lead to appropriate web page
                job_links.append({"Job Info": job_link}) # Appends a dictionary of the job link
            
        title_and_company_df = pd.DataFrame(job_data) # Creates A DataFrame of the job title and company
        info_df = pd.DataFrame(job_links) # Creates A DataFrame of the job links/info
        info_df = info_df.reset_index(drop=True)
        job_listing_df = pd.concat([title_and_company_df, info_df], axis=1) # Joins the 2 DataFrames together
        
        # Find the link to the next page
        next_page_link = self.parsed_content.find("a", class_="next page-numbers") # finds the link to the next page if there's any
        next_page_url = None
        if next_page_link is not None:
            next_page_url = next_page_link.get("href") # retrieves the value of the "href" attribute which is where the main URL is stored

        return job_listing_df, next_page_url
    
    def scrape_individual_pages(self, links):
        """
        Scrapes the data from individual pages of job listings.

        Parameters:
        - links (list): List of URLs of individual job listings.

        Returns:
        - location_and_salary_df (DataFrame): DataFrame containing location and salary of jobs.
        """
        job_data = [] # List containing salary of job and location
        
        for url in links:
            page = requests.get(url) #
            soup = BeautifulSoup(page.content, "html.parser")
            job_info = soup.find("div", class_="job_info_container_sm")
            
            location_text = job_info.find_all("div", class_="location_sm row")
            for x in location_text:
                location_str = x.find("div", class_="col-10 col-sm-11 pl-1").text.split(':', 1)[-1].strip()
            
            salary_text = job_info.find_all("div", class_="salary_sm row")
            for x in salary_text:
                salary_str = x.find("div", class_="col-10 col-sm-11 pl-1").text.split(':', 1)[-1].strip()
                
                if len(salary_str.split()) > 1 and "Annually" == salary_str.split()[1]:
                    salary_str = salary_str.split()[0]
            
            job_data.append({"Location": location_str,
                             "Annual Salary": salary_str})
            
        location_and_salary_df = pd.DataFrame(job_data)
            
        return location_and_salary_df