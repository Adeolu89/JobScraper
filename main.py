from jobscraper import JobScraper
import pandas as pd

# Initial URL
job_scraper = JobScraper("https://remote.co/remote-jobs/developer/")

all_job_data = []

while True:
    job_data, next_page_url = job_scraper.scrape_main_page()
    all_job_data.append(job_data)
    if not next_page_url:
        break
    job_scraper.base_url = next_page_url

result_df = pd.concat(all_job_data, ignore_index=True)

job_urls = result_df["Job Info"]

additional_info_df = job_scraper.scrape_individual_pages(job_urls)

listings_df = pd.concat([result_df, additional_info_df], axis=1)

output_file = "remote_jobs.xlsx"
listings_df.to_excel(output_file, index=False)

print(f"Job data saved to {output_file}")
print(listings_df.head(10))
