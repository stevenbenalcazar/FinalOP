import pulp
import re

class ResuelvePLineal:
    @staticmethod
    def resolver_problema(funcion_objetivo, objetivo, restricciones, metodo="simplex"):
        """
        Resuelve un problema de programación lineal con el método seleccionado.

        :param funcion_objetivo: String con la función objetivo.
        :param objetivo: "Maximizar" o "Minimizar".
        :param restricciones: Lista de strings con las restricciones.
        :param metodo: Método de solución ("simplex", "gran_m", "dos_fases").
        :return: Diccionario con los resultados.
        """
        variables = list(set(re.findall(r'[a-zA-Z]+', funcion_objetivo)))
        coeficientes = [int(coef) for coef in re.findall(r'[-+]?\d+', funcion_objetivo)]

        problema = pulp.LpProblem("Problema_de_Programacion_Lineal",
                                  pulp.LpMaximize if objetivo == "Maximizar" else pulp.LpMinimize)

        lp_variables = {var: pulp.LpVariable(var, lowBound=0) for var in variables}
        artificios = []
        fase_1 = False  # Para el método de Dos Fases
        M = 1e6  # Valor grande para Gran M

        # 📌 Definir función objetivo
        funcion_objetivo_expr = sum(coef * lp_variables[var] for coef, var in zip(coeficientes, variables))
        problema += funcion_objetivo_expr, "Funcion_Objetivo"

        # 📌 Procesar restricciones
        for i, restriccion in enumerate(restricciones):
            expr = re.sub(r'([a-zA-Z]+)', lambda m: f'lp_variables["{m.group(1)}"]', restriccion)
            nombre_restriccion = f"Restriccion_{i+1}"  # ✅ Nombre sin tilde ni espacios

            if '<=' in expr:
                lhs, rhs = expr.split('<=')
                problema += (eval(lhs.strip()) <= float(rhs.strip())), nombre_restriccion

            elif '>=' in expr:
                lhs, rhs = expr.split('>=')
                artificial = pulp.LpVariable(f'artificial_{i+1}', lowBound=0)
                artificios.append(artificial)

                if metodo == "gran_m":
                    problema += (eval(lhs.strip()) - artificial >= float(rhs.strip())), nombre_restriccion
                    problema.setObjective(funcion_objetivo_expr + M * artificial)

                elif metodo == "dos_fases":
                    fase_1 = True
                    problema += (eval(lhs.strip()) - artificial == float(rhs.strip())), nombre_restriccion

            elif '=' in expr:
                lhs, rhs = expr.split('=')
                artificial = pulp.LpVariable(f'artificial_{i+1}', lowBound=0)
                artificios.append(artificial)
                problema += (eval(lhs.strip()) + artificial == float(rhs.strip())), nombre_restriccion

                if metodo == "gran_m":
                    problema.setObjective(funcion_objetivo_expr + M * artificial)
                elif metodo == "dos_fases":
                    fase_1 = True
                    problema.setObjective(pulp.lpSum(artificios))  # Minimizar artificiales

            # 📌 Resolver Fase 1 en método Dos Fases
            if fase_1 and metodo == "dos_fases":
                problema.solve()
                if any(art.varValue > 0 for art in artificios):
                    return {"error": "El problema no tiene solución factible en la Fase 1"}

                # ✅ Reconfigurar problema sin artificiales
                problema = pulp.LpProblem("Fase_2_Programacion_Lineal",
                                        pulp.LpMaximize if objetivo == "Maximizar" else pulp.LpMinimize)
                problema += funcion_objetivo_expr, "Funcion_Objetivo"

                # 🔹 Volver a agregar las restricciones sin artificiales
                for i, restriccion in enumerate(restricciones):
                    expr = re.sub(r'([a-zA-Z]+)', lambda m: f'lp_variables["{m.group(1)}"]', restriccion)
                    nombre_restriccion = f"Restriccion_{i+1}"
                    
                    if '<=' in expr:
                        lhs, rhs = expr.split('<=')
                        problema += (eval(lhs.strip()) <= float(rhs.strip())), nombre_restriccion
                    elif '>=' in expr:
                        lhs, rhs = expr.split('>=')
                        problema += (eval(lhs.strip()) >= float(rhs.strip())), nombre_restriccion
                    elif '=' in expr:
                        lhs, rhs = expr.split('=')
                        problema += (eval(lhs.strip()) == float(rhs.strip())), nombre_restriccion
           
            # Asegurar que "Función" esté presente
                if "Función" not in resultado:
                    resultado["Función"] = funcion_objetivo


        # 📌 Resolver el problema
        problema.solve()

        # 📌 Construcción del resultado
        resultado = {
        "Metodo": metodo,
        "Objetivo": objetivo,
        "Función": funcion_objetivo,  # 🔹 Asegurar que "Función" esté presente
        "Variables": {var: var_value.varValue for var, var_value in lp_variables.items()},
        "Coeficientes": coeficientes,
        "Restricciones": restricciones,
        "Valor_Objetivo": pulp.value(problema.objective) if problema.objective else None,
        "Holguras": {nombre: restriccion.slack for nombre, restriccion in problema.constraints.items()} if problema.constraints else {},
        "Artificios": {f"artificial_{i+1}": art.varValue for i, art in enumerate(artificios)} if artificios else {},
        "Costo_Reducido": {var: var_value.dj for var, var_value in lp_variables.items()} if lp_variables else {},
        "Precios_Duales": {nombre: restriccion.pi for nombre, restriccion in problema.constraints.items()} if problema.constraints else {}
    }


        return resultado

# ✅ Pruebas rápidas
if __name__ == "_main_":
    funcion_objetivo = "3*x + 4*y"
    objetivo = "Maximizar"
    restricciones = ["2*x + y <= 5", "x + 2*y >= 6", "x + y = 3"]

    print("\n🔹 Método Simplex")
    print(ResuelvePLineal.resolver_problema(funcion_objetivo, objetivo, restricciones, metodo="simplex"))

    print("\n🔹 Método Gran M")
    print(ResuelvePLineal.resolver_problema(funcion_objetivo, objetivo, restricciones, metodo="gran_m"))

    print("\n🔹 Método Dos Fases")
    print(ResuelvePLineal.resolver_problema(funcion_objetivo, objetivo, restricciones, metodo="dos_fases"))