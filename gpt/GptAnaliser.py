import openai
from dotenv import load_dotenv
import os

class GptAnaliser:
    @staticmethod
    def interpretar_sensibilidad(resultados):
        """
        Obeten, analiza e interpreta los resultados de sensibilidad.

        :param resultados: Diccionario con los resultados del problema resuelto.
        :return: Interpretación detallada del análisis de sensibilidad en formato legible.
        """
        # Configurar la clave de API de OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Construir el prompt para GPT
        prompt = (
            f"Se presenta un problema de programación lineal resuelto. Analiza los resultados obtenidos en {resultados['Función']} "
            f"Además, realiza un análisis de sensibilidad"
            "Genera un análisis de sensibilidad en formato Markdown. "
            "Usa formato Markdown con títulos (`###`), listas (`-`), y negritas (`**`), pero **no uses LaTeX ni signos de dólar (`$`).**"
            "Explica todo de manera clara y en lenguaje natural."
            
            "### Análisis de Sensibilidad ###\n"
            "1. **Impacto de Cambios en los Coeficientes:**\n"
            "   - ¿Cómo afectaría a la solución óptima un aumento o disminución en los coeficientes de la función objetivo?\n"
            "   - Considera si las variables actuales cambiarían de valor o si el óptimo seguiría siendo el mismo.\n\n"
            
            "2. **Modificaciones en las Restricciones:**\n"
            "   - Evalúa cómo una relajación o endurecimiento de las restricciones afectaría las variables óptimas y la función objetivo.\n"
            "   - ¿Existen restricciones que limitan más la solución?\n\n"

            "3. **Interpretación de Holguras y Variables de Artificio:**\n"
            "   - Explica cómo las holguras afectan la solución y si hay restricciones que están activas en el óptimo.\n"
            "   - ¿Las variables de artificio están indicando que el problema es factible o hubo que forzar soluciones?\n\n"

            "4. **Conclusión y Recomendaciones:**\n"
            "   - Resume el análisis basado en los datos presentados.\n"
            "   - Da una interpretación clara y estructurada del comportamiento del problema y posibles ajustes.\n"
        )

        # Realizar la solicitud a OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Eres un asistente experto en programación lineal y análisis de sensibilidad."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=450
        )

        # Obtener la respuesta
        informacion = response.choices[0]['message']['content'].strip()
        return informacion

