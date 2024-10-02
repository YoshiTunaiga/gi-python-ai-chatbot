import os
import openai
from dotenv import load_dotenv
from colorama import Fore
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import (
    CharacterTextSplitter,
)
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.vectorstores import Chroma



load_dotenv()
client = openai.OpenAI()

# Constants
MODEL_ENGINE = "gpt-3.5-turbo"
# Set the message system
PERSONA = "You are a Senior developer with a passion for teaching code and AI who is always eager to help others learn."
MESSAGE_SYSTEM = "A Senior developer with a passion for teaching code and AI."
messages = [{"role": "system", "content": MESSAGE_SYSTEM}]

# Function that moderates user input based on the content
def moderate(user_input):
    response = client.moderations.create(input=user_input)
    return response.results[0].flagged

# Function that generates chat completion
def generate_chat_completion(user_input, messages):
    flagged = moderate(user_input)
    # print(f"Flagged: {flagged}")
    if flagged:
        return ":red[Your comment has been flagged as inappropriate.]"
    completion = client.chat.completions.create(
        model=MODEL_ENGINE,
        messages=messages,
        temperature=1,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    return completion.choices[0].message.content

# ===================== LANGCHAING MODEL ============================================
LANGUAGE_MODEL = "gpt-3.5-turbo-instruct"

template: str = """/
    You are a customer support specialist /
    question: {question}. You assist users with general inquiries based on {context} /
    and  technical issues. /
    """
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_message_prompt = HumanMessagePromptTemplate.from_template(
    input_variables=["question", "context"],
    template="{question}",
)
chat_prompt_template = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

model = ChatOpenAI()

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


def load_documents():
    """Load a file from path, split it into chunks, embed each chunk and load it into the vector store."""
    raw_documents = TextLoader("./docs/faq_abc.txt").load()
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    return text_splitter.split_documents(raw_documents)


def load_embeddings(documents, user_query):
    """Create a vector store from a set of documents."""
    db = Chroma.from_documents(documents, OpenAIEmbeddings())
    docs = db.similarity_search(user_query)
    print(docs)
    return db.as_retriever()


def generate_response(retriever, query):
    pass
    # Create a prompt template using a template from the config module and input variables
    # representing the context and question.
    # create the prompt

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | chat_prompt_template
        | model
        | StrOutputParser()
    )
    return chain.invoke(query)


def query(query):
    documents = load_documents()
    retriever = load_embeddings(documents, query)
    response = generate_response(retriever, query)
    return response
# ========================================================
