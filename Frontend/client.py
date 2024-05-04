import streamlit as st
import requests


SERVER_URL = "http://127.0.0.1:3000/ask"

# Streamlit header
st.header("Bot to answer questions about events from books")
question = st.text_input("Ask your question:")
book = st.radio(
    "Choose one of the books",
    key="visibility",
    options=["Anne Of Green Gables", "The Old Man And The Sea", "Adventures Of Tom Sawyer"],
)

def ask_user():
    if book and question:
        res = requests.post(
            "http://127.0.0.1:3000/ask",
            json={"book_name": book, "question": question}
        )

        error = res.json()["error"]
        answer = res.json()["answer"]

        if (error):
            st.write("No answer found, try to rephrase the question")
        else:
            st.write(answer)

if __name__ == '__main__':
    ask_user()