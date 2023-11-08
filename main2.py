import networkx as nx
import random
import matplotlib.pyplot as plt

# Function to generate random labels for nodes
def generate_label():
    land_use = random.choice(['Residential', 'Commercial', 'Industrial'])
    density = random.choice(['High', 'Low'])
    surface = random.choice(['Paved', 'Unpaved'])
    elevation = random.choice(['High', 'Low'])
    green_cover = random.choice(['High', 'Low'])
    accessibility = random.choice(['High', 'Low'])
    pollution_level = random.choice(['High', 'Low'])
    traffic = random.choice(['High', 'Low'])
    public_transport = random.choice(['Good', 'Poor'])
    walkability = random.choice(['High', 'Low'])
    crime_rate = random.choice(['High', 'Low'])
    amenities = random.choice(['Ample', 'Scarce'])
    land_value = random.choice(['High', 'Low'])
    
    return f"{land_use}, {density}, {surface}, {elevation}, {green_cover}, {accessibility}, {pollution_level}, {traffic}, {public_transport}, {walkability}, {crime_rate}, {amenities}, {land_value}"

# Initialize the graph
G = nx.Graph()

# Create a fully connected graph with initial nodes
initial_nodes = [1, 2, 3]
G = nx.complete_graph(initial_nodes)

# Label initial nodes
labels = {node: generate_label() for node in G.nodes()}

# Add 10 more nodes and make sure they are fully interconnected
for i in range(4, 14):
    G.add_node(i)
    for j in range(1, i):
        G.add_edge(i, j)
    labels[i] = generate_label()

# Draw the graph
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='skyblue', font_weight='bold', node_size=700, font_size=18)
plt.show()

# Show labels for all nodes
labels
