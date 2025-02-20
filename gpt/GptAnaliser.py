import openai
from dotenv import load_dotenv
import os

class GptAnaliser:
    @staticmethod
    def interpretar_sensibilidad(resultados):
        
        # Configurar la clave de API de OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Construir el prompt para GPT
        prompt = (
            f"Se presenta un problema de programación lineal resuelto. Analiza los resultados obtenidos en {resultados['Función']} "
            f"Además, realiza un análisis de sensibilidad"
            "Genera un análisis de sensibilidad en formato Markdown. "
            "Usa formato Markdown con títulos (`###`), listas (`-`), y negritas (`**`), pero **no uses LaTeX ni signos como este de dinero (`$`).**"
            "Por favor explica todo de manera clara y en lenguaje natural."
            
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
    
    
    @staticmethod
    def interpretar_transporte(resultados):
        """
        Analiza e interpreta los resultados del problema de transporte.
        """
        openai.api_key = os.getenv('OPENAI_API_KEY')

        prompt = (
            "Se presenta un problema de transporte resuelto mediante métodos de optimización.\n\n"
            "### Datos del Problema ###\n"
            f"- **Matriz de costos inicial:**\n{resultados['initial_matrix']}\n\n"
            f"- **Solución del Método de Vogel:**\n{resultados['vogel']['allocation']}\n"
            f"  - **Costo Total:** {resultados['vogel']['cost']}\n\n"
            f"- **Solución del Método Simplex:**\n{resultados['simplex']['allocation']}\n"
            f"  - **Costo Total:** {resultados['simplex']['cost']}\n\n"
            
            "### Análisis del Problema de Transporte ###\n"
            "1. **Comparación entre Métodos:**\n"
            "   - ¿Cuál de los métodos genera una mejor asignación?\n"
            "   - ¿El método de Vogel es suficiente o se necesita refinar la solución con Simplex?\n\n"
            
            "2. **Impacto en Costos:**\n"
            "   - ¿Qué tanto difiere el costo entre los métodos?\n"
            "   - ¿Se logró optimizar al máximo la asignación de recursos?\n\n"

            "3. **Posibles Mejoras:**\n"
            "   - ¿Qué ajustes se podrían hacer en la asignación de recursos?\n"
            "   - ¿Qué restricciones o condiciones adicionales podrían mejorar la solución?\n\n"

            "### Conclusión ###\n"
            "Proporciona un análisis detallado de los resultados obtenidos y si la asignación de recursos es óptima.\n"
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Eres un asistente experto en optimización de transporte y análisis de costos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=450
        )

        return response.choices[0]['message']['content'].strip()

    @staticmethod
    def interpretar_redes(resultados):
        """
        Analiza e interpreta los resultados del problema de redes.
        """
        openai.api_key = os.getenv('OPENAI_API_KEY')

        # Construir el prompt dinámico dependiendo del tipo de operación realizada
        if "flow_value" in resultados:
            prompt = (
                "Se ha resuelto un problema de flujo máximo en una red.\n\n"
                f"- **Valor del flujo máximo:** {resultados['flow_value']}\n"
                f"- **Detalle del flujo:** {resultados['flow_dict']}\n\n"
                "### Análisis del Flujo Máximo ###\n"
                "- ¿Cuáles son los cuellos de botella en la red?\n"
                "- ¿Cómo se podría mejorar la capacidad de flujo?\n"
                "- ¿Existe algún camino que no se está utilizando de manera eficiente?\n\n"
                "### Conclusión ###\n"
                "Proporciona un análisis detallado de los resultados obtenidos y posibles mejoras."
            )
        elif "path" in resultados:
            prompt = (
                "Se ha calculado la ruta más corta entre dos nodos en una red.\n\n"
                f"- **Ruta encontrada:** {resultados['path']}\n"
                f"- **Longitud total:** {resultados['length']}\n\n"
                "### Análisis de la Ruta Mínima ###\n"
                "- ¿Existen otras rutas con un costo similar?\n"
                "- ¿Cómo se podría mejorar la conectividad en la red?\n"
                "- ¿La ruta mínima encontrada es eficiente en términos de balance de carga?\n\n"
                "### Conclusión ###\n"
                "Explica si la solución es óptima y cómo se podría optimizar aún más."
            )
        elif "mst_edges" in resultados:
            prompt = (
                "Se ha calculado el Árbol de Expansión Mínima (MST) de una red.\n\n"
                f"- **Aristas del MST:** {resultados['mst_edges']}\n\n"
                "### Análisis del Árbol de Expansión Mínima ###\n"
                "- ¿El MST encontrado minimiza el costo total de conexión?\n"
                "- ¿Existen otras formas de estructurar la red con menor costo?\n"
                "- ¿Es posible eliminar nodos sin afectar la conectividad?\n\n"
                "### Conclusión ###\n"
                "Analiza si el MST es óptimo y si hay estrategias para reducir aún más los costos."
            )
        else:
            prompt = "No se pudo generar un análisis debido a un error en los datos."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Eres un experto en optimización de redes y teoría de grafos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=450
        )

        return response.choices[0]['message']['content'].strip()
