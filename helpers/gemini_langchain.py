from app.shortcodes.model import *
from app.whatsapp_number.model import *
from pinecone.grpc import PineconeGRPC as Pinecone
import os

from langchain_pinecone import PineconeVectorStore

from langchain.chains import RetrievalQA  
from langchain.agents import initialize_agent
from langchain.agents.types import AgentType
from langchain.schema import HumanMessage, AIMessage
from langchain.tools import Tool

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from helpers.langchain import get_or_create_index

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))


def train_gemini_with_resource(resource_url, organization_shortcode):
    print(resource_url, organization_shortcode)
    try:
        index_name = get_or_create_index(organization_shortcode)
        loader = PyPDFLoader(resource_url)
        data = loader.load()

        if not data:
            raise ValueError("PDF loaded but no content found.")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        documents = text_splitter.split_documents(data)
        texts = [doc.page_content for doc in documents]

        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        PineconeVectorStore.from_texts(
            texts=texts,
            index_name=index_name,
            embedding=embeddings, 
            namespace=index_name
        )
    except Exception as e:
        raise Exception(f"Vector Store Error: {str(e)}")


def gemini_qa_chain(question, history=[], shortcode="", language=""):
    shortcode_obj = Shortcodes.get_user_by_shortcode(shortcode)
    whatsapp_number_obj = Whatsapp_Number.get_user_by_number(shortcode)
    if shortcode_obj:
        username = shortcode_obj.username
    elif whatsapp_number_obj:
        username = whatsapp_number_obj.username
    else: 
        username='company'
    get_or_create_index(shortcode)

    # Determine the maximum response length based on the shortcode length
    # max_response_length = 300 if len(shortcode) <= 5 else 3000
    max_response_length = 300 #TODO: Fix for whatsapp messaging

    # Initialize a LangChain object for chatting with the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.0,
        google_api_key=os.environ.get("GOOGLE_API_KEY")
    )

    # Initialize a LangChain embedding object.
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


    docsearch = PineconeVectorStore.from_existing_index(index_name=shortcode, embedding=embeddings, namespace=shortcode)

    # Initialize a LangChain object for chatting with the LLM
    # with knowledge from Pinecone. 
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever()
    )

    # Adjust the system message based on the maximum response length
    system_message = f"""
            "You are the point of contact in charge of user queries for {username}"
            "Make your responses as concise as possible and try your best to always answer according to the document."
            "Make sure your responses are less than {max_response_length} characters maximum"
            "Always make sure you respond in {language} language."
            "If the user's query is not in {language} language, respond in the same language as the query."
            """
    tools = [
        Tool(
            name=f"{username} help desk agent",
            func=qa.run,
            description=f"Useful when you need to answer {username} questions",
        )
    ]
    executor = initialize_agent(
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        tools=tools,
        llm=llm,
        # memory=chat_history,
        handle_parsing_errors="Check your output and make sure it conforms!",
        agent_kwargs={"system_message": system_message},
        verbose=True,
    )

    q = {"question": question}

    chat_history = []
    for h in history:
        chat_history.append(HumanMessage(content=h.question))
        chat_history.append(AIMessage(content=h.answer))

    return executor.run(input=q, chat_history=chat_history)
