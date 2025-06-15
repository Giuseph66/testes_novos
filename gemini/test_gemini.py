import requests
import json

def test_gemini_api():
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    # Your API key
    api_key = "AIzaSyD8AUUxeuO9Df465lJmy0oBvvg7rRtlenA"
    
    # Headers
    headers = {
        "Content-Type": "application/json"
    }
    
    # Request payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": """Você é uma IA que está no meio de uma conversa e deve respondê-la como se estivesse dando continuidade ao diálogo. Aqui está o histórico resumido da conversa anterior: 

[INÍCIO DO HISTÓRICO]
Você: Olá, como você está?
IA: Estou bem, obrigado! E você?
Você: Estou ótimo! O que você tem feito ultimamente?
IA: Tenho aprendido muito sobre programação e inteligência artificial. É fascinante!
Você: Que legal! Eu também estou aprendendo sobre IA. Você pode me dar algumas dicas?
[FIM DO HISTÓRICO]

Agora continue a conversa a partir disso, como se estivesse em andamento, respondendo diretamente à última fala da pessoa. 
Sua resposta deve ser breve, clara e focada.
"""
                    }
                ]
            }
        ]
    }
    
    # Make the request
    response = requests.post(
        f"{url}?key={api_key}",
        headers=headers,
        json=payload
    )
    
    # Print the response
    print("Status Code:", response.status_code)
    print("\nResponse:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_gemini_api() 