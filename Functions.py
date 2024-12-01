from Tools import Get_Video_Details,Get_Web_Details,Save_to_chroma,Search_from_chroma
from The_State import State
from LLMs import Extractor,Generator
from colorama import Fore, Back, Style,init
from PIL import Image
import matplotlib.pyplot as plt
import io

init(autoreset=True)

def Create_RAG(state:State):
    print(Style.BRIGHT+Fore.YELLOW+"Create RAG ...")
    Youtube_handle = state["Youtube_Handle"]
    Documents = Get_Video_Details(Youtube_handle)
    Save_to_chroma(Documents)

def Web(state:State):
    print(Style.BRIGHT+Fore.YELLOW+"Web Search ...")
    Query = state["query"]
    Documents = Get_Web_Details(Query)
    Save_to_chroma(Documents)
    
def Get_Context(state:State):
    print(Style.BRIGHT+Fore.YELLOW+"Get Context ...")
    Query = state.get("query")
    return {"Content": Search_from_chroma(Query,5)}

def Extractor_function(state:State):
    print(Style.BRIGHT+Fore.GREEN+"Extractor Thinking...")
    Context = state["Content"]
    Info = state["Response"]
    input = {"Content":Context,"Extracted_infos":Info}
    Extractor_Response = Extractor.invoke(input)
    return {"Response":Extractor_Response.Response}

def Generator_function(state:State):
    print(Style.BRIGHT+Fore.GREEN+"Generator Thinking...")
    print(Style.BRIGHT+Fore.CYAN+"Iteration :",state["counter"])
    
    input = {"Informations":state["Response"],"Youtube_handle":state["Youtube_Handle"]}
    Generator_Response = Generator.invoke(input)
    if state["counter"] > 3:
        return {"query":Generator_Response.query,"Task_completed":"YES"}
    
    return {"query":Generator_Response.query,"Task_completed":Generator_Response.Done,"counter":state["counter"]+1}

def Condition(state:State):
    print(Style.BRIGHT+Fore.CYAN+"Condition ...")
    print("State : \n",state["Response"])
    Task_completed = state["Task_completed"]
    
    if "YES" in Task_completed.upper():
        return "END"
    else: 
        return "CONTINUE"
       
    

def Visualize(Graph):
    image_data = Graph.get_graph(xray=True).draw_png()
    image_buffer = io.BytesIO(image_data)
    img = Image.open(image_buffer)
    plt.imshow(img)
    plt.axis('off')  # Hide the axis
    plt.show()





















