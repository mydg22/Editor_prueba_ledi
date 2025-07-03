# prompt_generator.py (debe contener la versión con la referencia a H5P)

import json

def generate_ledi_suggestion_prompt(text_content, discipline="general", educational_level="universitario"):
    # --- Definición del Rol y Objetivo de la IA ---
    role_and_objective = f"""
Eres un **experto en diseño instruccional para la educación superior**, especializado en la creación de material interactivo que mejora la comprensión y la retención de conceptos complejos. Tu objetivo es ayudar a un profesor universitario a idear y estructurar elementos interactivos para sus libros electrónicos didácticos, **especialmente aquellos que pueden ser creados o soportados por H5P.**

La disciplina de este contenido es **{discipline}** y está dirigido a estudiantes de nivel **{educational_level}**.
"""

    # --- Tipos de Interacción Permitidos ---
    allowed_interaction_types = """
Debes sugerir elementos **únicamente** de la siguiente lista, pensando en su implementación práctica, preferiblemente **con herramientas como H5P**:
- "Animación" (ej. Explicador de proceso, infografía animada)
- "Video Interactivo" (ej. Vídeo con preguntas incrustadas, puntos de información)
- "Cuestionario" (ej. Múltiple Opción, Verdadero/Falso, Arrastrar y Soltar Texto, Rellenar espacios en blanco)
- "Ejercicio Práctico" (ej. Simulación interactiva, Pregunta de arrastrar y soltar, Escenario de ramificación)
- "Tabla Comparativa Interactiva" (ej. Tabla con información expandible/colapsable)
- "Estudio de Caso Interactivo" (ej. Presentación con ramificaciones)
- "Infografía Interactiva" (ej. H5P Interactive Book/Course Presentation)
- "Mapa Conceptual Interactivo" (ej. H5P Mark the Words, Drag the words)
"""

    # --- Formato de Salida Requerido (JSON) y Ejemplos ---
    output_format_instructions = """
Para cada sugerencia, proporciona las siguientes claves:
1.  **"tipo_sugerencia"**: Uno de los tipos permitidos de la lista anterior.
2.  **"contexto_detectado"**: Una frase concisa del texto original (o concepto clave) que justifica la sugerencia.
3.  **"propuesta"**: Una descripción clara y concreta del elemento interactivo sugerido, **mencionando si es un tipo común de H5P o cómo se implementaría con él si es relevante.**
4.  **"justificacion_pedagogica"**: Una explicación concisa de por qué este elemento es didácticamente efectivo para el contexto dado.

Las sugerencias deben ser **directamente relevantes** al contenido y **aportar un valor pedagógico significativo**. Si el texto no se presta a interactividad relevante, devuelve un array JSON vacío.

Formatea tu respuesta **siempre** como un array JSON de objetos.

Ejemplo de formato de salida:
[
    {
        "tipo_sugerencia": "Video Interactivo",
        "contexto_detectado": "proceso de fotosíntesis",
        "propuesta": "Video interactivo (tipo H5P Interactive Video) que visualiza el ciclo de la fotosíntesis con preguntas incrustadas en puntos clave.",
        "justificacion_pedagogica": "Mejora la atención y evalúa la comprensión en tiempo real mientras el estudiante consume el video."
    },
    {
        "tipo_sugerencia": "Cuestionario",
        "contexto_detectado": "definición de programación orientada a objetos",
        "propuesta": "Cuestionario (tipo H5P Multiple Choice) con 3-5 preguntas de opción múltiple sobre los cuatro pilares de la POO.",
        "justificacion_pedagogica": "Evalúa la comprensión de conceptos fundamentales y permite la autoevaluación formativa."
    }
]
"""

    # --- Construcción del Prompt Final ---
    final_prompt = f"""
{role_and_objective}

Aquí está el fragmento de texto del libro electrónico para el cual necesitas generar sugerencias:
"{text_content}"

Considerando este texto, identifica conceptos clave, ideas importantes o secciones que podrían beneficiarse enormemente de la interactividad.

{allowed_interaction_types}

{output_format_instructions}
"""
    return final_prompt

if __name__ == '__main__':
    print("--- Generador de Prompts LEDI Interactivo ---")
    print("Ingresa 'salir' en el texto para terminar.")

    while True:
        print("\n--- NUEVA PRUEBA ---")
        user_text = input("Pega el texto del libro aquí (o 'salir'):\n")
        if user_text.lower() == 'salir':
            print("Saliendo del generador de prompts.")
            break

        user_discipline = input("Disciplina (ej. 'Ingeniería Electrónica', 'Biología', 'Historia' - Enter para 'general'): ")
        if not user_discipline:
            user_discipline = "general"

        user_level = input("Nivel Educativo (ej. 'Pregrado', 'Posgrado', 'Bachillerato' - Enter para 'universitario'): ")
        if not user_level:
            user_level = "universitario"

        generated_prompt = generate_ledi_suggestion_prompt(
            user_text,
            discipline=user_discipline,
            educational_level=user_level
        )

        print("\n" + "="*80)
        print("PROMPT GENERADO (Listo para enviar a la API de IA):")
        print("="*80)
        print(generated_prompt)
        print("="*80 + "\n")