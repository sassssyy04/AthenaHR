"""
This file implements prompt template for llama based models. 
Modify the prompt template based on the model you select. 
This seems to have significant impact on the output of the LLM.
"""

from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# this is specific to Llama-2.

system_prompt = """You are athenaGuard, a Q&A chat assistant. Your purpose is to promptly assist and address individuals affected by financial scams, enhancing their experience by providing immediate guidance, resources, and solutions to mitigate the impact of scam-related issues. Offer concise and accurate responses. If you can not answer a user question based on 
the provided context, inform the user. Do not present a information to the user if you don't think it is relevant. Ask for clarity to confirm the relevance of the context. Do not use any other information for answering user."""

def get_prompt_template(system_prompt=system_prompt, promptTemplate_type=None, history=True):
    if promptTemplate_type == "llama":
        B_INST, E_INST = "[INST]", "[/INST]"
        B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
        SYSTEM_PROMPT = B_SYS + system_prompt + E_SYS
        instruction = """
        Context: {history} \n {context}
        User: {question}"""

        prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
        prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
    elif promptTemplate_type == "mistral":
        B_INST, E_INST = "<s>[INST] ", " [/INST]"
        prompt_template = (
                B_INST
                + system_prompt
                + """
            Context: {history} \n {context}
            User: {question}"""
                + E_INST
        )
        prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)

    else:
        # change this based on the model you have selected.
        prompt_template = (
             system_prompt
            + """
    
            Context: {history} \n {context}
            User: {question}
            Answer:"""
            )
        prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
    
    memory = ConversationBufferMemory(input_key="question", memory_key="history")

    return (
        prompt,
        memory,
    )
