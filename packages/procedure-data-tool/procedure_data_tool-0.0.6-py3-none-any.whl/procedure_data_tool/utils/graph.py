import networkx as nx
import matplotlib.pyplot as plt

def makeGraph(inventory, route):
    G = nx.Graph()

    color_map = []
    for component in route:
        if component:
            G.add_node(component.ein)
            for connection in component.connections:
                 G.add_edge(component.ein, connection.ein)
    
    # for key, value in components.items():
    #     if key:
    #         G.add_node(key)
    #         for connection in value.connections:
    #             G.add_edge(key, connection.ein)

    for node in G:
        color_map.append(inventory[node].color)

    pos = nx.planar_layout(G)  # Position nodes using the Fruchterman-Reingold force-directed algorithm
    # nx.draw(G, pos, with_labels=True, node_size=80, node_color="skyblue", font_size=9, font_color='black', edge_color='gray', linewidths=10)
    nx.draw(G, pos, with_labels=True, node_size=80, node_color=color_map, font_size=9, font_color='black', edge_color='gray', linewidths=10)
    plt.title = "Route PReview"
    plt.show()