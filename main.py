from jobscraper import JobScraper
import pandas as pd

# Initial URL
url = JobScraper("https://remote.co/remote-jobs/developer/")

all_job_data = []
job_data, next_page_url = url.scrape_main_page()
all_job_data.append(job_data)

while True:
    job_data, next_page_url = url.scrape_main_page()
    all_job_data.append(job_data)
    if not next_page_url:
        break
    url.base_url = next_page_url

result_df = pd.concat(all_job_data, ignore_index=True)

output_file = "remote_jobs.xlsx"
result_df.to_excel(output_file, index=False)

print(f"Job data saved to {output_file}")
print(result_df.head(10))
