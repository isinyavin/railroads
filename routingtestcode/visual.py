import matplotlib.pyplot as plt
import networkx as nx
import pickle

pickle_file_path = 'railway_network.pkl'

with open(pickle_file_path, 'rb') as file:
    G  = pickle.load(file)

import networkx as nx


print(G)

#pos = nx.get_node_attributes(G, 'pos') if nx.get_node_attributes(G, 'pos') else None
#nx.draw(G, pos=pos, with_labels=True, node_size=50)
#plt.show()

twos = 0
ones = 0 
for node, degree in G.degree():
    if degree == 2:
        twos += 1
    if degree == 1:
       ones += 1

print(twos)
print(ones)

node_name = "Port Talbot Parkway"


nodes_with_name = [node for node, data in G.nodes(data=True) if data.get('name') == node_name]
print(nodes_with_name)


for node_id in nodes_with_name:
    neighbors = list(G.neighbors(node_id))
    print(f"Adjacent nodes to '{node_name}' (Node ID: {node_id}): {neighbors}")

