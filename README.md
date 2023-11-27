
AthenaHR: HR Chatbot for Secure, Local Conversations with Your Documents 🌐
AthenaHR is an enhanced version of the open-source initiative LocalGPT, tailored for HR use within companies. It enables secure, local document interactions with advanced features to streamline HR-related queries. With a focus on privacy, AthenaHR ensures that all data remains on the company's servers, providing a confidential and efficient HR chatbot experience.

Enhanced Features 🚀
Smart Template Filtering: AthenaHR intelligently filters HR templates based on the context of the conversation, providing more relevant and targeted responses.
Soft Prompting: The chatbot prompts users with friendly suggestions to help guide the conversation and elicit clearer queries, improving user engagement.
Ensemble Retrieval: Utilizes FAISS, Bm25, and other ensemble methods to enhance document retrieval, ensuring comprehensive and accurate information retrieval.
Improved GUI: Upgrades to the graphical interface with a focus on user-friendly interactions, making it easier for HR personnel to navigate and use AthenaHR effectively.
Template Management: Allows HR administrators to manage and customize templates easily, ensuring that the chatbot provides accurate and up-to-date information.
Enhanced Security Measures: Implements additional security layers to safeguard sensitive HR data, providing a robust and trustworthy solution.
Credits and Acknowledgments 🙌
AthenaHR is built upon the foundation of the LocalGPT project created by PromtEngineer. The original project laid the groundwork for secure, local conversations with documents, and AthenaHR extends this vision to cater specifically to HR needs.

Original LocalGPT Features 🌟
Utmost Privacy: Your data remains on your company's servers, ensuring 100% security.
Versatile Model Support: Seamlessly integrates various open-source models, including HF, GPTQ, GGML, and GGUF.
Diverse Embeddings: Choose from a range of open-source embeddings.
Reuse Your LLM: Once downloaded, reuse your LLM without the need for repeated downloads.
Chat History: Remembers previous conversations within a session.
API: AthenaHR includes an API that can be used for building HR applications.
Graphical Interface: AthenaHR offers an improved GUI for HR personnel, enhancing user experience.
How to Use AthenaHR 🌍
Environment Setup 📥
📥 Clone the AthenaHR repo using git:

CLONE : 
git clone https://github.com/sassssyy04/AthenaHR
🐍 Install conda for virtual environment management. Create and activate a new virtual environment.

CREATE ENV : 
conda create -n athenaHR python=3.10.0
conda activate athenaHR
🛠️ Install the dependencies using pip:

INSTALL REQUIREMENTS :
pip install -r requirements.txt
Follow additional instructions in the LocalGPT readme for setting up LLAMA-CPP and Docker if needed.

Test AthenaHR with Sample Data 🧪
For testing, AthenaHR comes with sample HR documents. Follow the instructions in the LocalGPT readme to ingest and run queries with the sample dataset.

Ingest Your Own HR Data 📊
Put your HR files in the SOURCE_DOCUMENTS folder. You can organize multiple folders within SOURCE_DOCUMENTS, and AthenaHR will recursively read your files.

AthenaHR currently supports various HR-related file formats. Refer to the LocalGPT readme for a list of supported formats and instructions on adding support for additional formats.

Run the following command to ingest your HR data:

python ingest.py
Choose the appropriate device type, such as cpu or mps, based on your system.

Chat with AthenaHR Locally! 💬
Run the following command to interact with AthenaHR:

python run_localGPT.py
Specify the device type, such as cuda, cpu, or mps.

Enter your HR-related queries when prompted, and AthenaHR will generate responses based on the ingested HR documents.

Optionally, explore extra options with run_localGPT.py to show sources or enable chat history. Refer to the LocalGPT readme for more details.

Set the desired LLM models in constants.py for AthenaHR.

Acknowledgments and Disclaimer 📜
AthenaHR is a specialized HR chatbot project inspired by the original LocalGPT. It is not intended for production use and serves as a test project to explore the feasibility of a fully local solution for HR-related question answering. Credits to the original LocalGPT contributors for their innovative work.

Common Errors and Troubleshooting ❗
If you encounter common errors, refer to the LocalGPT readme for troubleshooting tips and solutions.

Feel free to explore, enhance, and tailor AthenaHR to meet your company's HR chatbot needs! 🌐
