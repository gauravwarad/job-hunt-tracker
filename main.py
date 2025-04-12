import requests
from ai import get_job_details, Job
from openpyxl import Workbook, load_workbook
from datetime import date
# from readability import Document  
from lxml_html_clean import clean_html, Cleaner, word_break_html

from bs4 import BeautifulSoup

def extract_main_content(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Remove unwanted tags
    for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'noscript']):
        tag.decompose()

    # Try to get main or article section
    main = soup.find('main') or soup.find('article') or soup.body
    return main.get_text(separator="\n", strip=True) if main else soup.get_text()


def save_to_excel(job_details, link, raw_html):
    
    woorkbook = load_workbook('tracker.xlsx')
    worksheet = woorkbook.active

    row = [
        0,
        date.today().strftime("%d-%b-%Y"),
        job_details.company,
        job_details.position,
        link,
        "No",
        "Applied",
        "N/A",
        job_details.location,
        job_details.h1b,
        job_details.job_description,
        raw_html
    ]
    worksheet.append(row)
    woorkbook.save('tracker.xlsx')


def process_job_link(link, job_id, status_dict):
    try:
        html = requests.get(link).text
        cleaned = clean_html(html)
        main_text = extract_main_content(cleaned)
        job_details = get_job_details(main_text)
        save_to_excel(job_details, link, html)
        status_dict[job_id] = {
            "url": link,
            "status": "Done",
            "company": job_details.company,
            "position": job_details.position,
            "location": job_details.location,
            "h1b": job_details.h1b
        }

    except Exception as e:
        status_dict[job_id] = {
            "url": link,
            "status": f"Failed - {str(e)}"
        }
        print(f"Error: {e}")
