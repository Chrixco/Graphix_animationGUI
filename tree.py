import random
import networkx as nx
import logging

# Setting up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class TreeGenerator:
    def __init__(self, max_nodes):
        self.G = nx.Graph()
        self.max_nodes = max_nodes
        self.current_node = 0

    def generate_random_color(self):
        return f"#{''.join(random.choices('0123456789ABCDEF', k=6))}"

    def generate_random_position(self, parent_pos=None):
        if parent_pos:
            return (parent_pos[0] + random.uniform(-0.05, 0.05), parent_pos[1] + random.uniform(-0.05, 0.05))
        return (random.uniform(0, 1), random.uniform(0, 1))

    def add_node(self, parent_node=None):
        if self.current_node < self.max_nodes:
            new_color = self.generate_random_color()
            new_position = self.generate_random_position(self.G.nodes[parent_node]['pos'] if parent_node is not None else None)
            self.G.add_node(self.current_node, color=new_color, pos=new_position)

            if parent_node is not None:
                self.G.add_edge(parent_node, self.current_node)
            
            logging.debug(f"Node {self.current_node} added with position {new_position} and color {new_color}")
            self.current_node += 1
            return True
        return False

    def grow_tree(self, parent_node=None):
        if not self.add_node(parent_node):
            return

        num_children = random.randint(1, 5)
        logging.debug(f"Node {self.current_node - 1} will have {num_children} children.")

        for _ in range(num_children):
            if self.current_node >= self.max_nodes:
                break
            child_node = self.current_node
            self.add_node(parent_node)
            self.grow_tree(child_node)

# Example usage
if __name__ == "__main__":
    max_nodes = 20
    graph_gen = TreeGenerator(max_nodes)
    graph_gen.grow_tree()

    logging.info(f"Generated a graph with {len(graph_gen.G.nodes)} nodes and {len(graph_gen.G.edges)} edges.")
    print(f"Generated a graph with {len(graph_gen.G.nodes)} nodes and {len(graph_gen.G.edges)} edges.")
