import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import networkx as nx
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

# Function to update and display parameters
def update_parameters():
    current_parameters = parameter_entry.get()
    parameter_display.config(text=f"Current Parameters: {current_parameters}")

# Function to update the graph (similar to previous examples)
# Function to update the graph (similar to previous examples)
def update(frame, graph, pos, ax, parameters, weights):
    ax.clear()
    ax.axis('off')
    
    # Randomly move nodes for animation
    for node in pos:
        pos[node] = (pos[node][0] + np.random.uniform(-0.05, 0.05), pos[node][1] + np.random.uniform(-0.05, 0.05))
    
    # Adjust node sizes based on their weights
    node_sizes = [weights[parameters[node % len(parameters)]] * 50 for node in graph.nodes()]
    
    # Redraw the graph
    nx.draw(graph, pos=pos, ax=ax, node_size=node_sizes, edge_color='gray')
    
    # Add labels for nodes with urban parameters
    label_dict = {node: parameters[node % len(parameters)] for node in graph.nodes()}
    nx.draw_networkx_labels(graph, pos, labels=label_dict, font_size=6, ax=ax)
    
    ax.set_title(f'Network Growth Model: Frame {frame}')

# Function to perform preferential attachment
def preferential_attachment(graph, new_nodes, m):
    for i in range(new_nodes):
        new_node = max(graph.nodes()) + 1
        degrees = np.array([d for n, d in graph.degree()])
        probabilities = degrees / np.sum(degrees)
        neighbors = np.random.choice(graph.nodes(), size=m, p=probabilities)
        for neighbor in neighbors:
            graph.add_edge(new_node, neighbor)


# Function to start the animation
def start_animation():
    # Get the parameters and weights from Tkinter entries
    parameters = parameter_entry.get().split(',')
    weight_value = weight_slider.get()  # Getting value from slider
    weights = [weight_value] * len(parameters)  # Assuming the same weight for all parameters for simplicity
    frames = int(frame_entry.get())
    
    # Create a dictionary of weights for easier lookup
    weight_dict = {param: weight for param, weight in zip(parameters, weights)}
    
    # Initialize a fully connected graph based on user input
    graph = nx.Graph()
    graph.add_nodes_from(range(len(parameters)))
    for i, node1 in enumerate(graph.nodes()):
        for node2 in graph.nodes()[i+1:]:
            graph.add_edge(node1, node2)
            
    # Initial position of nodes
    pos = nx.spring_layout(graph, seed=42)
    
    # Start the animation
    ani = FuncAnimation(fig, update, frames=frames, fargs=(graph, pos, ax, parameters, weight_dict))
    canvas.draw()

# Create the main window
root = tk.Tk()

# Add labels and text boxes for parameters
parameter_label = tk.Label(root, text="Parameters:")
parameter_label.pack()
parameter_entry = tk.Entry(root)
parameter_entry.pack()

# Button to update and display parameters
update_button = tk.Button(root, text="Update Parameters", command=update_parameters)
update_button.pack()

# Label to display current parameters
parameter_display = tk.Label(root, text="Current Parameters: None")
parameter_display.pack()

# Add labels and slider for weights
weight_label = tk.Label(root, text="Weights:")
weight_label.pack()
weight_slider = tk.Scale(root, from_=1, to=10, orient='horizontal')
weight_slider.pack()

# Add labels and text boxes for frames
frame_label = tk.Label(root, text="Frames:")
frame_label.pack()
frame_entry = tk.Entry(root)
frame_entry.pack()

# Add start button
start_button = tk.Button(root, text="Start", command=start_animation)
start_button.pack()
# Create a Matplotlib figure and a canvas
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Pack all the widgets and start the Tkinter event loop
parameter_entry.pack()
weight_slider.pack()
frame_entry.pack()
start_button.pack()
canvas.get_tk_widget().pack()
root.mainloop()
