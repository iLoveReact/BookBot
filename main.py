from dotenv import load_dotenv
from langchain_core.tools import Tool, StructuredTool
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from tools.tools import get_books_pdf_paths

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

tools = [StructuredTool.from_function(
    func=get_books_pdf_paths,
    description="Provides all book paths. Can be used to retrieve a path of specific book",
    name="get book pdf paths"
)]
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm=llm, prompt=prompt, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools)
book_path = agent_executor.invoke({"input": "What is the path to pdf of a book called Old Man And The Sea?"})
print(book_path)

