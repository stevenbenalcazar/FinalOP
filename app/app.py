from flask import Flask, jsonify, render_template, request, send_from_directory
import numpy as np
from markupsafe import Markup
import markdown
from gpt.ModuloGpt import ModuloGpt
from transporte.TransporteSolver import solve_transportation_problem, vogel_approximation_method
from lineal.ResuelvePLineal import ResuelvePLineal  # ✅ Importación correcta
from redes.redes_api import redes_bp  # ✅ Importar API de redes
from inventario.inventario_api import inventario_bp  # ✅ Importar API de Inventario
import os

app = Flask(__name__)

# ✅ Registrar Blueprints
app.register_blueprint(redes_bp)  # ✅ Registra el Blueprint de redes
app.register_blueprint(inventario_bp)  # ✅ Registra el Blueprint de Inventario

# ✅ Servir imágenes en static/graphs/
@app.route('/static/graphs/<path:filename>')
def serve_graphs(filename):
    ruta_completa = os.path.join(app.static_folder, 'graphs', filename)
    print(f"🔍 Buscando imagen en: {ruta_completa}")  # ✅ Verifica la ruta en la consola
    return send_from_directory(os.path.join(app.static_folder, 'graphs'), filename)


@app.route('/redesb')
def redes():
    return render_template('redes.html')

@app.route('/inventario')  # ✅ Agregar ruta para Inventario
def inventario():
    return render_template('inventario.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/objective')
def objetivo():
    return render_template('objetivo.html')

@app.route('/plineal', methods=['GET', 'POST'])
def linear():
    resultado = None
    if request.method == 'POST':
        funcion_objetivo = request.form.get('funcion_objetivo')
        objetivo = request.form.get('objetivo')
        restricciones_raw = request.form.get('restriccion')
        metodo = request.form.get('metodo', 'simplex')  # ✅ Método por defecto es Simplex

        # ✅ Procesar y limpiar restricciones
        restricciones = [r.strip() for r in restricciones_raw.split('\n') if r.strip()]

        if not funcion_objetivo or not objetivo or not restricciones:
            return "Faltan datos en el formulario.", 400

        # ✅ Pasamos el método como keyword argument
        resultado = ResuelvePLineal.resolver_problema(
            funcion_objetivo, objetivo, restricciones, metodo=metodo
        )

        # ✅ Análisis con GPT y conversión a HTML
        analisi = ModuloGpt.interpretar_sensibilidad(resultado)
        analisis_html = Markup(markdown.markdown(analisi))

        if resultado:
            return render_template('resultado.html', resultado=resultado, analisi=analisis_html)

    return render_template('progra_lineal.html')


@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    if request.method == 'POST':
        try:
            data = request.json
            num_sources = int(data['numSources'])
            num_destinations = int(data['numDestinations'])
            supply = [int(data[f'supply{i}']) for i in range(num_sources)]
            demand = [int(data[f'demand{j}']) for j in range(num_destinations)]
            cost = [[int(data[f'cost{i}{j}']) for j in range(num_destinations)] for i in range(num_sources)]
            cost_matrix = np.array(cost, dtype=float)

            # ✅ Balanceo de oferta y demanda
            if sum(supply) != sum(demand):
                if sum(supply) > sum(demand):
                    demand.append(sum(supply) - sum(demand))
                    cost_matrix = np.hstack((cost_matrix, np.zeros((cost_matrix.shape[0], 1))))
                else:
                    supply.append(sum(demand) - sum(supply))
                    cost_matrix = np.vstack((cost_matrix, np.zeros((1, cost_matrix.shape[1]))))

            vogel_allocation = vogel_approximation_method(supply, demand, cost_matrix.tolist())
            vogel_cost = np.sum(vogel_allocation * cost_matrix)
            simplex_allocation, simplex_cost = solve_transportation_problem(supply, demand, cost_matrix.tolist())

            resultados = {
                'initial_matrix': cost_matrix.tolist(),
                'vogel': {'allocation': vogel_allocation.tolist(), 'cost': vogel_cost},
                'simplex': {'allocation': simplex_allocation, 'cost': simplex_cost}
            }

            # ✅ Análisis con GPT en transporte
            analisi = ModuloGpt.interpretar_transporte(resultados)
            analisis_html = Markup(markdown.markdown(analisi))  # ✅ Convertir a HTML

            return jsonify({
                'initial_matrix': cost_matrix.tolist(),
                'vogel': {'allocation': vogel_allocation.tolist(), 'cost': vogel_cost},
                'simplex': {'allocation': simplex_allocation, 'cost': simplex_cost},
                'analisis': analisis_html
            })
        except Exception as e:
            return jsonify({'error': str(e)})

    return render_template('transportation.html')


if __name__ == '__main__':
    app.run(debug=True)
