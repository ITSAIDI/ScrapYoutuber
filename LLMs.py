from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_fireworks import ChatFireworks
from dotenv import load_dotenv
import os

load_dotenv()

class Extractor_Output(BaseModel):
    Response : str = Field(..., description="This is your Response in a form of a python dictionary")
class Gnerator_Output(BaseModel):
    query    : str = Field(..., description="This is the query to search in the Store of Informations")
    Done : str = Field(..., description="This is a boolean value indicating if all informations are found or not")
        
llm = ChatFireworks(api_key=os.getenv("FIREWOKS_API_KEY"),model="accounts/fireworks/models/mixtral-8x22b-instruct",temperature=0.7)

structured_llm_extractor = llm.with_structured_output(Extractor_Output)
structured_llm_generator = llm.with_structured_output(Gnerator_Output)

# Prompt
system_extractor = """You are an expert Youtubers scraper.\n
Given a banch of Informations(from the Web, Videos Transcriptions...), You have to extract main informations about a youtuber like (First and Last name, Main Topics, Email adresss, ...).\n
Steps To Perform Your Task :\n

     1. Observe The Informations we already have.\n {Extracted_infos}.
     2. Think in Outher keys we can add to what we have .\n
     3. Use The provided Context to extract informations associeted to this keys.\n
     
**Important Note** \n
- Your Response must be in a form of a python dictionary with keys like (First_Name,Last_Name,Topics,bio,Github,Discord,Email,linkden,Twetter of the youtuber,...).\n
"""

system_generator = """You are an expert at Gnerating search queries.\n
Steps To Perform Your First Task :\n

    1. Observe The extracted data by  your Team memeber (Extractor) \n
    2. Try to find what are the missing informations in this data.(like None or Not found)\n
    3. Generate a query to search in the Informations's Store, In order to find this missing informations.\n
    
**Important Note : ** - If The Extractor response is None ,Your String  Query should be like this : "Youtube Channel {Youtube_handle}".    

Your second Task is :\n

- Respond with "Yes" if all fields of the Extractor response are filled with correct informations.Outherwise respond with "No".\n
- The Extractor response fields are (First_Name,Last_Name,Topics,bio,Github,Discord,Email,linkden,Twetter of the youtuber,...).\n 
"""

prompt_extractor = ChatPromptTemplate.from_messages(
    [
        ("system", system_extractor),
        ("human", """Extract all informations about the youtuber.\n A help data here :\n {Content} .\n"""),
    ]
)

prompt_generator = ChatPromptTemplate.from_messages(
    [
        ("system", system_generator),
        ("human", """The data extracted by the Extractor is  :\n {Informations} """),
    ]
)

Extractor = prompt_extractor | structured_llm_extractor
Generator = prompt_generator | structured_llm_generator




