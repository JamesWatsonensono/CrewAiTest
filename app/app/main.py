from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
from langchain.agents import Tool
from langchain.utilities import GoogleSerperAPIWrapper,WikipediaAPIWrapper
from langchain.tools import DuckDuckGoSearchRun
from crewai import Agent,Task,Crew,Process
import os

#os.environ["OPEN_API_KEY"] = "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"
os.environ['SERPAPI_API_KEY'] = '1DA46A1006EE4997ACC72EBE7D7B739E'

ollama_model = Ollama(
    model="Phi",
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)

duck_search_tool = DuckDuckGoSearchRun()
search = GoogleSerperAPIWrapper(serper_api_key = '1DA46A1006EE4997ACC72EBE7D7B739E')
wiki = WikipediaAPIWrapper()

serper_tool = Tool(
  name="Wiki Search",
  func=wiki.run,
  description="useful for when you need do research"
)


researcher = Agent(name='researcher',
                   role='research agent',
                   goal='to use the tool give to search for for the answer and pass this to the writer',
                   backstory='You are a researcher and will tirelessly search the internet or your knoiwledge for the answer to the question',
                   description='researcher agent',
                   verbose=True,
                   allow_delegation=False,
                   tools = [duck_search_tool],
                   llm=ollama_model)


writer = Agent(name='writer',
               role = 'writer AI',
               goal='Give the best answer to the question taking the results from the researcher',
               backstory='You are a writer and will use the information from the researcher to answer the question if the research doesnt fit the question you will ask the researcher to do more research ',
               description='writer agent',
               verbose=True,
               allow_delegation=True,
               llm=ollama_model)

question = "tell me cats"

task1 = Task(description='investigate the question: {question} ', agent=researcher)
task2 = Task(description='respond to the question: {question}  usings the information passed on by the researcher', agent=writer)



crew = Crew(
            agents = [researcher,writer],
            tasks=[task1,task2],
            verbose=2,
            process = Process.sequential)


results = crew.kickoff()
               
print("######################")
print(results)   


