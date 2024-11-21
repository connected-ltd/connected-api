from app.user.model import User
from app.shortcodes.model import *
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os

from langchain_pinecone import PineconeEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import MarkdownHeaderTextSplitter
import time

from langchain.chains import RetrievalQA  
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents.types import AgentType
from langchain.schema import HumanMessage, AIMessage
from langchain.tools import Tool

from langchain_community.document_loaders import OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings

# organization_shortdoce = Shortcodes.get_by_user_id(User.id)
# print

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

def get_or_create_index(organization_shortcode):

  index_name = organization_shortcode

  if not pc.has_index(index_name):
      pc.create_index(
          name=index_name,
          dimension=1536, 
          metric="cosine", 
          spec=ServerlessSpec(
              cloud="aws", 
              region="us-east-1"
          ) 
      ) 
  return index_name



def train_with_resource(resource_url, organization_shortcode):
    index_name = get_or_create_index(organization_shortcode)

    # Load the PDF
    loader = OnlinePDFLoader(resource_url)
    data = loader.load()

    # Split the loaded document into chunks of text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(data)

    # Extract text content from the document chunks
    texts = [doc.page_content for doc in documents]

    # Initialize a LangChain embedding object using the OpenAI API key
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    # Embed each chunk and upsert the embeddings into the Pinecone index
    PineconeVectorStore.from_texts(
        texts=texts,  # Now this is a list of strings
        index_name=index_name,
        embedding=embeddings, 
        namespace=index_name
    )

def delete_resource(resource_url, organization_shortcode):
    loader = OnlinePDFLoader(resource_url)

    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)


    index = PineconeVectorStore.get_pinecone_index(organization_shortcode)
    for text in texts:
        index.delete(filter={'text':{"$eq": text.page_content}})

def qa_chain(question, history=[], shortcode="", language=""):
    username = Shortcodes.get_username_by_shortcode(shortcode)
    get_or_create_index(shortcode)
    # Initialize a LangChain object for chatting with the LLM
    # without knowledge from Pinecone.
    llm = ChatOpenAI(
        openai_api_key=os.environ.get('OPENAI_API_KEY'),
        model_name='gpt-4o-mini',
        temperature=0.0
    )

    # Initialize a LangChain embedding object.
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    docsearch = PineconeVectorStore.from_existing_index(index_name=shortcode, embedding=embeddings, namespace=shortcode)

    # Initialize a LangChain object for chatting with the LLM
    # with knowledge from Pinecone. 
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever()
    )

    system_message = f"""
            "You are the point of contact in charge of user queries for {username}"
            "Make your responses as concise as possible and try your best to always answer according to the document."
            "Make sure your responses are less than 300 characters maximum"
            "Make sure you respond in {language}"
            "Else, if user queries is not in {language}, Make sure your response is in the same language you were queried with"
            """
    tools = [
        Tool(
            name=f"{username} help desk agent",
            func=qa.run,
            description=f"Useful when you need to answer {username} questions",
        )
    ]
    executor = initialize_agent(
        agent = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        tools=tools,
        llm=llm,
        # memory=conversational_memory,
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

def qa_chain_x(query, history=[], partner: User = User()):
    # Initialize a LangChain object for chatting with the LLM
    # without knowledge from Pinecone.
    llm = ChatOpenAI(
        openai_api_key=os.environ.get('OPENAI_API_KEY'),
        model_name='gpt-4o-mini',
        temperature=0.0
    )

    # Initialize a LangChain embedding object.
    model_name = "multilingual-e5-large"  
    embeddings = PineconeEmbeddings(  
        model=model_name,  
        pinecone_api_key=os.environ.get("PINECONE_API_KEY")  
    )  

    docsearch = PineconeVectorStore.from_existing_index(index_name=partner.username, embedding=embeddings)

    # Initialize a LangChain object for chatting with the LLM
    # with knowledge from Pinecone. 
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever()
    )

    return qa.invoke(query).get("result")
