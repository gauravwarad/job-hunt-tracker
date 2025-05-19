from pydantic import BaseModel
from ollama import chat, ChatResponse

# class Job(BaseModel):
#     date: str
#     company: str
#     position: str
#     link: str
#     referral: str = 'No'
#     status: str = 'Applied'
#     last_update: str = 'N/A'
#     location: str
#     h1b: str
#     job_description: str


class Job(BaseModel):
    company: str
    position: str
    location: str
    h1b: str
    job_description: str


def get_job_details(html):
    print(html)
    prompt = '''
    You are a job description extractor. Your task is to extract structured information from a job posting HTML.

    **Required fields**:
    1. Company Name
    2. Position
    3. Location
    4. H1B Sponsorship (Answer: "Yes", "No", or "Not mentioned")
    5. Complete Job Description

    **Instructions**:
    - Only extract from meaningful visible content (ignore headers, footers, navigation, ads, scripts, or metadata).
    - Do not guess or fabricate information. If something is not clearly mentioned, return "Not mentioned".
    - Preserve line breaks and formatting in the job description where possible.

    **Output Format**:
    Return a JSON object with the following keys:
    {
    "company": "...",
    "position": "...",
    "location": "...",
    "h1b": "...",
    "job_description": "..."
    }
    '''

    response = chat(
        messages=[
            {"role": "user", "content": prompt + html},
        ],
        # model="llama3.1:8b",
        model="deepseek-coder-v2:latest",
        format=Job.model_json_schema(),
    )

    result = Job.model_validate_json(response.message.content)
    print("Job details extracted successfully.\n")
    print(result)
    return result
