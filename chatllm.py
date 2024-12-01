from langchain_core.prompts import ChatPromptTemplate

from langchain_fireworks import ChatFireworks
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatFireworks(api_key=os.getenv("FIREWORKS_API_KEY"),model="accounts/fireworks/models/llama-v3p1-8b-instruct",temperature=0.7)

prompt = ChatPromptTemplate.from_messages(
    [
        ("human", """Generate a well strutcered Markdown based on this json data : \n {Content} .\n """),
        ("system", "don't add any additional explanations just return the markdown based only on the json data."),
    ]
)

Reporter = prompt | llm

def RunLLM(Response):
    return Reporter.invoke({"Content":Response})

