import openai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os

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
        "The final report should be a very detailed one, at least 2000 words. The report should predict future trends for their business based on the information gathered, and how they can integrate the latest AI and ML in various parts of their business like marketing. Make it different for every business but put up a very detailed plan. Make the report not only about the data gathered but in general, I want the report to be very strategic in the sense it should also show clients how AI is going to impact their business in the future and what the play here is in the long run. Think of yourself like Gavin Belson and make a pitch like he makes in the AI report. Don't just mention AI but also ML and don't use AI as a word too much in your report. Also, make it more strategic. The report should have a strategic view about that industry. The report shouldn't just mention these things based on the above info but a good generic report also. You know it should look like it was made by a very great visionary like Steve Jobs.",
        "Encourage the client to schedule a consultation to discuss how our AI solutions can help them prepare for the future."
    )
    prompt = f"{additional_context}\nGenerate a list of 4-5 specific questions, with options for a business in the {context['industry']} sector."

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
    """
    Start the session by selecting the industry and generating questions based on it.
    """
    industry = industry_data.industry
    context = {"industry": industry}
    questions_text = generate_questions(context)

    questions = []
    current_question = ""
    current_options = []
    lines = questions_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line[0].isdigit() and '.' in line:
            if current_question:
                questions.append({'question': current_question, 'options': current_options})
                current_options = []
            current_question = line
        elif line.startswith('-'):
            current_options.append(line)
        else:
            if current_options:
                current_options[-1] += ' ' + line
            else:
                current_question += ' ' + line
    if current_question:
        questions.append({'question': current_question, 'options': current_options})
    
    return {"industry": industry, "questions": questions}

@app.post("/generate-report")
async def generate_report(report_request: ReportRequest):
    """
    Generate the final AI report based on the provided industry and answers.
    """
    industry = report_request.industry
    answers = report_request.answers

    report_prompt = f"Generate a visionary and strategic AI impact report for a business in the {industry} sector based on the following details:"
    for idx, answer in enumerate(answers, start=1):
        report_prompt += f"\nQuestion {idx}: {answer.question}\nAnswer: {answer.answer}"
    report_prompt += "\nProvide insights on how AI can be used to address these specifics in a transformative way, and suggest how TechTose can help implement these solutions. Encourage the client to schedule a consultation to discuss how our AI solutions can help them prepare for the future."

    report = get_ai_response(report_prompt)
    return {"report": report}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)