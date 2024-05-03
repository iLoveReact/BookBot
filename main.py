from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import Tool, StructuredTool
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from tools.tools import get_books_pdf_paths
from utils import embed_a_book
from langchain_core.prompts import PromptTemplate
from output_parsers.parser import parser, Answer
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)


def answer_question_about_book(book_name: str, question: str) -> Answer:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    tools = [
        StructuredTool.from_function(
            func=get_books_pdf_paths,
            description="Provides all book paths. Can be used to retrieve a path of specific book",
            name="get book pdf paths",
        )
    ]
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, prompt=prompt, tools=tools)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    res = agent_executor.invoke(
        {
            "input": "What is the path to pdf of a book called" + book_name + "? Only answer with path"
        }
    )
    book_path = res["output"]

    embeddings = OpenAIEmbeddings()
    index_path = embed_a_book(book_path)
    db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    embedding_vector = embeddings.embed_query(question)
    matched_docs = db.similarity_search_by_vector(embedding_vector)

    vectorestore = FAISS.from_documents(matched_docs, embeddings)
    retriever = vectorestore.as_retriever()
    rag_prompt = PromptTemplate.from_template(
        template="""
        You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use four sentences maximum and keep the answer concise.
        
        Question: {question} 
        
        Context: {context} 
        
        Answer:
        
        \n{format_instructions}
    """,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | rag_prompt
            | llm
            | parser
    )
    result = rag_chain.invoke(question)

    return result


# answer_question_about_book("Adventures of Tom Sawyer", "How did Tom Sawyer trick other kids to also paint the fence?")


@app.route("/ask", methods=["POST"])
def ask():
    book_name = request.json.get("book_name")
    question = request.json.get("question")

    res = answer_question_about_book(book_name, question)
    answer = res.answer
    error = res.error

    return jsonify(
        {
            "error": error,
            "answer": answer
        }
    )


if __name__ == '__main__':
    app.run(port=3000)
