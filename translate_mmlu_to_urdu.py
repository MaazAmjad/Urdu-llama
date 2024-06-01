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


# Convert the list to JSON
json_translated_questions = json.dumps(translated_questions, ensure_ascii=False).encode('utf8')

# Write the JSON data to a file
with open('translated_data.json', 'w', encoding='utf-8') as f:
    f.write(json_translated_questions.decode())


