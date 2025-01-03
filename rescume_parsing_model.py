# -*- coding: utf-8 -*-
"""Rescume_parsing_model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Udf5KUCR35DyFpO-XFbcxtJVxqC5se-U
"""

import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import json

print(spacy.__version__)

#print(!nvidia-smi)

cv_data = json.load(open('/content/drive/MyDrive/Colab Notebooks/Rescume parser/dataset.json','r'))

len(cv_data)

cv_data[0]

#pip install spacy-transformers

# change in another way to fill base config file into config file
#!python -m spacy init fill-config "/content/drive/MyDrive/Colab Notebooks/Rescume parser/config/base_config.cfg" "/content/drive/MyDrive/Colab Notebooks/Rescume parser/config/config.cfg"

# def get_spacy_doc(file,data):
#   nlp = spacy.blank("en")
#   db = DocBin()

#   for text,annot in tqdm(data):
#     doc = nlp.make_doc(text)
#     annot = annot['entities']
#     ents = []
#     entity_indices = []

#     for start, end, label in annot:
#       skip_entity = False
#       for idx in range(start,end):
#         if idx in entity_indices:
#           skip_entity = True
#           break
#       if skip_entity == True:
#         continue

#         entity_indices = entity_indices + list(range(start,end))

#         try:
#           span = doc.char_span(start,end,label=label,alignment_mode="strict")
#         except:
#           continue

#           if span is None:
#             err_data = str([start,end]) + " " + str(text) + "\n"
#             file.write(err_data)

#           else:
#               ents.append(span)
#           try:
#               doc.ents = ents
#               db.add(doc)
#           except:
#               pass

#     return db

import spacy
from spacy.tokens import DocBin
from tqdm import tqdm

def get_spacy_doc(file, data):
    nlp = spacy.blank("en")
    db = DocBin()

    for text, annot in tqdm(data, desc="Processing data"):
        doc = nlp.make_doc(text)
        ents = []
        entity_indices = []

        for start, end, label in annot['entities']:
            skip_entity = False

            # Check for overlapping entities
            for idx in range(start, end):
                if idx in entity_indices:
                    skip_entity = True
                    break

            if skip_entity:
                continue

            # Update the entity indices to avoid overlaps
            entity_indices.extend(range(start, end))

            # Create span and handle errors
            span = doc.char_span(start, end, label=label, alignment_mode="strict")
            if span is None:
                err_data = f"[{start}, {end}] {text}\n"
                file.write(err_data)
            else:
                ents.append(span)

        # Assign entities to the document and add to DocBin
        try:
            doc.ents = ents
            db.add(doc)
        except Exception as e:
            file.write(f"Error processing document: {text}\nException: {str(e)}\n")

    return db

from sklearn.model_selection import train_test_split
train,test = train_test_split(cv_data,test_size=0.3)

len(train), len(test)

file = open('/content/drive/MyDrive/Colab Notebooks/Rescume parser/Model_testing/train_file.txt','w')

db = get_spacy_doc(file,train)
db.to_disk('/content/drive/MyDrive/Colab Notebooks/Rescume parser/Model_testing/train_data.spacy')

db = get_spacy_doc(file,test)
db.to_disk('/content/drive/MyDrive/Colab Notebooks/Rescume parser/Model_testing/test_data.spacy')

file.close()
#change the way of training or fitting in the next line
#!python -m spacy train "/content/drive/MyDrive/Colab Notebooks/Rescume parser/config/config.cfg" --output "/content/drive/MyDrive/Colab Notebooks/Rescume parser/Model_testing/output" --paths.train "/content/drive/MyDrive/Colab Notebooks/Rescume parser/Model_testing/train_data.spacy" --paths.dev "/content/drive/MyDrive/Colab Notebooks/Rescume parser/Model_testing/test_data.spacy" --gpu-id 0

nlp = spacy.load('/content/drive/MyDrive/Colab Notebooks/Rescume parser/Model_testing/output/model-best')

#pip install PyMuPDF
#pip install fitz

import sys, fitz
fname= "/content/drive/MyDrive/Colab Notebooks/Rescume parser/tests/Alice Clark CV.pdf"

text= " "
for page in doc:
  text = text + str(page.get_text())

text

doc =nlp(text)
for ent in doc.ents:
  print(ent.text, "   ->>>>>>>>>>>    ",ent.label_)