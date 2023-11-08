import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def generate_label():
    parameters = ['Residential', 'Commercial', 'Industrial', 'High', 'Low', 'Paved', 'Unpaved', 'High', 'Low',
                  'High', 'Low', 'High', 'Low', 'High', 'Low', 'Good', 'Poor', 'High', 'Low', 'High', 'Low',
                  'Ample', 'Scarce', 'High', 'Low']
    return ', '.join(random.choices(parameters, k=13))

def generate_graph():
    G = nx.complete_graph(initial_nodes)
    labels = {node: generate_label() for node in G.nodes()}
    
    for i in range(4, 14):
        G.add_node(i)
        for j in range(1, i):
            G.add_edge(i, j)
        labels[i] = generate_label()
    
    pos = nx.spring_layout(G, seed=42)
    
    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, node_color='skyblue', font_weight='bold', node_size=700, font_size=18, ax=ax)
    
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    text_area.delete(1.0, tk.END)
    for node, label in labels.items():
        text_area.insert(tk.END, f"Node {node}: {label}\n")

# Initialize Tkinter window
window = tk.Tk()
window.title("Network Growth Model")

# Add a button to generate the graph
generate_button = ttk.Button(window, text="Generate Network", command=generate_graph)
generate_button.pack(side=tk.TOP)

# Add a scrolled text area to display labels
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=20)
text_area.pack(side=tk.BOTTOM)

# Initialize initial nodes and labels
initial_nodes = [1, 2, 3]

# Start Tkinter event loop
window.mainloop()
