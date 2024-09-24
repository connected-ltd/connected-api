from langchain.chat_models import ChatOpenAI
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.utilities.serpapi import SerpAPIWrapper
from langchain.prompts import PromptTemplate



def get_prompt(lang, question):
    prompts = {
        'eng': [
            f"""IF QUESTION '{question}' IS NOT IN ENGLISH, TRANSLATE IT TO THAT LANGUAGE AND RESPOND. IGNORE QUESTION '{question}' 
            IF IT'S NOT RELATED TO THE DOCUMENT PROVIDED. RESPOND IN THE SAME LANGUAGE AS IN '{question}'""",
        ],
        'hau': [
            f"""KA YI WATSAR DA TAMBAYA '{question}' IDAN KUMA IDAN TAMBAYAR BATA DA ALAKA DA TAKARDAR DA AKA BAYAR. 
            KA AMSA DA YAREN DA YAKE CIKIN TAMBAYA '{question}'""",
        ]
    }
    print(prompts)
    return prompts[lang]





def do_search(input, language="hau"):
    model = 'gpt-3.5-turbo'
    messages = [
        {
            "role": "system", "content": """You are a multilingual AI model named ConnectED.
            Always identify yourself as ConnectED when asked. Provide accurate and 
            concise responses within 290 characters based on the provided document.
            Always respond in the same language as the prompt."""
        }
    ]



    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to translate and answer questions that are not in {language}",
        )
    ]
    

    prefix = f"{messages[0]['content']} Answer the following questions as best you can. You have access to the following tools:"
    suffix = """When answering, you MUST speak in the following language: {language}.

    Question: {input}
    {agent_scratchpad}"""

    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input", "language", "agent_scratchpad"],
    )

    llm_chain = LLMChain(llm=ChatOpenAI(model=model, max_tokens=60, temperature=0.3), prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools)
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

    return agent_executor.run(input=input, language=language)





def ask_question(vectorstore, llm, question, chat_history, lang='eng'):
    system_instruction = get_prompt(lang, question)[0]
    template = f"""
        {system_instruction}
        
        {get_prompt(lang, question)[0]}
    """
    condense_prompt = PromptTemplate.from_template(template)


    qa = ConversationalRetrievalChain.from_llm(
        llm,
        vectorstore.as_retriever(),
        condense_question_prompt=condense_prompt,
    )
    
    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    return result["answer"]

