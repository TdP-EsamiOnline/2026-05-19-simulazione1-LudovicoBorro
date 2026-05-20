from model.model import Model

model = Model()
model.build_graph(1) # Passo un genre id, perchè nel controller ho gli oggetti genre
num_nodes, num_edges = model.getGraphDetails()
print("Grafo correttamente creato!")
print(f"Il grafo ha {num_nodes} nodi e {num_edges} archi.")

bestPath, bestScore = model.getPath(model.getRandomNode())
print(f"Trovato un cammino di lunghezza {len(bestPath)}")
for p in bestPath:
    print(p)