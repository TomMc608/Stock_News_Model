import pandas as pd
import networkx as nx
import ast
import matplotlib.pyplot as plt
import time
from math import sqrt

# Load the data
start_time = time.time()
df = pd.read_csv('./Thematic Analysis/thematic_analysis_results.csv')

# Initialize an empty graph
G = nx.Graph()

# Function to add edges between all co-occurring entities
def add_edges(row):
    entities = ast.literal_eval(row['entities'])
    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            if G.has_edge(entities[i][1], entities[j][1]):
                G[entities[i][1]][entities[j][1]]['weight'] += 1
            else:
                G.add_edge(entities[i][1], entities[j][1], weight=1)

# Apply the function to each row in the dataframe
df.apply(add_edges, axis=1)

# Calculate time taken for processing
processing_time = time.time() - start_time
print(f"Network built in {processing_time:.2f} seconds.")

# Check if the graph has nodes to prevent division by zero
if len(G.nodes()) > 0:
    k_value = min(1.0 / sqrt(len(G.nodes())), 0.75)  # Adjust 0.75 as needed to bring nodes closer without overlap
    pos = nx.spring_layout(G, k=k_value, iterations=100)
else:
    pos = {}

# Node sizes and colors
node_degree = dict(G.degree())
node_size = [v * 50 for v in node_degree.values()]
node_color = [float(G.degree(node)) for node in G]

# Edges
edges = G.edges()
weights = [G[u][v]['weight'] for u,v in edges]

# Create figure with white background and larger size
plt.figure(figsize=(20, 20), facecolor='white')
plt.axis('off')
plt.title('Entity Co-occurrence Network')

# Draw the network
nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.viridis, alpha=0.6)
# Make edges more visible: brighter color and increased width
nx.draw_networkx_edges(G, pos, edgelist=edges, width=[w * 0.5 for w in weights], alpha=0.9, edge_color='blue')
# Increase font size for labels to make them readable
nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold', font_color='black')

# Set the edges of the figure to white
fig = plt.gcf()
fig.patch.set_facecolor('white')
ax = plt.gca()
ax.set_facecolor('white')

plt.show()
