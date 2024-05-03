import os

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import Tool, StructuredTool
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from tools.tools import get_books_pdf_paths
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import pathlib
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

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
res = agent_executor.invoke({"input": "What is the path to pdf of a book called Adventures of Tom Sawyer? Only answear with path"})
book_path = res['output']
# print(book_path)


def embed_a_book(book_path: str) -> str:
    # Returns path to the book index
    loader = PyPDFLoader(book_path)
    text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    pages = loader.load_and_split(text_splitter=text_splitter)

    indexes_path = str(pathlib.Path().resolve()).replace("\\", "/") + "/indexes"
    available_indexes = [index for index in os.listdir(indexes_path)]
    searched_path = book_path.split("/")[-1] + "_index"

    if searched_path not in available_indexes:
        embeddings = OpenAIEmbeddings()
        db = FAISS.from_documents(pages, embeddings)
        db.save_local(indexes_path + "/" + searched_path)

    return indexes_path + "/" + searched_path


print(embed_a_book(book_path))