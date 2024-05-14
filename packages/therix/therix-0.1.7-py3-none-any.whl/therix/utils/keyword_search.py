from langchain.prompts.chat import ChatPromptTemplate
from langchain_community.vectorstores.pgvector import PGVector
from therix.utils.rag import get_vectorstore
from langfuse.callback import CallbackHandler

DEFAULT_PROMPT = """
        You are a skilled professional who understands All kinds of documents. 
        You will be provided with Content and keywords.
        You have Analyze given data.
        {{content}}
        {{keywords}}
        Response should be in valid JSON format.

"""

BASIC_INSTRUCTIONS = """
If a question seems confusing, simply rephrase it using simpler words. Examples can help too.
When unsure of the user's intent, rephrase the question and ask for confirmation.
Only answer questions related to your knowledge base.
Avoid asking the user questions unrelated to their current request.
Strive for factual answers. If unsure, acknowledge it and offer to find more information.
Always be polite and inclusive in your communication.
Be open to improvement based on user interactions and feedback.
"""


class KeywordSearchService:
    def __init__(self,llmProvider,embed_model):
        self.llmProvider=llmProvider
        self.embed_model=embed_model

    def keyword_search(self, keyword_search_dict):
        chain_callbacks = []
         
        if keyword_search_dict.get("trace_details") is not None:
            langfuse_handler = CallbackHandler(
            secret_key=keyword_search_dict.get("trace_details")["secret_key"],
            public_key=keyword_search_dict.get("trace_details")["public_key"],
            host=keyword_search_dict.get("trace_details")["host"],
            trace_name=keyword_search_dict.get("trace_details")["identifier"],
        )
        chain_callbacks.append(langfuse_handler)

        store = get_vectorstore(self.embed_model , str(keyword_search_dict.get("pipeline_id")))

        if(type(keyword_search_dict.get("config_id")) is list):
            retriever=store.as_retriever(
            search_kwargs={"filter": {'configId': {'$in': keyword_search_dict.get('config_id')}}},
            )
        
        else:
            retriever=store.as_retriever(
            search_kwargs={"filter": {'configId': keyword_search_dict.get('config_id')}},
            )
        
        content = ""  
        for keyword in keyword_search_dict["keywords"]:
            results = retriever.get_relevant_documents(keyword)
    
            for res in results:
                content += res.page_content + "\n\n---\n\n" 

        content = content.rstrip("\n\n---\n\n")
        prompt = keyword_search_dict["prompt"]

        if not prompt:
            prompt = DEFAULT_PROMPT.format(content, keyword_search_dict["keywords"])

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                ("human",
                 "{BASIC_INSTRUCTIONS} {content} {keywords}")
            ]
        )

        chain = prompt | self.llmProvider | keyword_search_dict["output_parser"]

        response_text = chain.invoke({"content": content, "keywords": keyword_search_dict["keywords"], "format_instructions": keyword_search_dict["output_parser"].get_format_instructions(), "BASIC_INSTRUCTIONS": BASIC_INSTRUCTIONS}, config={"callbacks": [langfuse_handler]})
        return response_text
    
    