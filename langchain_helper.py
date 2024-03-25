# from secret_key import google_api_key
from db import connect_db
from langchain_google_genai import GoogleGenerativeAI
from fewshots import few_shots
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.vectorstores import Chroma
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.chains.sql_database.prompt import _mysql_prompt, PROMPT_SUFFIX
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
google_api_key = os.environ["GOOGLE_API_KEY"]


def few_shot_query_selector():
    db = connect_db()

    llm = GoogleGenerativeAI(
        model="models/text-bison-001", google_api_key=google_api_key, temperature=0.1
    )

    to_vectorize = [" ".join(example.values()) for example in few_shots]
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_stores = Chroma.from_texts(
        to_vectorize, embedding=embeddings, metadatas=few_shots
    )

    example_selector = SemanticSimilarityExampleSelector(vectorstore=vector_stores, k=2)
    example_prompt = PromptTemplate(
        input_variables=[
            "Question",
            "SQLQuery",
            "SQLResult",
            "Answer",
        ],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )

    few_shot_prompt = FewShotPromptTemplate(
        example_prompt=example_prompt,
        example_selector=example_selector,
        suffix=PROMPT_SUFFIX,
        prefix=_mysql_prompt,
        input_variables=["input", "table_info", "top_k"],  # for suffix and prefix
    )
    db_chain = SQLDatabaseChain.from_llm(
        llm=llm, db=db, verbose=True, prompt=few_shot_prompt
    )
    return db_chain, db.table_info


if __name__ == "__main__":
    db_chain, db_info = few_shot_query_selector()
    print(db_chain.run("How Many Blue T shirt left?"))
