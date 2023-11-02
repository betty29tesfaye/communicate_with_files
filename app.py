#from communicate_with_files.helper import save_uploadedfile
#from mount.src.communicate_with_files.helper import save_uploadedfile

from PIL import Image

image = Image.open('nlp.png')

st.image(image, caption='')


# os.environ['OPENAI_API_KEY']= "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"
#"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"
#"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" #previous key
#nlp.png


# uploaded_file = st.file_uploader('Upload a file')
# if uploaded_file is not None:
#    save_uploadedfile(uploaded_file )
#    raw_pdf_document_content = get_file_content(str(uploaded_file.name))
#    pdf_document_chunks = text_splitter.split_text(raw_pdf_document_content)
#    doc_search_paper = create_vector_index(pdf_document_chunks)
#    print(doc_search_paper)
#    question_from_user = st.text_input("I am your file, please enter your question, I can answer")
#    if question_from_user is not None:
#     results = speak_with_file(str(uploaded_file.name),question_from_user)
#     answer = results["answer"]
#     confidence_score = results["score"]
#     st.write(f"{answer} \n {confidence_score}")
