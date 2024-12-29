import spacy
import fitz  # PyMuPDF for handling PDFs
#from pymupdf import fitz


# Load the SpaCy model
#model_path =r"F:\Seventh Term\graduation project\time plan\22-12 work\Models-20241227T205505Z-001\Models\JdModel\output\model-best"
model_path = r"F:\Seventh Term\graduation project\time plan\22-12 work\Models-20241227T205505Z-001\Models\ResumeModel\output\model-best"
nlp = spacy.load(model_path)

# Define the path to your PDF file
#pdf_file = r"F:\Seventh Term\graduation project\time plan\22-12 work\datasets_test\tests\Alice Clark CV.pdf"
pdf_file = r"F:\Seventh Term\Waleed_Resume.pdf"

# Extract text from the PDF
doc = fitz.open(pdf_file)
text = ""
for page in doc:
    text += page.get_text()

print("Extracted Text:")
print(text)

# Apply the model to the extracted text
doc = nlp(text)

# Print recognized entities
#skills=set()
#social_media=set()
print("\nExtracted Entities:")
for ent in doc.ents:
    #if ent.label_ == 'SKILLS':
    print(ent.text, " ->>>>>>>>>>> ", ent.label_)
        #skills.add(ent.text)
    #elif ent.label_ == 'LINKEDIN LINK'or 'EMAIL ADDRESS':
        #social_media.add(ent.text)

#print(skills ,'\n')
#print(social_media)