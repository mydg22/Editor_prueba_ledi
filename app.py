# app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
# Asegúrate de que el prompt_generator esté en el mismo directorio o accesible en la ruta de Python
from prompt_generator import generate_ledi_suggestion_prompt

# *** CAMBIO CLAVE AQUÍ: Importar Google Gemini en lugar de OpenAI ***
import google.generativeai as genai
import json

app = Flask(__name__)
CORS(app) # Esto permite peticiones desde cualquier origen (necesario para el frontend público)

# *** CAMBIO CLAVE AQUÍ: Configura tu clave de API usando una variable de entorno para GEMINI ***
# Render te permitirá establecer GEMINI_API_KEY en su configuración de variables de entorno.
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


@app.route('/sugerir', methods=['POST'])
def sugerir_contenido_interactivo():
    data = request.json
    texto_contenido = data.get('texto_contenido')
    discipline = data.get('discipline', 'general') # Valor por defecto 'general'
    educational_level = data.get('educational_level', 'universitario') # Valor por defecto 'universitario'

    if not texto_contenido:
        return jsonify({"error": "El campo 'texto_contenido' es requerido."}), 400

    try:
        # Genera el prompt LEDI con la disciplina y el nivel educativo
        prompt_para_ia = generate_ledi_suggestion_prompt(
            texto_contenido,
            discipline=discipline,
            educational_level=educational_level
        )

        # *** CAMBIO CLAVE AQUÍ: Llama a la API de Google Gemini ***
        # Crea una instancia del modelo Gemini
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", # Puedes probar con "gemini-pro" o "gemini-1.5-pro" si 1.5-flash no está disponible o quieres más capacidad
            system_instruction="You are a helpful assistant that generates JSON." # Instrucción de sistema para JSON
        )

        # Genera contenido con la instrucción de sistema y el modo JSON
        response = model.generate_content(
            prompt_para_ia,
            generation_config=genai.GenerationConfig(response_mime_type="application/json") # Fuerza la respuesta JSON
        )

        # Acceder al texto JSON de la respuesta
        ai_response_content = response.text
        sugerencias = json.loads(ai_response_content)

        # Asegúrate de que la respuesta sea un array, incluso si la IA devuelve un solo objeto
        if not isinstance(sugerencias, list):
            sugerencias = [sugerencias] # Envuelve en una lista si es un solo objeto

        return jsonify({"sugerencias": sugerencias}), 200

    # *** CAMBIO CLAVE AQUÍ: Excepciones específicas de Google Gemini ***
    except Exception as e:
        # Google Gemini no tiene las mismas excepciones detalladas que OpenAI para autenticación, etc.
        # Capturaremos cualquier excepción y la reportaremos. Si la API key es inválida,
        # lo más probable es que falle aquí y veamos el error en los logs de Render.
        return jsonify({"error": f"Ocurrió un error al comunicarse con la API de Gemini: {str(e)}"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "La IA no devolvió un JSON válido. Intenta con un texto más claro o revisa el prompt."}), 500
    except Exception as e: # Una captura general para cualquier otra cosa
        return jsonify({"error": f"Ocurrió un error inesperado en el servidor: {str(e)}"}), 500

if __name__ == '__main__':
    # En Render, Gunicorn se encargará de correr la aplicación,
    # esta parte solo se usa para pruebas locales.
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", 5000))