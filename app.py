import warnings
warnings.filterwarnings('ignore')
from langchain.document_loaders.image import UnstructuredImageLoader
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
import tiktoken
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from filetype import guess
import base64
import streamlit as st
from PIL import Image

def save_uploadedfile(uploadedfile):
     with open(uploadedfile.name,"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success("Saved")

def get_file_type(file_path):
   file_type = ""
   image_type = ["png","jpg","jpeg","gif"]
   guess_file_type = guess(file_path)
   if(guess_file_type.extension.lower() == "pdf"):
     file_type = "pdf"
   elif(guess_file_type.extension.lower() in image_type):
     file_type = "image"
   else:
     file_type = "Unkown"
   return file_type

def get_file_content(file_path):
   file_type = get_file_type(file_path)
   if(file_type == "pdf"):
     loader=UnstructuredFileLoader(file_path)
   elif(file_type == "image"):
     loader = UnstructuredImageLoader(file_path)
   else:
      return null
   document = loader.load()
   document_content = '\n'.join(doc.page_content for doc in document)
   return document_content

text_splitter = CharacterTextSplitter(
    separator = "\n\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)
os.environ['OPENAI_API_KEY']= "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"
#"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" #previous key
embeddings = OpenAIEmbeddings()

def create_vector_index(text_chunks):
   return FAISS.from_texts(text_chunks, embeddings)
chain = load_qa_chain(OpenAI(),chain_type = "map_rerank",return_intermediate_steps=True)
def speak_with_file(file_path,query):
  file_content = get_file_content(file_path)
  file_splitter = text_splitter.split_text(file_content)
  doc_search = create_vector_index(file_splitter)
  documents = doc_search.similarity_search(query)
  results = chain({"input_documents":documents,"question":query},return_only_outputs=True)
  results = results['intermediate_steps'][0]
  return results
  

def add_background_image(image_file):
  with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_background_image('aipic.png')   


uploaded_file = st.file_uploader('Upload a file')
if uploaded_file is not None:
   save_uploadedfile(uploaded_file )
   raw_pdf_document_content = get_file_content(str(uploaded_file.name))
   pdf_document_chunks = text_splitter.split_text(raw_pdf_document_content)
   doc_search_paper = create_vector_index(pdf_document_chunks)
   print(doc_search_paper)
   question_from_user = st.text_input("I am your file, please enter your question, I can answer")
   if question_from_user is not None:
     results = speak_with_file(str(uploaded_file.name),question_from_user)
     answer = results["answer"]
     confidence_score = results["score"]
     st.write(f"{answer} \n {confidence_score}")
