from pdfparser import  extract_text
from chunk import create_chunks
from embeddings import create_embeddings
# print(
#     extract_text(
#         "upload/infosys-ar-26.pdf"
#     )
# )

text = extract_text("upload/infosys-ar-26.pdf")
chunks = create_chunks(text)
print(len(chunks))

vectors = create_embeddings(chunks)
print(vectors.shape)