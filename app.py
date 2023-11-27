from flask import Flask, render_template, request
from run_localGPT import retrieval_qa_pipline
import os
import utils
from constants import MODELS_PATH

import os
print("Current Working Directory:", os.getcwd())
MODELS_PATH = "models"


if not os.path.exists(MODELS_PATH):
    os.mkdir(MODELS_PATH)

app = Flask(__name__)


# Initialize an empty list to store query history
query_history = []
query_history1 = []

# Endpoint to render the initial UI
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    global qa_instance
    use_history = True
    

    user_input = request.form.get('user_input', '')

    greetings = ["hi", "hello", "hey", "greetings", "morning", "afternoon", "evening"]
    if any(greeting == user_input.lower() for greeting in greetings):
        response = "Hello! I am AthenaGuard, I am here to assist you with issues related to financial scams. How may I help you today?"
        query_history.append({'user_input': user_input, 'response': response})
        
    else:
        qa_instance = retrieval_qa_pipline(device_type="mps", use_history = True ,promptTemplate_type="llama")
      
        res = qa_instance(user_input)
        answer, docs = res["result"], res["source_documents"]
        query_history.append({'user_input': user_input, 'response': answer})
        response = answer

    print(response)  # Print the response to the Flask console for debugging purposes
    return render_template('index.html', user_input=user_input, response=response, query_history=query_history)

@app.route('/faq')
def faq():
    # You can add any additional logic here if needed
    return render_template('FAQ.html')

@app.route('/submit_faq', methods=['POST'])
def submit_faq():


    user_input1 = request.form['user_input']

    # Ensure the global qa_instance is initialized
    #global qa_instance
    #if qa_instance is None:
        #qa_instance = retrieval_qa_pipline(device_type="mps", use_history=True, promptTemplate_type="llamaFAQ")
    qa_instance = retrieval_qa_pipline(device_type="mps", use_history = True, promptTemplate_type="llamaFAQ")
    while True:
        user_input1 = request.form['user_input']
    # Get the answer from the QA instance
        res = qa_instance(user_input1)
        answer1, docs1 = res["result"], res["source_documents"]
        query_history1.append({'user_input': user_input1, 'response': answer1}) 
    
        #if save_qa:
        #    utils.log_to_csv(user_input1, answer1)
        return render_template('FAQ.html', user_input=user_input1, response=answer, query_history=query_history1)


if __name__ == "__main__":
    app.run(debug=True)