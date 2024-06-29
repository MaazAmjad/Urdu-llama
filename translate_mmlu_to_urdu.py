import googletrans
from datasets import load_dataset
import json
import time
from tqdm import tqdm

# Initialize the translator
translator = googletrans.Translator()

# Load the dataset
dataset_name = "cais/mmlu"
dataset = load_dataset(dataset_name, "all")

# Initialize variables
translated_questions = []
num_questions = 0
batch_counter = 0
batch_size = 500
max_retries = 5

# Master JSON file name
master_file = 'translated_data_master.json'

# Function to handle translation with retries on timeout
def translate_with_retry(text, dest_lang='ur', src_lang='en', retries=max_retries):
    attempts = 0
    while attempts <= retries:
        try:
            translation = translator.translate(text, dest=dest_lang, src=src_lang)
            return translation.text
        except googletrans.exceptions.TranslatorError as e:
            print(f"Translation attempt {attempts + 1} failed: {str(e)}")
            attempts += 1
            time.sleep(5)  # Wait for 5 seconds before retrying
    print(f"Translation failed after {retries} attempts for: {text}")
    return None

# Iterate through the dataset with tqdm for progress bar
for i in tqdm(range(len(dataset['dev'])), desc="Translating Questions"):
    question = dataset['dev'][i]['question']
    choices = dataset['dev'][i]['choices']
    translated_choices = []

    # Translate each choice
    for choice in choices:
        translated_choice = translate_with_retry(choice)
        if translated_choice:
            translated_choices.append(translated_choice)
        else:
            continue  # Skip to next question if translation fails after retries
    
    if not translated_choices:
        continue  # Skip this question if all choices failed to translate

    # Translate the question
    translated_question = translate_with_retry(question)

    if not translated_question:
        continue  # Skip this question if translation fails after retries

    # Prepare the dictionary
    D = {
        'question': translated_question,
        'choices': translated_choices,
        'subject': dataset['dev'][i]['subject'],
        'answer': dataset['dev'][i]['answer']
    }

    # Append to translated_questions
    translated_questions.append(D)
    num_questions += 1

    # Write to master JSON file after each translation
    with open(master_file, 'a', encoding='utf-8') as master_f:
        json.dump(D, master_f, ensure_ascii=False)
        master_f.write('\n')  # Newline for separating entries

    # Write to JSON file if batch size reached
    if num_questions % batch_size == 0:
        batch_counter += 1
        json_translated_questions = json.dumps(translated_questions, ensure_ascii=False).encode('utf8')
        with open(f'translated_data_batch{batch_counter}.json', 'w', encoding='utf-8') as f:
            f.write(json_translated_questions.decode())
        translated_questions = []  # Clear list for next batch

    # Sleep after every 10 questions
    if num_questions % 10 == 0:
        time.sleep(2)

# Final write for remaining questions
if translated_questions:
    batch_counter += 1
    json_translated_questions = json.dumps(translated_questions, ensure_ascii=False).encode('utf8')
    with open(f'translated_data_batch{batch_counter}.json', 'w', encoding='utf-8') as f:
        f.write(json_translated_questions.decode())
