import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np

# Global variables
G = None
pos = None
labels = None
node_sizes = None
ani = None  # Initialize ani as None
show_labels = True  # Declare as a global variable at the top of your script


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

def fill_all_params():
    generate_graph(predefined_params=all_params) 

def fill_predefined_params():
    for i, param in enumerate(predefined_params):
        param_entries[i].delete(0, tk.END)
        param_entries[i].insert(0, param)

def randomize_weights():
    for scale in param_scales:
        random_value = random.randint(1, 10)  # Change this range according to your scale range
        scale.set(random_value)

def generate_label(parameters):
    return random.choices(parameters, k=3)# Reduced k for better visibility

def generate_graph(predefined_params=None):
    global G, pos, labels, node_sizes, show_labels  # Declare as global to modify
    if predefined_params:
        user_parameters = predefined_params[:len(param_scales)]  # Limit to the number of available scales
    else:
        user_parameters = [entry.get() for entry in param_entries if entry.get() != '']

    num_nodes = len(user_parameters)
    
    # Create a graph with nodes equal to the number of user-defined parameters
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    
    # Add edges to make it a complete graph
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            G.add_edge(i, j)
            
    # Assign labels and sizes based on user-defined parameters and weights
    labels = {i: param for i, param in enumerate(user_parameters)}
    node_sizes = [int(param_scales[i].get()) * 10 for i in range(num_nodes)]
    
    ax.clear()
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, node_color='#04D99D', node_size=node_sizes, width=0.1, ax=ax)  # Set width to 0.1
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax)

    if show_labels:
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax)
    
    canvas.draw()
    
    text_area.delete(1.0, tk.END)
    for node, label in labels.items():
        text_area.insert(tk.END, f"Node {node}: {label}\n")

def update(frame, G, ax, canvas):
    global pos, show_labels  # Use the global pos variable
    # Randomly update positions
    for node in pos:
        pos[node] += np.random.normal(scale=0.1, size=2)  # Change this scale for more/less movement
    
    ax.clear()
    nx.draw(G, pos, node_color='#04D99D', node_size=node_sizes, width=0.1, ax=ax)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax)
    if show_labels:
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax)
    canvas.draw()  # Update the canvas to show the new frame
    return ax,

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
    global ax, canvas, param_entries, param_scales  # Declare as global to modify
    ax.clear()  # Clear the axis
    canvas.draw()  # Redraw the canvas

    # Clear the parameter entries
    for entry in param_entries:
        entry.delete(0, tk.END)

    # Reset the scales (sliders) to a default value, say 1
    for scale in param_scales:
        scale.set(1)
    generate_graph()


def toggle_labels():
    global show_labels  # Declare as global to modify
    show_labels = not show_labels  # Toggle the state
    generate_graph()  # Redraw the graph to reflect the change
  


# Initialize Tkinter window
window = tk.Tk()
window.title("Network Growth Model")
window.configure(background='white')  # Set the background color
font_tuple = ("Helvetica", 12)  # Define a modern font tuple

# Define the custom style
style = ttk.Style()
style.theme_use('clam')  # Use a theme that allows customization


# Frame for input boxes and scales at the bottom
input_frame = ttk.Frame(window, padding="10")
input_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Add parameter input boxes and weight scales with padding
param_entries = []
param_scales = []

# First set of parameters
for i in range(1, 11):
    ttk.Label(input_frame, text=f"Parameter {i}:", font=font_tuple).grid(row=i, column=0, padx=10, pady=5)
    param_entry = ttk.Entry(input_frame, font=font_tuple)
    param_entry.grid(row=i, column=1, padx=10, pady=5)
    param_entries.append(param_entry)
    
    param_scale = ttk.Scale(input_frame, from_=1, to=10, orient='horizontal')
    param_scale.grid(row=i, column=2, padx=10, pady=5)
    param_scales.append(param_scale)

# Second set of parameters
for i in range(11, 21):
    ttk.Label(input_frame, text=f"Parameter {i}:", font=font_tuple).grid(row=i-10, column=3, padx=10, pady=5)
    param_entry = ttk.Entry(input_frame, font=font_tuple)
    param_entry.grid(row=i-10, column=4, padx=10, pady=5)
    param_entries.append(param_entry)
    
    param_scale = ttk.Scale(input_frame, from_=1, to=10, orient='horizontal')
    param_scale.grid(row=i-10, column=5, padx=10, pady=5)
    param_scales.append(param_scale)

# Generation and Animation Buttons
generate_button = ttk.Button(input_frame, text="Generate Network", command=generate_graph)
generate_button.grid(row=1, column=6, padx=10, pady=5)

animate_button = ttk.Button(input_frame, text="Animate Network", command=animate_graph)
animate_button.grid(row=2, column=6, padx=10, pady=5)

# Saving Buttons
save_button = ttk.Button(input_frame, text="Save as PNG", command=save_graph)
save_button.grid(row=3, column=6, padx=10, pady=5)

save_ani_button = ttk.Button(input_frame, text="Save Animation", command=save_animation)
save_ani_button.grid(row=4, column=6, padx=10, pady=5)

# Predefined Parameter Buttons
predefined_params_button = ttk.Button(input_frame, text="Fill with Predefined Parameters", command=fill_predefined_params)
predefined_params_button.grid(row=5, column=6, padx=10, pady=5)

fill_15min_city_params_button = ttk.Button(input_frame, text="Fill with 15-min City Parameters", command=fill_15min_city_params)
fill_15min_city_params_button.grid(row=6, column=6, padx=10, pady=5)

fill_all_params_button = ttk.Button(input_frame, text="Fill with All Parameters", command=fill_all_params)
fill_all_params_button.grid(row=7, column=6, padx=10, pady=5)

# Weight Randomization Button
randomize_button = ttk.Button(input_frame, text="Randomize Weights", command=randomize_weights)
randomize_button.grid(row=8, column=6, padx=10, pady=5)

# Reset Button
reset_button = ttk.Button(input_frame, text="Reset", command=reset)
reset_button.grid(row=9, column=6, padx=10, pady=5)

toggle_labels_button = ttk.Button(input_frame, text="Toggle Labels", command=toggle_labels)
toggle_labels_button.grid(row=10, column=6, padx=10, pady=5)


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