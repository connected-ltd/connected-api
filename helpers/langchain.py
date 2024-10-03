import os
from langchain.document_loaders import OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

import pinecone

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain.agents.types import AgentType
from langchain.schema import HumanMessage, AIMessage


from app.shortcodes.model import Shortcodes

def answer_question(question, history=[], language='english', shortcode: Shortcodes = Shortcodes()):
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    pinecone.init(
        api_key=os.getenv('PINECONE_API_KEY'),
        environment=os.getenv('PINECONE_API_ENV'),
    )

    docsearch = Pinecone.from_existing_index(index_name=shortcode.shortcode, embedding=embeddings)
    
    llm = ChatOpenAI()
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
    )

    system_message = f"""You are an AI assistant that answers questions based strictly on the provided context. 
        If the answer cannot be found in the context, say "I don't have enough information to answer that question."
        Do not use any external knowledge.
        
        Provide your answer in {language}."""
    tools = [
        Tool(
            name=f"Assistant",
            func=qa.run,
            description=f"Useful when you need to answer questions",
        ),
        # Tool(
        #     name=f"{partner.name} customer support",
        #     func=qa.run,
        #     description=f"Useful when you need to answer {partner.name} questions",
        # ),
    ]
    executor = initialize_agent(
        agent = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        tools=tools,
        llm=llm,
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

def pinecone_train_with_resource(resource_url, shortcode):
    loader = OnlinePDFLoader(resource_url)

    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)
    

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    pinecone.init(
        api_key=os.getenv('PINECONE_API_KEY'),
        environment=os.getenv('PINECONE_API_ENV'),
    )
    
    if shortcode not in pinecone.list_indexes():
        # we create a new index
        pinecone.create_index(
        name=shortcode,
        metric='cosine',
        dimension=1536
        )

    Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=shortcode)

def pinecone_delete_resource(resource_url, partner_identity):
    loader = OnlinePDFLoader(resource_url)

    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)

    pinecone.init(
        api_key=os.getenv('PINECONE_API_KEY'),
        environment=os.getenv('PINECONE_API_ENV'),
    )

    index = Pinecone.get_pinecone_index(partner_identity)
    for text in texts:
        index.delete(filter={'text':{"$eq": text.page_content}})