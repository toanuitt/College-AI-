import streamlit as st
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.llms import GooglePalm
from langchain.chains import RetrievalQA
from langchain import PromptTemplate
def home():
        
    # Set your Google Palm API key
    palm_api = "AIzaSyAWFYtQuHNIha4v2-vmDJPVopM-1exlMF0"

    # Initialize SentenceTransformer embeddings
    embeddings = SentenceTransformerEmbeddings(model_name="all-mpnet-base-v2")

    # Initialize Chroma for creating a database of chunks
    db = Chroma(persist_directory="./chroma_index_2", embedding_function=embeddings)

    # Set up Google Palm language model
    google_palm_llm = GooglePalm(google_api_key=palm_api)

    # Set up Streamlit app
    #st.title("College AI advisor")

    # User input
    user_input = st.text_input("Enter your context:")

    # User question

    # Button to trigger QA
    if st.button("Get Answer"):
        # Perform QA based on user input
        qa = RetrievalQA.from_chain_type(
            llm=google_palm_llm,
            chain_type="stuff",
            retriever=db.as_retriever(search_type="similarity", search_kwargs={"k": 8}),
            return_source_documents=True
        )
        
        # Set up question prompt
        question_template = """
        Utilize the provided context to respond to the question below.
        If you lack the information, kindly state that you don't know rather than providing speculative answers.
        Envision yourself advising a college student and communicate in a natural and friendly manner.

        Please use English exclusively; refrain from incorporating other languages.

        {context}
        Student Inquiry: {question}
        Advisor's Response:
        """
        QUESTION_PROMPT = PromptTemplate(
            template=question_template, input_variables=["question", "context"]
        )
        
        # Set up QA parameters
        qa.combine_documents_chain.llm_chain.prompt = QUESTION_PROMPT
        qa.combine_documents_chain.verbose = True
        qa.return_source_documents = True
        
        # Run QA
        result = qa({"query": user_input})
        
        # Display result
        st.write("Result:", result['result'])
