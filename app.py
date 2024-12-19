from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Debug - Imprimir variables de entorno
api_key = os.getenv('OPENAI_API_KEY')
assistant_id = os.getenv('ASSISTANT_ID')
print("\n=== Configuración ===")
print(f"API Key (primeros 10 caracteres): {api_key[:10] if api_key else 'No encontrada'}")
print(f"Assistant ID: {assistant_id if assistant_id else 'No encontrado'}\n")

client = OpenAI(api_key=api_key)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # 1. Verificar el mensaje recibido
        data = request.json
        print(f"Mensaje recibido: {data}")
        
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
            
        message = data['message']
        
        # 2. Verificar el ID del asistente
        if not assistant_id:
            return jsonify({'error': 'Assistant ID not configured'}), 500
            
        # 3. Crear thread
        thread = client.beta.threads.create()
        print(f"Thread creado: {thread.id}")
        
        # 4. Añadir mensaje
        message_obj = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )
        print(f"Mensaje añadido: {message_obj.id}")
        
        # 5. Ejecutar asistente
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )
        print(f"Run creado: {run.id}")
        
        # 6. Esperar respuesta
        while run.status != 'completed':
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            print(f"Estado del run: {run.status}")
        
        # 7. Obtener respuesta
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        response = messages.data[0].content[0].text.value
        
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"\n=== ERROR ===\n{str(e)}\n")
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'ok',
        'api_key_present': bool(api_key),
        'assistant_id_present': bool(assistant_id)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)