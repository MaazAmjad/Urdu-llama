import googletrans
from datasets import load_dataset
import json

# Initialize the translator
translator = googletrans.Translator()

# Load the dataset
dataset_name = "cais/mmlu"
dataset = load_dataset(dataset_name, "college_biology")

# Get the test set questions
questions = dataset['test']['question']

urdu_dataset = []

# Translate each question to Urdu
translated_questions = []

for i in range(len(dataset['dev'])):
    question = dataset['dev'][i]['question']
    choices = dataset['dev'][i]['choices']
    translated_qestion = translator.translate(question, dest='ur', src='en')
    
    D = {}
    D['question'] = translated_qestion.text
    D['choices'] = []
    for choice in choices:
        translated_choice = translator.translate(choice, dest='ur', src= 'en')
        D['choices'].append(translated_choice.text)
        #print(choice, translated_choice.text)

    D['subject'] = dataset['dev'][i]['subject']
    D['answer'] = dataset['dev'][i]['answer']

    #input(translated_qestion.text)
    translated_questions.append(D)


with open("translated_data.json", "w") as final:
    json.dump(translated_questions, final)
    

