from flask import Flask, render_template, request
from run_localGPT import retrieval_qa_pipline

import os
print("Current Working Directory:", os.getcwd())

app = Flask(__name__)

# Initialize the RetrievalQA instance
qa_instance = None

# Endpoint to render the initial UI
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['user_input']

    # Ensure the global qa_instance is initialized
    global qa_instance
    if qa_instance is None:
        qa_instance = retrieval_qa_pipline(device_type="mps", use_history=False, promptTemplate_type="llama")

    # Get the answer from the QA instance
    res = qa_instance(user_input)
    answer, docs = res["result"], res["source_documents"]

    # Pass user input and response to the template
    return render_template('index.html', user_input=user_input, response=answer)

if __name__ == "__main__":
    app.run(debug=True)
