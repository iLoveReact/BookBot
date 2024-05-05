import streamlit as st
import requests



# Streamlit header
st.header("Bot to answer questions about events from books")
question = st.text_input("Ask your question:")
book = st.radio(
    "Choose one of the books",
    key="visibility",
    options=["Anne Of Green Gables", "The Old Man And The Sea", "Adventures Of Tom Sawyer"],
)

st.header("Example Questions: ")

st.write("Why Diana was drunk? (Anne of the green gables)")
st.write("How Tom Sawyer managed to convince other children to paint the fence? (Adventures of Tom Sawyer)")
st.write("For how long Santiago was unable to catch any fish? (Old man and the sea)")

def ask_user():
    if book and question:
        res = requests.post(
            "http://backend:3000/ask",
            json={"book_name": book, "question": question}
        )

        error = res.json()["error"]
        answer = res.json()["answer"]
        st.header("Answer:")
        if (error):
            st.write("No answer found, try to rephrase the question")
        else:
            st.write(answer)

if __name__ == '__main__':
    ask_user()