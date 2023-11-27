"""
This file implements prompt template for llama based models. 
Modify the prompt template based on the model you select. 
This seems to have significant impact on the output of the LLM.
"""

from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from smart_default import get_system_prompt

from datetime import datetime

# Get today's date in the format you want
today_date = datetime.now().strftime("%B %d, %Y")


# Include today's date in the system prompt


def get_prompt_template(promptTemplate_type=None, history=True):
    system_prompt = get_system_prompt()
    print(system_prompt)
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
