import streamlit as st
import helper as helper1



def save_uploadedfile(uploadedfile):
     with open(uploadedfile.name,"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success("Saved")
  
def get_file_content(file_path):
  if("pdf" in file_path):
   loader=UnstructuredFileLoader(file_path)
  elif("png" in file_path):
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


uploaded_file = st.file_uploader('Upload a file')
if uploaded_file is not None:
   save_uploadedfile(uploaded_file )
   raw_pdf_document_content = helper1.get_file_content(str(uploaded_file.name))
   pdf_document_chunks = text_splitter.split_text(raw_pdf_document_content)
   doc_search_paper = create_vector_index(pdf_document_chunks)
   print(doc_search_paper)
   question_from_user = st.text_input("I am your file, please enter your question, I can answer")
   if question_from_user is not None:
    results = speak_with_file(str(uploaded_file.name),question_from_user)
    answer = results["answer"]
    confidence_score = results["score"]
    st.write(f"{answer} \n {confidence_score}")
