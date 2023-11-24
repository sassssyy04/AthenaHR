import json
from langchain import OpenAI, PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
import logging
from langchain.chains import AnalyzeDocumentChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler  # for streaming response
from langchain.callbacks.manager import CallbackManager
from constants import (
    MODEL_ID,
    MODEL_BASENAME,
    MAX_NEW_TOKENS,
    MODELS_PATH,
)
from datetime import datetime
today_date = datetime.now().strftime("%B %d, %Y")
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

from langchain.vectorstores import Chroma
from transformers import (
    GenerationConfig,
    pipeline,
)
from load_models import (
    load_quantized_model_gguf_ggml,
    load_quantized_model_qptq,
    load_full_model,
)
def load_model(device_type, model_id, model_basename, LOGGING=logging):
    """
    Select a model for text generation using the HuggingFace library.
    If you are running this for the first time, it will download a model for you.
    subsequent runs will use the model from the disk.

    Args:
        device_type (str): Type of device to use, e.g., "cuda" for GPU or "cpu" for CPU.
        model_id (str): Identifier of the model to load from HuggingFace's model hub.
        model_basename (str, optional): Basename of the model if using quantized models.
            Defaults to None.

    Returns:
        HuggingFacePipeline: A pipeline object for text generation using the loaded model.

    Raises:
        ValueError: If an unsupported model or device type is provided.
    """
    logging.info(f"Loading Model: {model_id}, on: {device_type}")
    logging.info("This action can take a few minutes!")

    if model_basename is not None:
        if ".gguf" in model_basename.lower():
            llm = load_quantized_model_gguf_ggml(model_id, model_basename, device_type, LOGGING)
            return llm
        elif ".ggml" in model_basename.lower():
            model, tokenizer = load_quantized_model_gguf_ggml(model_id, model_basename, device_type, LOGGING)
        else:
            model, tokenizer = load_quantized_model_qptq(model_id, model_basename, device_type, LOGGING)
    else:
        model, tokenizer = load_full_model(model_id, model_basename, device_type, LOGGING)

    # Load configuration from the model to avoid warnings
    generation_config = GenerationConfig.from_pretrained(model_id)
    #https://huggingface.co/docs/transformers/main/main_classes/text_generation
    # see here for details:
    # https://huggingface.co/docs/transformers/
    # main_classes/text_generation#transformers.GenerationConfig.from_pretrained.returns

    # Create a pipeline for text generation
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=MAX_NEW_TOKENS,
        temperature=0.01,
        top_p=0.95,
        top_k=40,
        repetition_penalty=1.03,
        generation_config=generation_config,
    )

    local_llm = HuggingFacePipeline(pipeline=pipe)
    logging.info("Local LLM Loaded")

    return local_llm

llm = load_model(device_type='mps', model_id=MODEL_ID, model_basename=MODEL_BASENAME, LOGGING=logging)

file_path = "user_chat/User.txt"
# Function to categorize user based on chat history
def categorize_user(file_path):

    try:
        with open(file_path, 'r') as file:
            text_data = file.read()
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
  
    from langchain.chains.question_answering import load_qa_chain

    qa_chain = load_qa_chain(llm, chain_type="map_reduce")

    qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)
    prompt = """Analyse the given chat history between the user and the HR AI assistant chatbot. Categoriese the user into one of the following categories:
     1. Formal communicator
      2. Informal communicator
       3. Detailed communicator
         4. Guided interactor
          5. Varied feedback provider
           6. Autonomous decision maker
              Based on the categorisation only output the exact category to the user. If the user cannot be categorised into the given output categories, output the category as 'Cannot be categorised'.
               Example: 1) chat history analysis shows that the user is an Autonomous decision maker. Output: Autonomous decision maker
             2) chat history analysis shows that the user is an informal communicator. Output: Informal communicator"""
    response = qa_document_chain.run(input_document=text_data, question=prompt)
        # Extract and return the category from the model's response
    category = response
    return category


def set_system_prompt(category):
    # Define your default system prompt
    default_prompt = f"""You are athenaHR, an HR assistance chatbot designed for Quadwave employees. Your primary objective is to promptly aid and address inquiries related to human resources, enhancing the employee experience by providing immediate guidance, resources, and solutions to various HR-related issues. Deliver concise and accurate responses. If uncertain about the context of a user's question, seek clarification to confirm relevance. Refrain from presenting information if its applicability is in doubt. Your role is to assist Quadwave employees effectively and efficiently. Today is {today_date}."""

    # Map category to a custom prompt (add more categories as needed)
    category_to_prompt = {
        "Formal communicator": f"You are athenaHR, the HR assistant for Quadwave employees. Your user is a Formal Communicator who values professionalism in communication. Provide information in a formal and business-appropriate manner, maintaining a tone of respect and formality.Today is {today_date}",
        "Informal communicator": f"You are athenaHR, the friendly HR chatbot for Quadwave employees. Your user is an Informal Communicator who appreciates a more casual and conversational tone. Feel free to engage in friendly banter while delivering helpful HR information.Today is {today_date}",
        "Detailed communicator": f"You are athenaHR, an HR assistance chatbot designed for Quadwave employees. Your user prefers detailed and thorough information. Take the time to provide comprehensive responses, ensuring all aspects of the inquiry are covered. Prioritize depth and clarity in your explanations.Today is {today_date}",
        "Guided interactor": f"You are athenaHR, the HR assistant for Quadwave employees. Your user is a Guided Interactor who appreciates step-by-step guidance. Assist them by breaking down information into manageable steps. Offer structured support to help them navigate through HR processes effectively.Today is {today_date}",
        "Varied feedback provider": f"You are athenaHR, the HR assistant for Quadwave employees. Your user is a Varied Feedback Provider, offering different styles of feedback. Be receptive to both direct critiques and constructive suggestions. Adapt your responses to accommodate a range of feedback approaches.Today is {today_date}",
        "Autonomous decision maker": f"Your user is an Autonomous Decision Maker who prefers making decisions independently. Provide information that allows them to make confident decisions on their own. Offer guidance without overwhelming details.Today is {today_date}",
    }

    # Check if each category is present in the response
    for category_to_check in category_to_prompt.keys():
        if category_to_check.lower() in category.lower():
            return category_to_prompt[category_to_check]

    # If none of the categories are present, return the default prompt
    return default_prompt

def get_system_prompt():
    file_path="user_chat/User.txt"
    category = categorize_user(file_path)
    system_prompt = set_system_prompt(category)
    return system_prompt

def main(file_path):
    file_path = "user_chat/User.txt"
    category = categorize_user(file_path)
    print(category)
    system_prompt = set_system_prompt(category)
    print("System Prompt:")
    print(system_prompt)

if __name__ == "__main__":
    main(file_path=file_path)