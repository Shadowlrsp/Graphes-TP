import networkx as nx
import matplotlib.pyplot as plt

def initialiser_graphe():
    """ Crée un graphe pondéré représentant un réseau de serveurs. """
    G = nx.Graph()
    liaisons = [
        ('Serveur A', 'Serveur B', 4), ('Serveur A', 'Serveur C', 2), ('Serveur B', 'Serveur C', 5), 
        ('Serveur B', 'Serveur D', 10), ('Serveur C', 'Serveur D', 3), ('Serveur C', 'Serveur E', 8), 
        ('Serveur D', 'Serveur E', 4), ('Serveur D', 'Serveur F', 11), ('Serveur E', 'Serveur F', 1)
    ]
    G.add_weighted_edges_from(liaisons)
    return G

def calculer_routage_dijkstra(G, src, dest):
    """ Calcule le plus court chemin et sa distance via l'algorithme de Dijkstra. """
    chemin = nx.dijkstra_path(G, source=src, target=dest, weight='weight')
    distance = nx.dijkstra_path_length(G, source=src, target=dest, weight='weight')
    return chemin, distance

def afficher_reseau(G, chemin_trouve):
    """ Génère une visualisation du graphe avec le chemin de routage en couleur. """
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))

    nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=800)
    
    poids = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=poids)

    aretes_chemin = list(zip(chemin_trouve, chemin_trouve[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=aretes_chemin, edge_color='red', width=2)
    nx.draw_networkx_nodes(G, pos, nodelist=chemin_trouve, node_color='orange')

    plt.title("Simulation de routage IP avec Algorithme de Dijkstra")
    plt.show()

# --- Main ---
reseau = initialiser_graphe()
depart, arrivee = 'Serveur A', 'Serveur F'

route, cout = calculer_routage_dijkstra(reseau, depart, arrivee)

print(f"Trajet : {route}")
print(f"Latence totale : {cout}ms")

afficher_reseau(reseau, route)