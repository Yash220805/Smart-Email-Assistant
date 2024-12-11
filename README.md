# Smart-Email-Assistant
-----------------------

Smart Email Assistant is a web application built using Streamlit that allows users to authenticate with Gmail, fetch and display recent emails, summarize email content, and generate thoughtful responses. The project leverages Google's Gmail API, Transformers for summarization, and LangChain for generating responses.






Features:
--------

Gmail Authentication: Securely authenticate with Gmail to access emails.


Fetch Emails: Retrieve and display the 10 most recent emails.


Summarize Emails: Summarize email content using a pre-trained summarization model.


Generate Responses: Generate professional responses to emails using LangChain.






Technologies Used:
-----------------

  Python


  Streamlit


  Google API


  Transformers (Hugging Face)


  LangChain


  dotenv


  Bootstrap (for enhanced UI)






Installation:
------------


   1) Clone the repository by using the git clone command and change directory to the project's root directory.


   2) Create and activate a virtual environment using python -m venv venv and source venv/bin/activate (On Windows use venv\Scripts\activate).


   3) Install the dependencies listed in requirements.txt using the
   4)     pip install -r requirements.txtcommand.


   5) Set up the environment variables by creating a .env file in the root directory of the project. Add your Groq API key to the .env file as GROQ_API_KEY=your_groq_api_key.


   6) Set up Google API credentials: 
      a. Go to the Google Cloud Console. 
      b. Create a new project and enable the Gmail API. 
      c. Create OAuth 2.0 credentials and download the credentials.jsonfile. 
      d. Place the credentials.jsonfile in the root directory of the project.




 Usage:
 -----

  Run the Streamlit application using the streamlit run app.py command


  Open your web browser and go to http://localhost:8501 to access the Smart Email Assistant.


  Authenticate with Gmail by following the prompts to log in to your Gmail account and grant the necessary permissions.


  
  
  View Emails:
  -----------


  The sidebar will display the 10 most recent emails.


  Click on an email to view its content.


  Summarize Emails:
  ----------------

  Click on the "📄 Summarize" button to generate a summary of the email content.


  The summary will be displayed below the email content.


  Generate Responses:
  ------------------

  Click on the "✍️ Generate Response" button to generate a professional response to the email.


  The suggested response will be displayed below the summary (if any) or the email content.


  You can edit the response before sending.




Contributing: Contributions are welcome! Please feel free to submit a Pull Request.






Home Page 
---------

![image](https://github.com/user-attachments/assets/b7050d09-e6f7-41b5-b173-67b8eaaa867d)




Email Content
-------------

![image](https://github.com/user-attachments/assets/9bd7e559-8c3c-4f1b-b52e-13cf90f0d90a)



summarization
-------------

![image](https://github.com/user-attachments/assets/72af6f9b-8700-4340-887b-556cce02e76d)



Response Generation
-------------------

![image](https://github.com/user-attachments/assets/f0983e85-ab9b-4e37-a7cb-b313137dc49c)





