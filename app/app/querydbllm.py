from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
from langchain.agents import Tool
from langchain.tools import tool
from crewai import Agent,Task,Crew,Process
import os
import sqlite3
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from sqlselectfunction import get_data,get_data_declaration

#os.environ["OPEN_API_KEY"] = "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"
os.environ['SERPAPI_API_KEY'] = '1DA46A1006EE4997ACC72EBE7D7B739E'


telephone = 1234567890



ollama_model = Ollama(
    model="mistral",
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)

search = GoogleSerperAPIWrapper(serper_api_key = '1DA46A1006EE4997ACC72EBE7D7B739E')

serper_tool = Tool(
  name="Intermediate Answer",
  func=search.run,
  description="useful for when you need to ask with search",
)

class DbTools():
    @tool("Get customer data from database")
    def get_data(query):
        """execute database query"""
        conn = sqlite3.connect('customer.db')
        cursor = conn.cursor()
        
        
        cursor.execute(query)
        
        rows = cursor.fetchall()
        
        # Assuming the customers table columns are: first_name, last_name, email, phone, notes
        customers_list = [{"first_name": row[0], "last_name": row[1], "email": row[2], "phone": row[3], "notes": row[4]} for row in rows]
        
        conn.close()
        
        return customers_list
    


researcher = Agent(name='researcher',
                   role='Data agent',
                   goal=f'pass this query to the tool getdata() :select * from customers where phone = {telephone}',
                   backstory='You are a database agent and are amazing at querying sql databases',
                   description='researcher agent',
                   verbose=True,
                   allow_delegation=False,
                   tools=[DbTools().get_data],
                   llm=ollama_model)


writer = Agent(name='writer',
               role = 'writer AI',
               goal='Give the best answer to the question taking the results from the researcher',
               backstory='You are a writer and will use the information from the researcher to answer the question and give an answer on how best to respond to the customer',
               description='writer agent',
               tools=[serper_tool],
               verbose=True,
               allow_delegation=True,
               llm=ollama_model)

question = "what is the name of the customer"

task1 = Task(description="""fetch all the data from the customer table""", agent=researcher)
task2 = Task(description="""summarise the notes from the database and what the customers is complaining and advise on how best to respond to the customer""", agent=writer)

crew = Crew(
            agents = [researcher,writer],
            tasks=[task1,task2],
            verbose=2,
            process = Process.sequential)


results = crew.kickoff()
               
print("######################")
print(results)   


