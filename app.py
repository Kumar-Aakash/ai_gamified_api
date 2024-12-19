import openai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def write_to_google_sheets(data, sheet_id, range_name="Sheet1!A1"):
    creds = Credentials.from_service_account_file(
        "./etc/secrets/vast-box-445114-r5-04253bd8e90f.json", scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    body = {"values": data}
    result = sheet.values().append(
        spreadsheetId=sheet_id,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()

    return result


class IndustrySelection(BaseModel):
    industry: str


class Answer(BaseModel):
    question: str
    answer: str


class ReportRequest(BaseModel):
    industry: str
    answers: List[Answer]


def generate_questions(context):
    """
    Function to generate all questions and options based on the selected industry.
    """
    additional_context = (
        "We want to add an AI feature to our site that will ask questions to clients who visit the website. The AI page will first ask what industry they belong to, and after getting that information, it will frame 4-5 questions for the client. These questions will gather information about their business, such as company size and goals, to create an AI report that predicts future trends for their business. The report will detail how AI can be a game changer in their business and help them grow, including some stats and feature-centric insights. While curating these questions, keep in mind that the client may not be in tech, so the questions should be crafted just for the purpose of understanding their business. Once you have answers to all these questions, you will generate a report. Don't ask technology-specific questions to the client.",
        "The questions that you generate should be specific. The client does not have any idea about how AI works or anything, so the questions should be very simple, easy to understand, and very specific to the industry and the business. What you are doing here is basically trying to understand their business. The client has no idea about AI, so don't include AI stuff in the questions you generate. Don't include any technical questions. Don't ask clients about how they think technology or AI is impacting or will impact their businesses; that is for you to figure out. Also note that TechTose is an IT service provider, the one who will be providing AI services to the clients and will help them. We are not the client. Clients will be different companies and can be anyone.",
        "The final report should be a very detailed one, at least 2000 words. The report should predict future trends for their business based on the information gathered, and how they can integrate the latest AI and ML in various parts of their business like marketing. Make it different for every business but put up a very detailed plan. Make the report not only about the data gathered but in general, I want the report to be very strategic in the sense it should also show clients how AI is going to impact their business in the future and what the play here is in the long run. Think of yourself like Gavin Belson and make a pitch like he makes in the AI report. Don't just mention AI but also ML and don't use AI as a word too much in your report. Also, make it more strategic. The report should have a strategic view about that industry.",
        "Encourage the client to schedule a consultation to discuss how our AI solutions can help them prepare for the future."
                "\nAt the end, output the questions and options strictly in the following JSON format:\n\n"
        "{\n"
        "    \"industry\": \"<industry>\",\n"
        "    \"questions\": [\n"
        "        {\n"
        "            \"question\": \"<question 1>\",\n"
        "            \"options\": [\"option1\", \"option2\", ...]\n"
        "        },\n"
        "        {\n"
        "            \"question\": \"<question 2>\",\n"
        "            \"options\": [\"option1\", \"option2\", ...]\n"
        "        }\n"
        "    ]\n"
        "}\n\n"
        "No extra text outside of this JSON. No bullet points, no numbering in the question text. Just a direct, clean JSON as shown above."
    )
    prompt = f"{additional_context}\nGenerate a list of 4-5 specific questions, with options for a business in the {context['industry']} sector. In the options you generate please don't generate option like 'Others' or 'Please Specify (others)' options like that cause i will be hardcoding these options in the frontend."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=900,
        temperature=0.7
    )
    questions_text = response.choices[0].message['content'].strip()
    return questions_text


def get_ai_response(report_prompt):
    """
    Generate the final report based on the collected answers.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": report_prompt}
        ],
        max_tokens=4096,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()


@app.post("/start-session")
async def start_session(industry_data: IndustrySelection):
    industry = industry_data.industry
    context = {"industry": industry}
    questions_json_str = generate_questions(context)

    # Parse the returned JSON directly
    import json
    try:
        data = json.loads(questions_json_str)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse the questions JSON from the model.")

    return data


def clean_question(question_text):
    """
    Clean up the question formatting by removing unnecessary quotes and ensuring consistency.
    """
    question_text = question_text.strip()
    if question_text.startswith('\"') and question_text.endswith('\"'):
        question_text = question_text[1:-1]
    return question_text


def extract_embedded_options(question_text):
    """
    Extract options embedded within the question text.
    """
    import re
    option_pattern = r"(?:[a-z]\))\s*[^a-z]*[^a-z]*(?=\s[a-z]\)|$)"
    matches = re.findall(option_pattern, question_text)
    return [match.strip() for match in matches]


@app.post("/generate-report")
async def generate_report(report_request: ReportRequest):
    """
    Generate the final AI report based on the provided industry and answers.
    Save the details to a Google Sheet.
    """
    industry = report_request.industry
    answers = report_request.answers

    report_prompt = f"Generate a visionary and strategic AI impact report for a business in the {industry} sector based on the following details:"
    for idx, answer in enumerate(answers, start=1):
        report_prompt += f"\nQuestion {idx}: {answer.question}\nAnswer: {answer.answer}"
    report_prompt += "\nProvide insights on how AI can be used to address these specifics in a transformative way, and suggest how TechTose can help implement these solutions. Encourage the client to schedule a consultation to discuss how our AI solutions can help them prepare for the future."

    report = get_ai_response(report_prompt)

    customer_data = [
        [industry, answer.question, answer.answer] for answer in answers
    ]
    customer_data.append(["Generated Report", report])

    SHEET_ID = "1CEXWRxk21ZEMiOk161nVoayimWtduYXfnIbVot_bzQo"
    RANGE_NAME = "Sheet1!A1"

    try:
        write_to_google_sheets(customer_data, SHEET_ID, RANGE_NAME)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write to Google Sheets: {str(e)}")

    return {"report": report}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
