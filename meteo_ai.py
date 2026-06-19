import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def get_weather(city):
    return "22°C si partial noros"

unelte_meteo = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Afla vremea curenta intr-un oras",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "Orasul cautat"}},
            "required": ["city"],
        },
    },
}]

print("\n--- 1. MODELUL SIMPLU (FARA TOOLS) ---")
rsp1 = client.chat.completions.create(
    model="qwen2.5:0.5b",
    messages=[{"role": "user", "content": "Cum e vremea acum in Bucuresti?"}]
)
print("Raspuns Model Simplu (Halucinatie):", rsp1.choices[0].message.content)

print("\n--- 2. MODELUL CU TOOL CALLS (AGENT INTELIGENT) ---")
mesaje = [{"role": "user", "content": "Cum e vremea acum in Bucuresti?"}]
rsp2 = client.chat.completions.create(
    model="qwen2.5:0.5b",
    messages=mesaje,
    tools=unelte_meteo
)

msg = rsp2.choices[0].message
if msg.tool_calls:
    tool = msg.tool_calls[0]
    print(f"[Sistem] AI-ul apeleaza functia: {tool.function.name}")
    
    args = json.loads(tool.function.arguments)
    rezultat_meteo = get_weather(args["city"])
    print(f"[Sistem] Aplicatia meteo ii transmite: {rezultat_meteo}")
    
    mesaje.append(msg)
    mesaje.append({"role": "tool", "tool_call_id": tool.id, "content": rezultat_meteo})
    
    rsp_final = client.chat.completions.create(model="qwen2.5:0.5b", messages=mesaje, tools=unelte_meteo)
    print("Raspuns Final AI:", rsp_final.choices[0].message.content)
