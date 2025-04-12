# job-hunt-tracker
trying to keep a record of my job applications

what it does:
    saves the links and details of each job application in an excel file

running instructions:
    1. install requirements.txt
    2. hopefully you have Ollama installed locally, if not go here: https://ollama.ai/
    3. update the model value in ai.py based on whatever you have locally & start ollama
    4. create an empty tracker.xlsx file
    5. start backend server with uvicorn api:app --reload
    6. open index.html with a browser and paste job links into input box, then press enter to submit
