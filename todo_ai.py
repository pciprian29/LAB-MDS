import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

lista_todo = []

def adauga_task(task, data):
    lista_todo.append({"Task": task, "Data": data})
    return f"Succes! Am salvat."

unelte_todo = [{
    "type": "function",
    "function": {
        "name": "adauga_task",
        "description": "Adauga o sarcina noua in lista de TODO",
        "parameters": {
            "type": "object",
            "properties": {
                "task": {"type": "string", "description": "Ce trebuie facut"},
                "data": {"type": "string", "description": "Ziua sau data la care trebuie facut"}
            },
            "required": ["task", "data"],
        },
    },
}]

print("--- APLICATIE TODO CU AGENT AI ---")
prompt_natural = input("Spune-i AI-ului o sarcina (ex: Adauga sa imi platesc facturile maine): ")

rsp = client.chat.completions.create(
    model="qwen2.5:0.5b",
    messages=[{"role": "user", "content": prompt_natural}],
    tools=unelte_todo
)

msg = rsp.choices[0].message
if msg.tool_calls:
    for call in msg.tool_calls:
        date_extrase = json.loads(call.function.arguments)
        print(f"\n[AI-ul a inteles!] -> Sarcina: '{date_extrase.get('task', '')}', Data: '{date_extrase.get('data', '')}'")
        
        adauga_task(date_extrase.get('task', ''), date_extrase.get('data', ''))

print("\nBaza de date TODO dupa apel:", lista_todo)
