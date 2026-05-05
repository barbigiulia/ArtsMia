from model.model import Model

model = Model()  # istanza del modello

model.buildGraph()
print(f"Grafo che contiene {model.getNumNodes()} nodi e {model.getNumEdges()} archi")



model.getInfoConnessa(1224)