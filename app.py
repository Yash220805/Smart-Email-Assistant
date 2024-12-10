import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from transformers import pipeline
from dotenv import load_dotenv
import streamlit as st
from streamlit_lottie import st_lottie, st_lottie_spinner
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate

# Set the page configuration first
st.set_page_config(page_title="Smart Email Assistant", layout="wide")

# Load environment variables
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

# Initialize summarization and response generation models once and reuse
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")  # Smaller, faster model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-70b-8192")
output_parser = StrOutputParser()
prompt_template = """
You are a professional email assistant. Based on the email content provided below, generate a thoughtful and appropriate response.
You must generate the response immediately, without generating any other words that are not related to response generation.
Ensure that the generated response is precise and to the point without beating around the bush.

Email Content:
{email_content}

Response:
"""
chain = ChatPromptTemplate.from_template(prompt_template) | llm | output_parser

# Define the required Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh (Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def fetch_emails(service, max_results=10):
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    emails = []
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        headers = msg['payload']['headers']
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "No Subject")
        sender = next((header['value'] for header in headers if header['name'] == 'From'), "Unknown Sender")
        date = next((header['value'] for header in headers if header['name'] == 'Date'), "Unknown Date")
        emails.append((message['id'], subject, sender, date, msg['snippet']))
    return emails

def fetch_email_by_id(service, email_id):
    msg = service.users().messages().get(userId='me', id=email_id).execute()
    email_content = msg['snippet']
    headers = msg['payload']['headers']
    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "No Subject")
    sender = next(header['value'] for header in headers if header['name'] == 'From')
    return email_content, sender, subject

def summarize_email(email_content):
    summary = summarizer(
        email_content, 
        max_length=150, 
        min_length=10,   
        do_sample=False  
    )
    return summary[0]['summary_text']

def suggest_response(email_content):
    result = chain.invoke(input={"email_content": email_content})
    response_text = result.strip()
    return response_text

# Custom CSS
st.markdown("""
<style>
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
        padding: 10px;
    }
    .sidebar .sidebar-content .stTextInput input {
        border-radius: 10px;
        border: 1px solid #bbb;
    }
    .main .block-container {
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff;
    }
    .stButton>button {
        border-radius: 10px;
        padding: 10px;
        background-color: #007BFF;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)

# Streamlit app setup
st.sidebar.header("Emails")
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    st.session_state['service'] = service
    st.session_state['authenticated'] = True
else:
    service = st.session_state['service']

emails = fetch_emails(service)

# Sidebar for email navigation and search functionality
with st.sidebar:
    search_term = st.text_input("Search Emails")
    filtered_emails = [email for email in emails if search_term.lower() in email[1].lower()]

    for i, (email_id, subject, sender, date, snippet) in enumerate(filtered_emails):
        button = st.button(f"{i+1}. {subject[:30]}... - {sender}", key=email_id)
        if button or ('selected_email_id' in st.session_state and st.session_state['selected_email_id'] == email_id):
            st.session_state.selected_email_id = email_id
            st.session_state.last_selected_email_id = email_id
            st.session_state['highlighted_email'] = email_id  # Add a state to track highlighted email

selected_email_id = st.session_state.get('selected_email_id')
highlighted_email = st.session_state.get('highlighted_email')
if selected_email_id:
    email_content, sender_email, subject = fetch_email_by_id(service, selected_email_id)

    st.title("📧 Smart Email Assistant")
    st.write("This app allows you to view, summarize, and generate responses for your Gmail emails.")
    
    st.markdown("---")
    st.write(f"**Email from {sender_email}:**")
    st.write(email_content)
    
    st.markdown("---")
    if st.button("📄 Summarize"):
        st.write("**Summary:**")
        st.write(summarize_email(email_content))

    if st.button("✍️ Generate Response"):
        st.write("**Suggested Response:**")
        response_text = suggest_response(email_content)
        st.text_area("Edit your response before sending:", value=response_text, height=200, key="editable_response")
    
    # Keep the highlight on the selected email
    st.session_state.selected_email_id = highlighted_email  # Maintain the highlighted email
