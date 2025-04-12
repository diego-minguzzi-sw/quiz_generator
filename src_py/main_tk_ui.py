#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Diego Minguzzi 2025
#

"""
Using Python, create a TkInter GUI interface that can is adaptable so that the window can be maximized in full scheen.
The UI must show:
. a top button buttGenerateQuestion with the label 'Genera domanda.'
. below the button buttGenerateQuestion, a text area question, its with fills the entire window, it can have scrollbars and host up to 100 lines, at the beginning populated with '...'
. below a 3 rows, 2 columns grid : where each row has :
  . a text area, one line, and a button choice
  . the text area variables are named text1, text2, text3
  . at the beginning the text1 area contains 'Risposta 1'
  . at the beginning the text2 area contains 'Risposta 2'
  . at the beginning the text2 area contains 'Risposta 3'
  . the choice button variables are named answ1, answ2, answ3.
  . the button answ1 has label Risposta 1
  . the button answ2 has label Risposta 2
  . the button answ3 has label Risposta 3
  . text1 fills the entire windows with, except the space for the button answ1
  . text2 fills the entire windows with, except the space for the button answ2
  . text2 fills the entire windows with, except the space for the button answ3
. under the grid , a result text area called result, that fills the entire window width
. at the beginning result is initialized with 'Risultato'
. under the result, an explanation text ares, that fills the entire window width
. at the beginning explanation is initialized with 'Spiegazione'
. an OK button that exits the application.
"""
from langchain_google_genai import ChatGoogleGenerativeAI

import entities

import copy
import json
import logging as log
import os
import random
import pickle
import pprint
import random
import tkinter as tk

from tkinter import scrolledtext

defaultFont= ("DejaVu Sans", 14)

modelName="gemini-2.0-flash"

maxOutputTokens=8192
temperature=1.0

promptTemplate="""
Sei un esperto in grado di generare domande a risposta chiusa su un regolamento comunale, per una persona la quale deve sostenere un esame di ammissione per una selezione a scopo assunzione.
L'esame richiede la conoscenza degli articoli del regolamento.  Ogni articolo ha un titolo ed un testo.
Dato un articolo, genera un risultato composto da:
. una domanda
. possibili risposte a tale domanda, in cui la prima risposta è giusta, le altre sono sbagliate.
. la spiegazione del perchè la prima risposta è vera, considerando il testo dell'articolo.
Le risposte sbagliate contengono informazioni plausibili ma in contrasto o non consistenti con quanto scritto nell'articolo.

Il risultato deve essere formattato in JSon, come di seguito.
Il campo question contiene la domanda, il campo answers contiene la lista delle possibili risposte.
Genera sempre tre possibili risposte alla domanda.

Esempio del formato della risposta:

{
  "question": "Domanda",
  "answers": ["Risposta 1", "Risposta 2", "Risposta 3"],
  "explanation": "Spiegazione del perche' la prima risposta è vera."
}


Nel formulare la domanda e le risposte, utilizza solamente il titolo e testo dell'articolo, non introdurre altre informazioni estranee ad esso o inventate. Genera solamente Json valido.

Esempio di articolo:
TITOLO:
UBICAZIONE E ORARI DEI CIMITERI

TESTO:
Il Comune ha inoltre Cimiteri Speciali nelle seguenti frazioni: - Casale Popolo, Terranova, Santa Maria del Tempio, San Germano, Torcello-Rolasco, Roncaglia.  L'orario di apertura al pubblico dei cimiteri viene determinato dal Sindaco a seconda delle stagioni. Nei giorni di neve il cimitero resta chiuso ai visitatori, sino a quando si saranno praticati gli opportuni passaggi ed accessi.

Esempio di risposta:
{
  "question": "Chi decide l'orario di apertura al pubblico dei cimiteri?",
  "answers": ["Il Sindaco, inoltre l'orario dipende dalle stagioni", "Il consiglio comunale ad ogni inizio anno, riunito in seduta plenaria", "L'assessore ai lavori pubblici, tramite referendum che coinvolge i cittadini"],
  "explanation":"L'articolo specifica che l'orario di apertura al pubblico dei cimiteri viene determinato dal Sindaco a seconda delle stagioni."
}

Di seguito l'articolo su cui devi generare il risultato:
---
"""

#---------------------------------------------------------------------------------------------------
document = entities.Document()
question = None
text_area_question = None
numCorrect=0
numWrong=0

def generate_llm_question():
    log.info('generate_llm_question')

    llm = ChatGoogleGenerativeAI(model=modelName,
                                max_output_tokens=maxOutputTokens,
                                temperature=temperature)

    assert document.numArticles>0

    indexArticle = random.randint(0, document.numArticles-1)
    article = document.article(indexArticle)

    arguments= {'title':article.title, 'text':article.text}
    prompt= copy.copy(promptTemplate)
    prompt += f'TITOLO: { article.title}\n\n'
    prompt += f'TESTO:  { article.text}\n'
    result = llm.invoke(prompt)

    textContent= str(result.content)
    if textContent.startswith("```json"):
        textContent= textContent.replace("```json", "", 1)
    if textContent.endswith("```"):
        textContent= textContent[0:-3]

    parsedResult = json.loads( textContent)
    return entities.Question( question= parsedResult['question'],
                              answers= parsedResult['answers'],
                              explanation= parsedResult['explanation'],
                              indexArticle=indexArticle)


#---------------------------------------------------------------------------------------------------
def selectedAnswer( indxAnswer: int):
    global question
    global numCorrect
    global numWrong

    log.info(f'selectedAnswer: indxAnswer:{indxAnswer}')
    if question is None:
        result.delete(1.0, tk.END)
        result.insert(tk.END, "Genera prima una domanda.")  # Initial placeholder
        return

    result.delete(1.0, tk.END)
    if indxAnswer == question.indexCorrectAnswer:
        result.insert(tk.END, "Risposta corretta!!")
        numCorrect += 1
    else:
        result.insert(tk.END, f"Risposta sbagliata: la risposta corretta è la {question.indexCorrectAnswer+1}.")
        numWrong += 1

    explanation.delete(1.0, tk.END)
    explanation.insert(tk.END, question.explanation)

    refArticle = document.article( question.indexArticle)
    textArticle= f'Articolo:{question.indexArticle}\n{refArticle}'

    article.delete(1.0, tk.END)
    article.insert(tk.END, textArticle)

    statistics.delete(1.0, tk.END)
    statistics.insert(tk.END, f'Numero risposte giuste:{numCorrect} sbagliate:{numWrong}')
    question= None

#---------------------------------------------------------------------------------------------------
def generate_question():
    log.info('generate_question')
    # Just an example to update the text areas
    global document
    global question
    question = None

    question_text = "Genera una domanda qui"
    text1.delete(1.0, tk.END)
    text2.delete(1.0, tk.END)
    text3.delete(1.0, tk.END)
    article.delete(1.0, tk.END)
    explanation.delete(1.0, tk.END)

    try:
        question= generate_llm_question()
    except Exception as exc:
        result_text= str(exc)
        log.error(f'Exception:{result_text}')
        question= None
        return

    question_text = question.question
    text_area_question.delete(1.0, tk.END)
    text_area_question.insert(tk.END, question_text)

    # Example to update the answer options and result dynamically
    text1.delete(1.0, tk.END)
    text1.insert(tk.END, question.answer(0))
    text2.delete(1.0, tk.END)
    text2.insert(tk.END, question.answer(1))
    text3.delete(1.0, tk.END)
    text3.insert(tk.END, question.answer(2))

    result_text = "..."
    result.delete(1.0, tk.END)
    result.insert(tk.END, result_text)

    explanation_text = "..."
    explanation.delete(1.0, tk.END)
    explanation.insert(tk.END, explanation_text)


# Create main window
root = tk.Tk()
root.title("Generatore Domande")

# Make the window adaptable and maximize
root.geometry("1500x1000")  # Initial window size
root.state('normal')  # Ensure the window can be resized

# Frame for top button and question text area
frame_top = tk.Frame(root)
frame_top.pack(fill=tk.X)

# Button to generate question
buttGenerateQuestion = tk.Button(frame_top, text="Genera domanda", command=generate_question)
buttGenerateQuestion.pack(padx=10, pady=10)

# Text area for the question with scrollbar
text_area_question = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=3, font=defaultFont)
text_area_question.pack(fill=tk.BOTH, padx=10, pady=10)
text_area_question.insert(tk.END, "...")  # Initial placeholder

# Frame for the grid of answer rows
frame_grid = tk.Frame(root)
frame_grid.pack(fill=tk.X, padx=10, pady=10)

# Create a grid of 3 rows, each with a text area and button
textWidth= 100
text1 = scrolledtext.ScrolledText(frame_grid, height=1, width=textWidth, font=defaultFont)
text1.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
text1.insert(tk.END, "Risposta 1")

answ1 = tk.Button(frame_grid, text="Risposta 1", command=lambda: selectedAnswer(0))
answ1.grid(row=0, column=1, padx=5, pady=5)

text2 = scrolledtext.ScrolledText(frame_grid, height=1, width=textWidth, font=defaultFont)
text2.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
text2.insert(tk.END, "Risposta 2")

answ2 = tk.Button(frame_grid, text="Risposta 2", command=lambda: selectedAnswer(1))
answ2.grid(row=1, column=1, padx=5, pady=5)

text3 = scrolledtext.ScrolledText(frame_grid, height=1, width=textWidth, font=defaultFont)
text3.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
text3.insert(tk.END, "Risposta 3")

answ3 = tk.Button(frame_grid, text="Risposta 3", command=lambda: selectedAnswer(2))
answ3.grid(row=2, column=1, padx=5, pady=5)

# Text area for the result
result = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=2, font=defaultFont)
result.pack(fill=tk.BOTH, padx=10, pady=10)
result.insert(tk.END, "")  # Initial placeholder

# Text area for the explanation
explanation = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=2, font=defaultFont)
explanation.pack(fill=tk.BOTH, padx=10, pady=10)
explanation.insert(tk.END, "")  # Initial placeholder

article = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, font=defaultFont)
article.pack(fill=tk.BOTH, padx=10, pady=10)
article.insert(tk.END, "")  # Initial placeholder

statistics = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=1, font=defaultFont)
statistics.pack(fill=tk.BOTH, padx=10, pady=10)
statistics.insert(tk.END, "")  # Initial placeholder

# Button to exit the application
ok_button = tk.Button(root, text="Esci", command=root.quit)
ok_button.pack(padx=10, pady=10)

#---------------------------------------------------------------------------------------------------
def main():
    global document

    StorageEnvVarName = 'STORAGE_ROOT'
    assert StorageEnvVarName in os.environ
    StorageEnvVar= os.environ[StorageEnvVarName]
    log.info(f'StorageEnvVar:{StorageEnvVar}')

    documentFile= os.path.join( StorageEnvVar,'document.pickle' )
    with open(documentFile, 'rb') as file:
        document = pickle.load(file)

    log.info(f'Num articles:{document.numArticles}')

    root.mainloop()

#---------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    _FORMAT_STRING = "%(module)s.%(funcName)s():%(lineno)d %(asctime)s\n[%(levelname)-5s] %(message)s\n"
    log.basicConfig(level= log.ERROR, format=_FORMAT_STRING)
    main()
