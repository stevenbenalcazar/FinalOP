import pulp
import re

class LinearProgrammingSolver:
    @staticmethod
    def resolver_problema(funcion_objetivo, objetivo, restricciones):
        variables = list(set(re.findall(r'[a-zA-Z]+', funcion_objetivo)))
        
        # Extrae los coeficientes numéricos de la función objetivo con expresiones regulares
        coeficientes = [int(coef) for coef in re.findall(r'[-+]?\d+', funcion_objetivo)]
        
        # Se precesa si es Maximizar o Minimizar
        problema = pulp.LpProblem("Problema_de_Programacion_Lineal",
        pulp.LpMaximize if objetivo == "Maximizar" else pulp.LpMinimize)

        lp_variables = {var: pulp.LpVariable(var, lowBound=0) for var in variables}
        artificios = []
        # Construye la función objetivo en PuLP y la asigna al problema
        funcion_objetivo_expr = sum(coef * lp_variables[var] for coef, var in zip(coeficientes, variables))
        problema += funcion_objetivo_expr, "Función Objetivo"

        M = 1e6
        
        # Se procesan las restricciones 
        for i, restriccion in enumerate(restricciones):
            expr = restriccion
            expr = re.sub(r'([a-zA-Z]+)', lambda m: f'lp_variables["{m.group(1)}"]', expr)

            if '<=' in expr:
                lhs, rhs = expr.split('<=')
                rhs = float(rhs.strip())
                lhs = lhs.strip()
                problema += (eval(lhs) <= rhs), f"Restricción_{i+1}"

            elif '>=' in expr:
                lhs, rhs = expr.split('>=')
                rhs = float(rhs.strip())
                lhs = lhs.strip()
                artificial = pulp.LpVariable(f'artificial_{i+1}', lowBound=0)
                artificios.append(artificial)
                problema += (eval(lhs) - artificial >= rhs), f"Restricción_{i+1}"
                problema.setObjective(funcion_objetivo_expr + M * artificial)

            elif '=' in expr:
                lhs, rhs = expr.split('=')
                rhs = float(rhs.strip())
                lhs = lhs.strip()
                artificial = pulp.LpVariable(f'artificial_{i+1}', lowBound=0)
                artificios.append(artificial)
                problema += (eval(lhs) + artificial == rhs), f"Restricción_{i+1}"
                problema.setObjective(funcion_objetivo_expr + M * artificial)
                
        # Resuelve el problema con el solve interno de PuLP
        problema.solve()

        resultado = {
            "Objetivo": objetivo, # Almacena si es Maximizar o Minimizar
            "Función": funcion_objetivo, # Guarda la función objetivo en formato de string
            "Variables": {var: var_value.varValue for var, var_value in lp_variables.items()}, # Valores óptimos de las variables
            "Coeficientes": coeficientes, # Lista de coeficientes extraídos de la función objetivo
            "Restricciones": restricciones, # Lista de restricciones ingresadas por el usuario
            "Valor_Objetivo": pulp.value(problema.objective), # Valor óptimo de la función objetivo después de resolver
            "Holguras": {f"Restricción_{i+1}": max(0, problema.constraints[f"Restricción_{i+1}"].slack) for i in range(len(restricciones))}, # Espacio libre en restricciones
            "Artificios": {f"artificial_{i+1}": artificio.varValue for i, artificio in enumerate(artificios)}, # Variables artificiales usadas
            "Costo_Reducido": {var: var_value.dj for var, var_value in lp_variables.items()}, # Costo reducido de cada variable
            "Precios_Duales": {f"Restricción_{i+1}": problema.constraints[f"Restricción_{i+1}"].pi for i in range(len(restricciones))} # Multiplicadores de Lagrange
        }
        return resultado

# Hacia abajo son pruebas y depuracion que se imprimen en terminal
if __name__ == "__main__":
    funcion_objetivo = "3*x + 4*y"
    objetivo = "Maximizar"
    restricciones = [
        "2*x + y <= 5",
        "x + 2*y >= 6",
        "x + y = 3"
    ]

    resultado = LinearProgrammingSolver.resolver_problema(funcion_objetivo, objetivo, restricciones)

    print("Resultados del Problema de Programación Lineal:")
    print(f"Función Objetivo: {resultado['Función']}")
    print(f"Tipo de Objetivo: {resultado['Objetivo']}")
    print(f"Variables y Valores: {resultado['Variables']}")
    print(f"Coeficientes: {resultado['Coeficientes']}")
    print(f"Restricciones: {resultado['Restricciones']}")
    print(f"Valor de la Función Objetivo: {resultado['Valor_Objetivo']}")
    print(f"Holguras: {resultado['Holguras']}")
    print(f"Artificios: {resultado['Artificios']}")
    print(f"Costo Reducido: {resultado['Costo_Reducido']}")
    print(f"Precios Dual: {resultado['Precios_Duales']}")