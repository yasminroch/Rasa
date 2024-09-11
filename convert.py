import csv
import yaml

def csv_to_rasa(csv_filepath):
    intents = {}
    responses = {}
    stories = []
    rules = []

    # Ler CSV e organizar dados
    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            intent = row['intent']
            question = row['question']
            answer = row['answer']

            if intent not in intents:
                intents[intent] = []
                responses[intent] = set()  # Usar set para evitar respostas duplicadas

            intents[intent].append(question)
            responses[intent].add(answer)

            # Gerar uma story simples e uma rule para cada intent
            stories.append({
                'story': f'Generated story for {intent}',
                'steps': [
                    {'intent': intent},
                    {'action': f'utter_{intent}'}
                ]
            })
            rules.append({
                'rule': f'Generated rule for {intent}',
                'steps': [
                    {'intent': intent},
                    {'action': f'utter_{intent}'}
                ]
            })

    # Salvar NLU
    nlu_data = {'version': '3.0', 'nlu': [{'intent': intent, 'examples': '\n'.join(f'- {ex}' for ex in examples)} for intent, examples in intents.items()]}
    with open('data/nlu.yml', 'w') as f:
        yaml.dump(nlu_data, f, allow_unicode=True)

    # Salvar Domain
    domain_data = {
        'version': '3.0',
        'intents': list(intents.keys()),
        'responses': {f'utter_{intent}': [{'text': text} for text in texts] for intent, texts in responses.items()},
        'actions': [f'utter_{intent}' for intent in intents.keys()]
    }
    with open('domain.yml', 'w') as f:
        yaml.dump(domain_data, f, allow_unicode=True)

    # Salvar Stories
    stories_data = {'version': '3.0', 'stories': stories}
    with open('data/stories.yml', 'w') as f:
        yaml.dump(stories_data, f, allow_unicode=True)

    # Salvar Rules
    rules_data = {'version': '3.0', 'rules': rules}
    with open('rules.yml', 'w') as f:
        yaml.dump(rules_data, f, allow_unicode=True)

# Uso do script
csv_to_rasa('dataset/rasa_augmented_data.csv')
