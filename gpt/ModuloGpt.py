import openai
from dotenv import load_dotenv
import os

class ModuloGpt:
    
    # ✅ PLANTEAMIENTO DEL PROBLEMA (Se agregará en cada prompt)
    PLANTEAMIENTO_PROBLEMA = """
    Exi'Models es una empresa dedicada a la fabricación de sillas de alta calidad. 
    La empresa enfrenta desafíos en la optimización de producción, distribución eficiente de productos y costos logísticos.
    Para mejorar la toma de decisiones, se ha diseñado un modelo basado en Programación Lineal, Transporte y Redes.
    """
    
    @staticmethod
    def interpretar_sensibilidad(resultados):
        """
        Analiza los resultados de Programación Lineal incluyendo análisis de sensibilidad.
        """
        openai.api_key = os.getenv('OPENAI_API_KEY')

        prompt = (
            f"{ModuloGpt.PLANTEAMIENTO_PROBLEMA}\n\n"
            "### Análisis de Programación Lineal ###\n"
            "Se ha resuelto un problema de optimización de producción en Exi'Models.\n"
            f"- **Función Objetivo:** {resultados['Función']}\n"
            f"- **Variables de decisión:** {resultados['Variables']}\n"
            f"- **Restricciones:** {resultados['Restricciones']}\n"
            f"- **Valor Óptimo:** {resultados['Valor_Objetivo']}\n\n"
            "### Análisis de Sensibilidad ###\n"
            "1. **Impacto de cambios en los coeficientes:**\n"
            "   - ¿Cómo afectaría a la solución un cambio en la producción de sillas estándar o de lujo?\n"
            "   - ¿Podría Exi'Models ajustar la producción para mejorar la rentabilidad?\n\n"
            "2. **Modificaciones en las restricciones:**\n"
            "   - ¿Qué pasaría si se aumenta el límite de tiempo de producción?\n"
            "   - ¿Sería posible producir más sin generar costos excesivos?\n\n"
            "### Conclusión ###\n"
            "Explica si la solución es óptima y qué recomendaciones harías para mejorar la estrategia de producción."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Eres un asistente experto en optimización de producción y análisis de sensibilidad."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=450
        )

        return response.choices[0]['message']['content'].strip()


    @staticmethod
    def interpretar_transporte(resultados):
        """
        Analiza e interpreta los resultados del problema de transporte en Exi'Models.
        """
        openai.api_key = os.getenv('OPENAI_API_KEY')

        prompt = (
            f"{ModuloGpt.PLANTEAMIENTO_PROBLEMA}\n\n"
            "### Análisis del Problema de Transporte ###\n"
            "Se ha resuelto un problema de distribución de productos en Exi'Models.\n"
            f"- **Matriz de costos inicial:**\n{resultados['initial_matrix']}\n\n"
            f"- **Método de Vogel:**\n{resultados['vogel']['allocation']}\n"
            f"  - **Costo Total:** {resultados['vogel']['cost']}\n\n"
            f"- **Método Simplex:**\n{resultados['simplex']['allocation']}\n"
            f"  - **Costo Total:** {resultados['simplex']['cost']}\n\n"
            "### Preguntas de Análisis ###\n"
            "1. **Comparación entre métodos:**\n"
            "   - ¿Cuál de los métodos genera un menor costo de transporte?\n"
            "   - ¿El método de Vogel es suficiente o se requiere una solución más refinada con Simplex?\n\n"
            "2. **Impacto en costos:**\n"
            "   - ¿Cómo afecta el costo de transporte la rentabilidad de Exi'Models?\n"
            "   - ¿Podrían optimizarse mejor los envíos?\n\n"
            "### Conclusión ###\n"
            "Proporciona una interpretación detallada de la asignación de recursos y posibles mejoras en la logística."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Eres un experto en optimización de transporte y logística empresarial."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=450
        )

        return response.choices[0]['message']['content'].strip()

    
    @staticmethod
    def interpretar_redes(resultados):
        """
        Analiza e interpreta los resultados de optimización de rutas de distribución en Exi'Models.
        """
        openai.api_key = os.getenv('OPENAI_API_KEY')

        prompt = (
            f"{ModuloGpt.PLANTEAMIENTO_PROBLEMA}\n\n"
            "### Análisis de Redes ###\n"
            "Se ha calculado una solución de optimización de rutas en Exi'Models.\n"
        )

        if "flow_value" in resultados:
            prompt += (
                f"- **Flujo máximo encontrado:** {resultados['flow_value']}\n"
                f"- **Detalle del flujo:** {resultados['flow_dict']}\n\n"
                "### Preguntas de Análisis ###\n"
                "- ¿Cuáles son los cuellos de botella en la red de distribución?\n"
                "- ¿Podrían aumentarse los envíos sin afectar la logística?\n\n"
            )
        elif "path" in resultados:
            prompt += (
                f"- **Ruta mínima encontrada:** {resultados['path']}\n"
                f"- **Longitud total:** {resultados['length']}\n\n"
                "### Preguntas de Análisis ###\n"
                "- ¿Existen rutas alternativas eficientes?\n"
                "- ¿Cómo mejorar la conectividad entre tiendas segun el planteamiento de este problema y las respuestas?\n\n"
            )
        elif "mst_edges" in resultados:
            prompt += (
                f"- **Árbol de Expansión Mínima encontrado:** {resultados['mst_edges']}\n\n"
                "### Preguntas de Análisis ###\n"
                "- ¿Se minimizó correctamente el costo de conexión entre tiendas?\n"
                "- ¿Podrían reducirse aún más los costos logísticos?\n\n"
            )

        prompt += "### Conclusión ###\nExplica si la solución es óptima y cómo podría mejorarse."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Eres un experto en teoría de grafos y optimización de redes de distribución."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=450
        )

        return response.choices[0]['message']['content'].strip()