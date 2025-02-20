from flask import Blueprint, request, render_template
import networkx as nx
import matplotlib.pyplot as plt
import os
from redes.network_solver import max_flow
from datetime import datetime
from gpt.GptAnaliser import GptAnaliser  # ✅ Importamos la IA
from markupsafe import Markup
import markdown

redes_bp = Blueprint('redes', __name__)

def generar_grafico(G, resultado, operation):
    """ Genera el gráfico resaltando la ruta calculada """
    img_path = os.path.join("app", "static", "graphs", "network.png")
    os.makedirs(os.path.dirname(img_path), exist_ok=True)
    plt.figure(figsize=(6, 6))
    pos = nx.spring_layout(G)
    
    # Dibujar el grafo base
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    # Resaltar el camino encontrado
    if operation == "shortest_path" and 'path' in resultado:
        path_edges = list(zip(resultado['path'], resultado['path'][1:]))
        nx.draw(G, pos, edgelist=path_edges, edge_color='red', width=2)
    elif operation == "max_flow" and 'flow_dict' in resultado:
        flow_edges = [(u, v) for u in resultado['flow_dict'] for v in resultado['flow_dict'][u] if resultado['flow_dict'][u][v] > 0]
        nx.draw(G, pos, edgelist=flow_edges, edge_color='blue', width=2)
    elif operation == "mst" and 'mst_edges' in resultado:
        mst_edges = [(u, v) for u, v, _ in resultado['mst_edges']]
        nx.draw(G, pos, edgelist=mst_edges, edge_color='green', width=2)
    
    plt.savefig(img_path)
    plt.close()

@redes_bp.route('/redesb', methods=['GET', 'POST'])
def redes():
    if request.method == 'POST':
        nodes = request.form.get('nodes')
        edges = request.form.get('edges')
        source = request.form.get('source')
        sink = request.form.get('sink')
        operation = request.form.get('operation')
        
        G = nx.DiGraph() if operation == "max_flow" else nx.Graph()
        node_list = [n.strip() for n in nodes.split(",")]
        G.add_nodes_from(node_list)
        
        for edge in edges.split(";"):
            try:
                n1, n2, weight = edge.split(",")
                G.add_edge(n1.strip(), n2.strip(), weight=int(weight.strip()))
            except ValueError:
                return "Error en el formato de conexiones.", 400
        
        if operation == "max_flow":
            resultado = max_flow(nodes, edges, source, sink)
        elif operation == "shortest_path":
            try:
                path = nx.shortest_path(G, source=source, target=sink, weight="weight")
                length = nx.shortest_path_length(G, source=source, target=sink, weight="weight")
                resultado = {"path": path, "length": length}
            except nx.NetworkXNoPath:
                resultado = {"error": "No hay camino entre los nodos seleccionados."}
        elif operation == "mst":
            mst = nx.minimum_spanning_tree(G, weight="weight")
            resultado = {"mst_edges": list(mst.edges(data=True))}
        else:
            return "Operación no válida", 400
        
        generar_grafico(G, resultado, operation)
        
        
        analisis_ia = GptAnaliser.interpretar_redes(resultado)  # ✅ Generar análisis con OpenAI
        analisis_html = Markup(markdown.markdown(analisis_ia))  # ✅ Convertir a HTML para la interfaz
        return render_template("resultado_redes.html", resultado=resultado, analisis=analisis_html, now=datetime.now())
    
    return render_template('redes.html')
