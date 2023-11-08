import tkinter as tk
from tkinter import ttk, Checkbutton, Button, Toplevel, IntVar, StringVar, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
import random
import time
from tree import TreeGenerator

# Global variables
G = None
pos = None
labels = None
node_sizes = None
ani = None  # Initialize ani as None
show_labels = True  # Declare as a global variable at the top of your script
param_entries = []
param_scales = []
param_comboboxes = []
param_connections = [{} for _ in range(20)] 
num_nodes = 0
node_colors = []



predefined_params = ['Land Use', 'Health', 'Density', 'Transport', 'Green Space', 
                     'Housing', 'Employment', 'Education', 'Safety', 'Air Quality',
                     'Noise', 'Water Quality', 'Energy', 'Waste Management', 'Local Amenities',
                     'Cultural Assets', 'Tourism', 'Social Cohesion', 'Innovation', 'Governance']

all_params = [
    # 15-minute city parameters
    'Public Transport Accessibility', 'Essential Services Density', 'Active Mobility Infrastructure', 
    'Green Space Proximity', 'Local Job Opportunities', 'Housing Affordability', 
    'Air Quality Index', 'Noise Pollution Levels', 'Public Safety', 
    'Cultural Facilities Density', 'Local Food Availability', 'Water Quality',
    'Waste Management Efficiency', 'Energy Sustainability', 'Community Spaces',
    
    # Weather parameters
    'Temperature', 'Humidity', 'Wind Speed', 'Barometric Pressure',
    'Solar Radiation', 'Cloud Cover', 'Rainfall', 'Snowfall', 
    'Fog Presence', 'Hail Presence', 'Thunderstorm Index', 'Drought Index', 
    'Heatwave Index', 'Cold Fronts', 'Tornado Risk',
    
    # Nature parameters
    'Biodiversity Index', 'Tree Canopy Cover', 'Presence of Water Bodies', 
    'Soil Quality', 'Bird Species Diversity', 'Fish Species Diversity', 
    'Mammal Species Diversity', 'Plant Species Diversity', 'Protected Areas',
    'Ecosystem Services', 'Invasive Species', 'Natural Resource Depletion',
    'Conservation Efforts', 'Wildlife Habitats', 'Floral Density',
    
    # UN-Habitat and United Nations parameters
    'Social Inclusion Index', 'Gender Equality Measures', 'Unemployment Rate', 
    'Education Accessibility', 'Healthcare Accessibility', 'Life Expectancy', 
    'Child Mortality Rate', 'Access to Clean Water', 'Access to Sanitation', 
    'Poverty Rate', 'Income Inequality', 'Literacy Rate',
    'Digital Inclusion', 'Legal Aid Accessibility', 'Crime Rate', 
    
    # Additional Urbanism and Architecture parameters
    'Architectural Diversity', 'Historic Sites', 'Zoning Regulations', 
    'Land Use Mix', 'Urban Sprawl Index', 'Walkability', 
    'Cycling Infrastructure', 'Traffic Congestion', 'Parking Availability', 
    'Public Transport Frequency', 'Road Quality', 'Bridge Integrity',
    'Building Code Adherence', 'Urban Design Quality', 'Public Art Installations',
    
    # Additional Environmental parameters
    'Carbon Footprint', 'Recycling Rates', 'Composting Rates', 
    'Renewable Energy Use', 'Fossil Fuel Dependency', 'Water Use Per Capita', 
    'Air Pollutants', 'Chemical Waste', 'Oceanic Pollution',
    'River Health', 'Mountain Ecosystems', 'Desert Ecosystems', 
    'Forest Ecosystems', 'Grassland Ecosystems', 'Wetland Ecosystems',
    
    # Social and Economic parameters
    'Civic Engagement', 'Political Stability', 'Corruption Index',
    'Market Diversity', 'Economic Growth Rate', 'Inflation Rate',
    'Interest Rates', 'Stock Market Performance', 'Foreign Investment',
    'Tourism Rates', 'Cultural Diversity', 'Immigration Rates', 
    'Emigration Rates', 'Religious Freedom', 'Press Freedom',
    
    # Health parameters
    'Nutrition Levels', 'Obesity Rates', 'Physical Activity Levels',
    'Smoking Rates', 'Alcohol Consumption', 'Substance Abuse Rates',
    'Mental Health Support', 'Psychiatric Care Availability', 'Ambulance Response Times',
    'Emergency Room Efficiency', 'Specialized Medical Services', 'Disease Control',
    'Vaccination Rates', 'Public Health Campaigns', 'Average Sleep Duration',
    
    # Technology and Innovation parameters
    'Internet Speed', 'Mobile Network Coverage', '5G Availability',
    'Tech Startups Density', 'R&D Investment', 'Patent Applications',
    'Tech Talent Pool', 'University-Industry Collaboration', 'Innovation Index',
    'Smart City Initiatives', 'Data Privacy Regulations', 'Cybersecurity Measures',
    'E-commerce Adoption', 'Robotics Use', 'AI Development',
    
    # Additional Miscellaneous parameters
    'Time Use Surveys', 'Leisure Activity Diversity', 'Local Cuisine Quality',
    'International Cuisine Availability', 'Music Scene', 'Nightlife Options',
    'Festival and Events', 'Public Libraries', 'Museums and Galleries',
    'Sport Facilities', 'Public Pools', 'Beach Quality',
    'Mountain Access', 'Historic Preservation', 'Future Preparedness'
]


# Predefined 15-Minute City parameters
def fill_15min_city_params():
    fifteen_min_city_params = ['Accessibility to Public Transport', 'Density of Essential Services', 
                               'Availability of Safe Cycling Lanes', 'Availability of Green Spaces', 
                               'Air Quality', 'Noise Levels', 'Street Connectivity', 'Local Employment Opportunities',
                               'Access to Educational Institutions', 'Healthcare Facility Accessibility', 
                               'Housing Affordability', 'Community Spaces', 'Local Food Production', 
                               'Safety and Security', 'Sustainability Initiatives', 'Cultural Amenities',
                               'Water Quality and Accessibility', 'Digital Connectivity', 'Social Inclusion',
                               'Governance and Civic Participation']
    
    for i, param in enumerate(fifteen_min_city_params):
        param_entries[i].delete(0, tk.END)
        param_entries[i].insert(0, param)

def print_connections(*args):
    print("Current connections:")
    for i, connections in enumerate(param_connections):
        for j, var in connections.items():
            if var.get():
                print(f"Parameter {i+1} is connected to Parameter {j+1}")

def randomize_weights():
    for scale in param_scales:
        random_value = random.randint(1, 10)  # Change this range according to your scale range
        scale.set(random_value)

def select_all(connection_vars):
    for var in connection_vars.values():
        var.set(1)
    print_connections()

def show_connections(param_index):
    def print_connections():
        print("Current connections for Parameter {}: {}".format(param_index+1, param_connections[param_index]))

    window = Toplevel()
    window.title(f"Connect Parameter {param_index+1}")
    
    select_all_var = IntVar()
    
    def select_all():
        state = select_all_var.get()
        for var in connection_vars.values():
            var.set(state)
        print_connections()

    Checkbutton(window, text="Select All", variable=select_all_var, command=select_all).pack()
    
    connection_vars = {}
    for i, param_entry in enumerate(param_entries):
        if param_entry.get():
            var = IntVar()
            c = Checkbutton(window, text=f"Parameter {i+1}", variable=var, command=print_connections)
            c.pack()
            connection_vars[i] = var
    param_connections[param_index] = connection_vars

def connect_random_params():
    # Assuming you have 20 parameters and param_connections is a list of dictionaries
    # Clear existing connections
    for connections in param_connections:
        connections.clear()

    # Randomly connect parameters
    for i in range(len(param_entries)):
        num_connections = random.randint(1, 3)  # Each parameter can have 1 to 3 connections
        connections = random.sample(range(len(param_entries)), num_connections)
        for connection in connections:
            if connection != i:  # Avoid self-connections
                param_connections[i][connection] = IntVar(value=1)  # Use IntVar to be consistent

    # Update the interface to reflect the new connections
    generate_graph()
    print_connections()

def generate_label(parameters):
    return random.choices(parameters, k=3)# Reduced k for better visibility

def generate_graph(predefined_params=None):
    global G, pos, labels, node_sizes, show_labels, param_connections  # Declare as global to modify
    if predefined_params:
        user_parameters = predefined_params[:len(param_scales)]  # Limit to the number of available scales
    else:
        user_parameters = [entry.get() for entry in param_entries if entry.get() != '']

    num_nodes = len(user_parameters)
    
    # Create a graph with nodes equal to the number of user-defined parameters
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    
    # Add edges to make it a complete graph
    # Clear existing edges and add new ones based on selected connections
    G.clear_edges()
    for i, connections in enumerate(param_connections):
        for j, var in connections.items():
            if var.get():
                G.add_edge(i, j)
            
    # Assign labels and sizes based on user-defined parameters and weights
    labels = {i: param for i, param in enumerate(user_parameters)}
    node_sizes = [int(param_scales[i].get()) * 10 for i in range(num_nodes)]
    
    ax.clear()
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, node_color='#04D99D', node_size=node_sizes, width=0.25, ax=ax)  # Set width to 0.1
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax)

    if show_labels:
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax)
    
    canvas.draw()
    
    text_area.delete(1.0, tk.END)
    for node, label in labels.items():
        text_area.insert(tk.END, f"Node {node}: {label}\n")

def animate_tree(frame):
    global pos  # Use global position dictionary
    
    # Check if the graph exists
    if G is None or not pos:
        print("No graph to animate.")
        return

    # Randomly move the nodes
    for node in pos:
        pos[node] += np.random.normal(scale=0.01, size=2)  # Adjust the scale for desired movement

    # Update the graph with new positions
    ax.clear()
    nx.draw(G, pos, node_color=node_colors, node_size=node_sizes, with_labels=show_labels)
    ax.set_title(f"Animated Tree Graph - Frame {frame}")
    canvas.draw()
   
    
def animate_tree_generation():
    global ani  # Declare as global to modify/read
    # Ensure the graph exists
    if G is not None:
        # Start the animation, calling animate_tree for each frame
        ani = FuncAnimation(fig, animate_tree, frames=range(100), repeat=True)
        canvas.draw()
    else:
        print("Please generate the graph first.")


def generate_tree(max_nodes=500):
    # Use 'max_nodes' to control the size of the tree
    graph_gen = TreeGenerator(max_nodes)
    graph_gen.grow_tree()

    # Use networkx to get the positions and colors for each node
    positions = nx.get_node_attributes(graph_gen.G, 'pos')
    colors = [graph_gen.G.nodes[node]['color'] for node in graph_gen.G.nodes]

    # Determine the size of each node based on its degree
    node_degrees = dict(graph_gen.G.degree())
    node_sizes = [node_degrees[node] * 1 for node in graph_gen.G.nodes]

    # Clear the previous figure and create a new one
    ax.clear()
    fig.set_dpi(300) 
    nx.draw(graph_gen.G, positions, node_color=colors, node_size=node_sizes, with_labels=False, width=0.1)
    #ax.set_title(f"Generated Tree Graph - Frame {max_nodes}")
    canvas.draw()

    
def update(frame, G, ax, canvas):
    global pos  # Use the global pos variable

    # Check if the graph has nodes and the pos dictionary has been initialized
    if not G.nodes or not pos:
        return

    # Randomly update positions
    for node in pos:
        pos[node] += np.random.normal(scale=0.01, size=2)  # Change this scale for more/less movement

    # Use the current positions as a starting point for the spring layout
    new_pos = nx.spring_layout(G, pos=pos, iterations=5)

    # Smoothly transition to the new position
    for node in pos:
        pos[node] += 0.1 * (new_pos[node] - pos[node])  # Adjust this factor for faster/slower transitions

    # Clear the previous drawing and draw the new frame
    ax.clear()
    nx.draw(G, pos, node_color='#04D99D', node_size=20, width=0.1, ax=ax)
    canvas.draw()  # Update the canvas to show the new frame


def animate_graph():
    global ani, pos, G, ax, canvas  # Declare as global to modify/read
    if G is not None:  # Ensure the graph exists
        pos = nx.spring_layout(G, seed=42)  # Initialize positions
        ani = FuncAnimation(fig, update, frames=range(100), fargs=(G, ax, canvas), blit=False)
    else:
        print("Please generate the graph first.")
    save_graph()

def save_graph():
    plt.savefig("graph.png")

def save_animation():
    global ani  # Declare as global to read
    if ani is not None:  # Check if ani is None before saving
        ani.save("animation.gif", writer='imagemagick')
    else:
        print("Please generate the animation first.")

def reset():
    global ax, canvas, param_entries, param_scales, param_connections  # Declare as global to modify
    ax.clear()  # Clear the axis
    canvas.draw()  # Redraw the canvas

    # Clear the parameter entries
    for entry in param_entries:
        entry.delete(0, tk.END)

    # Reset the scales (sliders) to a default value, say 1
    for scale in param_scales:
        scale.set(1)
    
    # Reset the param_connections
    param_connections = [{} for _ in range(len(param_entries))]
    
    generate_graph()

def toggle_labels():
    global show_labels  # Declare as global to modify
    show_labels = not show_labels  # Toggle the state
    generate_graph()  # Redraw the graph to reflect the change

def toggle_input_frame():
    global input_frame_visible
    if input_frame_visible:
        input_frame.pack_forget()
        canvas.get_tk_widget().pack_forget()  # Forget the current packing
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)  # Repack to fill the space
    else:
        input_frame.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.get_tk_widget().pack_forget()  # Forget the current packing
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)  # Repack to fill the space
    input_frame_visible = not input_frame_visible

# Initialize the variable to track the visibility
input_frame_visible = True  # Start with the input frame being visible
  
# Use StringVar to monitor changes
param_string_vars = []

# Initialize Tkinter window
window = tk.Tk()
window.title("Network Growth Model")
window.configure(background='white')  # Set the background color
font_tuple = ("Helvetica", 8)  # Define a modern font tuple

# Define the custom style
style = ttk.Style()
style.theme_use('clam')  # Use a theme that allows customization


# Frame for input boxes and scales at the bottom
input_frame = ttk.Frame(window, padding="10")
input_frame.pack(side=tk.BOTTOM, fill=tk.X)

for i in range(1, 11):
    ttk.Label(input_frame, text=f"Parameter {i}:", font=font_tuple).grid(row=i, column=0, padx=10, pady=5)
    param_entry = ttk.Entry(input_frame, font=font_tuple)
    param_entry.grid(row=i, column=1, padx=10, pady=5)
    param_entries.append(param_entry)
    
    param_scale = ttk.Scale(input_frame, from_=1, to=10, orient='horizontal')
    param_scale.grid(row=i, column=2, padx=10, pady=5)
    param_scales.append(param_scale)

    btn = Button(input_frame, text="Choose Connections", command=lambda i=i-1: show_connections(i))
    btn.grid(row=i, column=3, padx=10, pady=5)
    param_connections.append({})

# Second set of parameters
for i in range(11, 21):
    ttk.Label(input_frame, text=f"Parameter {i}:", font=font_tuple).grid(row=i-10, column=4, padx=10, pady=5)
    param_entry = ttk.Entry(input_frame, font=font_tuple)
    param_entry.grid(row=i-10, column=5, padx=10, pady=5)
    param_entries.append(param_entry)
    
    param_scale = ttk.Scale(input_frame, from_=1, to=10, orient='horizontal')
    param_scale.grid(row=i-10, column=6, padx=10, pady=5)
    param_scales.append(param_scale)

    btn = Button(input_frame, text="Choose Connections", command=lambda i=i-1: show_connections(i))
    btn.grid(row=i-10, column=7, padx=10, pady=5)
    param_connections.append({})

button_options = {'padx': 10, 'pady': 5, 'ipadx': 10, 'ipady': 5}  # Common button options for padding and internal padding

# Define button size
button_width = 20
button_height = 2

# Generation and Animation Buttons
generate_button = ttk.Button(input_frame, text="Generate Network", command=generate_graph, width=button_width)
generate_button.grid(row=1, column=8, **button_options)

animate_button = ttk.Button(input_frame, text="Animate Network", command=animate_graph, width=button_width)
animate_button.grid(row=2, column=8, **button_options)

# Saving Buttons
save_button = ttk.Button(input_frame, text="Save as PNG", command=save_graph, width=button_width)
save_button.grid(row=3, column=8, **button_options)

save_ani_button = ttk.Button(input_frame, text="Save Animation", command=save_animation, width=button_width)
save_ani_button.grid(row=4, column=8, **button_options)

fill_15min_city_params_button = ttk.Button(input_frame, text="Fill with 15-min City Parameters", command=fill_15min_city_params, width=button_width)
fill_15min_city_params_button.grid(row=5, column=8, **button_options)

# Weight Randomization and Reset Buttons
randomize_button = ttk.Button(input_frame, text="Randomize Weights", command=randomize_weights, width=button_width)
randomize_button.grid(row=6, column=8, **button_options)

reset_button = ttk.Button(input_frame, text="Reset", command=reset, width=button_width)
reset_button.grid(row=7, column=8, **button_options)

# Tree  Button
animate_tree_button = ttk.Button(input_frame, text="Create Tree", command=generate_tree, width=button_width)
animate_tree_button.grid(row=8, column=8, **button_options)


# Tree Animation Button
animate_tree_button = ttk.Button(input_frame, text="Animate Tree", command=animate_tree_generation, width=button_width)
animate_tree_button.grid(row=9, column=8, **button_options)

# Add this to your button creation section in the GUI code
connect_random_button = ttk.Button(input_frame, text="Connect Random Params", command=connect_random_params, width=button_width)
connect_random_button.grid(row=11, column=8, **button_options)

# Add a button to toggle the input frame
toggle_input_btn = ttk.Button(window, text="Toggle Input Frame", command=toggle_input_frame, width=button_width)
toggle_input_btn.pack(side=tk.BOTTOM, pady=5)  # You can change the side if needed


# Create an initial empty plot
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Add a scrolled text area to display labels, place it at the top
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=20, font=font_tuple)
text_area.pack(side=tk.TOP, pady=10)

# Initialize initial nodes and labels
initial_nodes = [1, 2, 3]
# Start Tkinter event loop
window.mainloop()
