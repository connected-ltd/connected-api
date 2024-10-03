# from langchain.chat_models import ChatOpenAI
# from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
# from langchain.chains import LLMChain, ConversationalRetrievalChain
# from langchain.utilities.serpapi import SerpAPIWrapper
# from langchain.prompts import PromptTemplate
import os
import openai
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential
from helpers.weaviate import wv_client

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


# def get_prompt(lang, question):
#     prompts = {
#         'eng': [
#             f"""IF QUESTION '{question}' IS NOT IN ENGLISH, TRANSLATE IT TO THAT LANGUAGE AND RESPOND. IGNORE QUESTION '{question}' 
#             IF IT'S NOT RELATED TO THE DOCUMENT PROVIDED. RESPOND IN THE SAME LANGUAGE AS IN '{question}'""",
#         ],
#         'hau': [
#             f"""KA YI WATSAR DA TAMBAYA '{question}' IDAN KUMA IDAN TAMBAYAR BATA DA ALAKA DA TAKARDAR DA AKA BAYAR. 
#             KA AMSA DA YAREN DA YAKE CIKIN TAMBAYA '{question}'""",
#         ]
#     }
#     print(prompts)
#     return prompts[lang]





# def do_search(input, language="hau"):
#     model = 'gpt-3.5-turbo'
#     messages = [
#         {
#             "role": "system", "content": """You are a multilingual AI model named ConnectED.
#             Always identify yourself as ConnectED when asked. Provide accurate and 
#             concise responses within 290 characters based on the provided document.
#             Always respond in the same language as the prompt."""
#         }
#     ]



#     search = SerpAPIWrapper()
#     tools = [
#         Tool(
#             name="Search",
#             func=search.run,
#             description="useful for when you need to translate and answer questions that are not in {language}",
#         )
#     ]
    

#     prefix = f"{messages[0]['content']} Answer the following questions as best you can. You have access to the following tools:"
#     suffix = """When answering, you MUST speak in the following language: {language}.

#     Question: {input}
#     {agent_scratchpad}"""

#     prompt = ZeroShotAgent.create_prompt(
#         tools,
#         prefix=prefix,
#         suffix=suffix,
#         input_variables=["input", "language", "agent_scratchpad"],
#     )

#     llm_chain = LLMChain(llm=ChatOpenAI(model=model, max_tokens=60, temperature=0.3), prompt=prompt)
#     agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools)
#     agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

#     return agent_executor.run(input=input, language=language)





# def ask_question(vectorstore, llm, question, chat_history, lang='eng'):
#     system_instruction = get_prompt(lang, question)[0]
#     template = f"""
#         {system_instruction}
        
#         {get_prompt(lang, question)[0]}
#     """
#     condense_prompt = PromptTemplate.from_template(template)


#     qa = ConversationalRetrievalChain.from_llm(
#         llm,
#         vectorstore.as_retriever(),
#         condense_question_prompt=condense_prompt,
#     )
    
#     result = qa({"question": question, "chat_history": chat_history})
#     chat_history.append((question, result["answer"]))
#     return result["answer"]
# def ask_question(wv_class_name, message):
#     file_content = wv_client.collections.get(wv_class_name)
#     response = file_content.query.hybrid(query='content', limit=10)
#     for o in response.objects:
#         print(o.properties)
#         return o



def ask_question(wv_class_name, message, target_language):
    print(1)
    collection = wv_client.collections.get(wv_class_name)
    print(2)
    # print(collection)
    try:
        print(3)
        response = collection.query.hybrid(
            query=message,
            limit=5,
            # properties=["content", "filename"]
            # vector=
        )
        print(4)
        
        results = []
        for obj in response.objects:
            results.append({
                "content": obj.properties["content"],
                "filename": obj.properties["filename"]
            })
        print(5)
        if results:
            context = "\n".join([r["content"] for r in results])
            print("Context: ",context)
            
            answer = respond_to_prompt(context, message, target_language)
            
            return answer
        else:
            return respond_to_prompt("", "I couldn't find any relevant information to answer your question.", target_language)
    
    except Exception as e:
        print(f"Error querying Weaviate: {str(e)}")
        return respond_to_prompt("", "I encountered an error while trying to answer your question.", target_language)
    # finally:
        # wv_client.close()



@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def respond_to_prompt(context, question, target_language):
    try:
        system_prompt = f"""You are an AI assistant that answers questions based strictly on the provided context. 
        If the answer cannot be found in the context, say "I don't have enough information to answer that question."
        Do not use any external knowledge.
        
        Provide your answer in {target_language}."""

        user_prompt = f"""Context:
        {context}

        Question: {question}

        Please provide your answer in {target_language}."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.5,
        )

        answer = response.choices[0].message.content
        print(f"Generated answer in {target_language}: {answer}")
        return answer

    except Exception as e:
        print(f"Error generating answer with ChatGPT: {str(e)}")
        return f"I'm sorry, but I encountered an error while trying to generate an answer. Please try again later. (Error in {target_language})"


