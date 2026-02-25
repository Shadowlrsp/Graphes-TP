import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random

def initialiser_graphe():
    G = nx.Graph()
    test = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
            'J', 'K', 'L', 'M', 'N', 'O', 'P']
    liaisons = []
    for t1 in test:
        chance = random.random()
        if chance < 0.9:
            continue

        for t2 in test:
            if t2 == t1: continue

            poids = random.randint(0, 20)
            liaisons.append(
                (f'Serveur {t1}', f'Serveur {t2}', poids)
            )
    # liaisons = [
    #     ('Serveur A', 'Serveur B', 4), 
    #     ('Serveur A', 'Serveur C', 2), 
    #     ('Serveur B', 'Serveur D', 10), 
    #     ('Serveur B', 'Serveur E', 6),
    #     ('Serveur C', 'Serveur F', 15),
    #     ('Serveur D', 'Serveur G', 8),
    #     ('Serveur D', 'Serveur H', 7),
    #     ('Serveur E', 'Serveur I', 3),
    #     ('Serveur F', 'Serveur J', 9),
    #     ('Serveur G', 'Serveur K', 5),
    #     ('Serveur H', 'Serveur L', 11),
    #     ('Serveur I', 'Serveur M', 4),
    #     ('Serveur J', 'Serveur N', 6),
    #     ('Serveur K', 'Serveur O', 2),
    #     ('Serveur L', 'Serveur P', 12),
    #     ('Serveur M', 'Serveur Q', 7),
    #     ('Serveur N', 'Serveur R', 5),
    #     ('Serveur O', 'Serveur S', 3),
    #     ('Serveur P', 'Serveur T', 8),
    #     ('Serveur E', 'Serveur H', 5),
    #     ('Serveur G', 'Serveur J', 6),
    #     ('Serveur I', 'Serveur L', 9),
    #     ('Serveur K', 'Serveur N', 4),
    #     ('Serveur M', 'Serveur P', 7),
    #     ('Serveur Q', 'Serveur R', 3),
    #     ('Serveur S', 'Serveur T', 5),
    #     ('Serveur B', 'Serveur F', 13),
    #     ('Serveur D', 'Serveur I', 8),
    #     ('Serveur H', 'Serveur M', 6),
    #     ('Serveur J', 'Serveur O', 9),
    # ]
    G.add_weighted_edges_from(liaisons)
    return G

def afficher_reseau(G, chemin_trouve):
    pos = nx.spring_layout(G, k=2, iterations=50)
    plt.figure(figsize=(14, 10))

    nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=800, font_size=9)
    
    poids = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=poids, font_size=7)

    aretes_chemin = list(zip(chemin_trouve, chemin_trouve[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=aretes_chemin, edge_color='red', width=3)
    nx.draw_networkx_nodes(G, pos, nodelist=chemin_trouve, node_color='orange', node_size=900)

    plt.title("Simulation de routage IP avec Algorithme de Dijkstra", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

def obtenir_tous_noeuds(G):
    return sorted(G.nodes())

def afficher_statistiques_graphe(G):
    print("\n" + "="*60)
    print("STATISTIQUES DU GRAPHE")
    print("="*60)
    print(f"Nombre de nœuds: {G.number_of_nodes()}")
    print(f"Nombre de liaisons: {G.number_of_edges()}")
    
    degrees = dict(G.degree(weight='weight'))
    top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:3]
    print("\nTop 3 nœuds les plus connectés:")
    for i, (node, degree) in enumerate(top_nodes, 1):
        print(f"  {i}. {node}: {degree} connexions")
    print("="*60 + "\n")

def afficher_menu_principal():
    print("\n" + "="*60)
    print("1. Calculer le chemin le plus court entre deux serveurs")
    print("2. Afficher tous les serveurs disponibles")
    print("3. Afficher les statistiques du graphe")
    print("4. Voir les distances depuis un serveur")
    print("5. Quitter")
    print("="*60)

def afficher_serveurs(G):
    print("\nSERVEURS DISPONIBLES:")
    noeuds = obtenir_tous_noeuds(G)
    for i, noeud in enumerate(noeuds, 1):
        print(f"  {i}. {noeud}")

def choisir_serveur(G, prompt):
    noeuds = obtenir_tous_noeuds(G)
    while True:
        print(f"\n{prompt}")
        try:
            afficher_serveurs(G)
            choix = input("\nEntrez le numéro ou le nom du serveur : ").strip()
            
            if choix.isdigit():
                idx = int(choix) - 1
                if 0 <= idx < len(noeuds):
                    return noeuds[idx]
                else:
                    print("Numero invalide. Réessayez.")
            else:
                if choix in noeuds:
                    return choix
                else:
                    print("Serveur non trouvé. Réessayez.")
        except Exception as e:
            print(f"Erreur: {e}. Réessayez.")

def calculer_chemin_utilisateur(G):
    src = choisir_serveur(G, "Choisir le serveur SOURCE:")
    dest = choisir_serveur(G, "Choisir le serveur DESTINATION:")
    
    if src == dest:
        print("\nLe serveur source et destination sont identiques")
        return
    
    try:
        chemin, distance = calculer_routage_dijkstra(G, src, dest)
        
        print("\n" + "="*60)
        print("RESULTAT DU CALCUL")
        print("="*60)
        print(f"Serveur source: {src}")
        print(f"Serveur destination: {dest}")
        print(f"Chemin trouvé: {' > '.join(chemin)}")
        print(f"Latence totale: {distance}ms")
        print(f"Nombre de sauts: {len(chemin) - 1}")
        print("="*60)
        
        afficher = input("\nAfficher le graphe avec le chemin en rouge? (o/n): ").strip().lower()
        if afficher == 'o':
            afficher_reseau(G, chemin)
    
    except nx.NetworkXNoPath:
        print("\nAucun chemin trouvé entre ces deux serveurs")
    except Exception as e:
        print(f"\nErreur: {e}")

def afficher_distances_depuis_serveur(G):
    src = choisir_serveur(G, "Choisir le serveur source:")
    
    try:
        distances = nx.single_source_dijkstra_path_length(G, src, weight='weight')
        
        print("\n" + "="*60)
        print(f"DISTANCES DEPUIS {src}")
        print("="*60)
        
        for dest, dist in sorted(distances.items()):
            if dest != src:
                print(f"{dest}: {dist}ms")
        
        print("="*60)
    
    except Exception as e:
        print(f"Erreur: {e}")

def menu_interactif(G):
    while True:
        afficher_menu_principal()
        choix = input("Choisissez une option (1-5): ").strip()
        
        if choix == '1':
            calculer_chemin_utilisateur(G)
        elif choix == '2':
            afficher_serveurs(G)
        elif choix == '3':
            afficher_statistiques_graphe(G)
        elif choix == '4':
            afficher_distances_depuis_serveur(G)
        elif choix == '5':
            print("\nAu revoirr\n")
            break
        else:
            print("Option invalide. Réessayez")

class ApplicationGUI:
    
    def __init__(self, root, graphe):
        self.root = root
        self.graphe = graphe
        self.root.title("Systeme de Routage IP - Algorithme de Dijkstra")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f0f0')
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        self.style.configure('Normal.TLabel', font=('Helvetica', 10))
        
        self.create_widgets()
    
    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tab_calcul = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_calcul, text='Calculer Chemin')
        self.create_calcul_tab()
        
        self.tab_serveurs = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_serveurs, text='Serveurs')
        self.create_serveurs_tab()
        
        self.tab_stats = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_stats, text='Statistiques')
        self.create_stats_tab()
        
        self.tab_distances = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_distances, text='Distances')
        self.create_distances_tab()
        
        self.tab_graphe = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_graphe, text='Visualisation')
        self.create_graphe_tab()
    
    def create_calcul_tab(self):
        frame = ttk.Frame(self.tab_calcul, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Calcul du Chemin le Plus Court", style='Title.TLabel').pack(pady=10)
        
        ttk.Label(frame, text="Serveur SOURCE:", style='Header.TLabel').pack(anchor='w', pady=(10, 5))
        self.combo_src = ttk.Combobox(frame, values=sorted(self.graphe.nodes()), state='readonly', width=30)
        self.combo_src.pack(fill='x', pady=(0, 15))
        
        ttk.Label(frame, text="Serveur DESTINATION:", style='Header.TLabel').pack(anchor='w', pady=(10, 5))
        self.combo_dest = ttk.Combobox(frame, values=sorted(self.graphe.nodes()), state='readonly', width=30)
        self.combo_dest.pack(fill='x', pady=(0, 20))
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Calculer le chemin", command=self.calculer_chemin_gui).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Afficher graphe", command=self.afficher_graphe_chemin).pack(side='left', padx=5)
        
        ttk.Label(frame, text="Resultat:", style='Header.TLabel').pack(anchor='w', pady=(20, 5))
        self.text_resultat = scrolledtext.ScrolledText(frame, height=12, width=70, bg='white')
        self.text_resultat.pack(fill='both', expand=True)
    
    def create_serveurs_tab(self):
        frame = ttk.Frame(self.tab_serveurs, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Liste des Serveurs Disponibles", style='Title.TLabel').pack(pady=10)
        
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill='both', expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.listbox_serveurs = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=('Helvetica', 11), height=20)
        self.listbox_serveurs.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.listbox_serveurs.yview)
        
        for i, noeud in enumerate(sorted(self.graphe.nodes()), 1):
            self.listbox_serveurs.insert(tk.END, f"{i}. {noeud}")
        
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill='x', pady=10)
        ttk.Label(info_frame, text=f"Total: {self.graphe.number_of_nodes()} serveurs", style='Normal.TLabel').pack()
    
    def create_stats_tab(self):
        frame = ttk.Frame(self.tab_stats, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Statistiques du Graphe", style='Title.TLabel').pack(pady=10)
        
        self.text_stats = scrolledtext.ScrolledText(frame, height=20, width=70, bg='white')
        self.text_stats.pack(fill='both', expand=True, pady=10)
        
        self.afficher_stats()
        
        ttk.Button(frame, text="Rafraichir", command=self.afficher_stats).pack(pady=10)
    
    def create_distances_tab(self):
        frame = ttk.Frame(self.tab_distances, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Distances depuis un Serveur", style='Title.TLabel').pack(pady=10)
        
        ttk.Label(frame, text="Serveur SOURCE:", style='Header.TLabel').pack(anchor='w', pady=(10, 5))
        self.combo_src_dist = ttk.Combobox(frame, values=sorted(self.graphe.nodes()), state='readonly', width=30)
        self.combo_src_dist.pack(fill='x', pady=(0, 15))
        
        ttk.Button(frame, text="Calculer distances", command=self.afficher_distances_gui).pack(pady=10)
        
        self.text_distances = scrolledtext.ScrolledText(frame, height=15, width=70, bg='white')
        self.text_distances.pack(fill='both', expand=True, pady=10)
    
    def create_graphe_tab(self):
        frame = ttk.Frame(self.tab_graphe, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Visualisation du Réseau IP", style='Title.TLabel').pack(pady=10)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Afficher graphe entier", command=self.afficher_graphe_complet).pack(side='left', padx=5)
        
        self.canvas_frame = ttk.Frame(frame)
        self.canvas_frame.pack(fill='both', expand=True)
    
    def calculer_chemin_gui(self):
        src = self.combo_src.get()
        dest = self.combo_dest.get()
        
        if not src or not dest:
            messagebox.showerror("Erreur", "Veuillez selectionner source ET destination")
            return
        
        if src == dest:
            messagebox.showwarning("Attention", "Source et destination sont identiques")
            return
        
        try:
            chemin, distance = calculer_routage_dijkstra(self.graphe, src, dest)
            
            self.text_resultat.delete(1.0, tk.END)
            
            resultat = "="*60 + "\n"
            resultat += "RESULTAT DU CALCUL\n"
            resultat += "="*60 + "\n\n"
            resultat += f"Serveur source: {src}\n"
            resultat += f"Serveur destination: {dest}\n\n"
            resultat += f"Chemin trouvé:\n{' > '.join(chemin)}\n\n"
            resultat += f"Latence totale: {distance}ms\n"
            resultat += f"Nombre de sauts: {len(chemin) - 1}\n"
            resultat += "\n" + "="*60
            
            self.text_resultat.insert(tk.END, resultat)
            
            messagebox.showinfo("Succès", f"Chemin trouvé\nLatence: {distance}ms")
        
        except nx.NetworkXNoPath:
            messagebox.showerror("Erreur", "Aucun chemin trouvé entre ces serveurs")
            self.text_resultat.delete(1.0, tk.END)
            self.text_resultat.insert(tk.END, "Aucun chemin trouvé")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {e}")
    
    def afficher_graphe_chemin(self):
        src = self.combo_src.get()
        dest = self.combo_dest.get()
        
        if not src or not dest:
            messagebox.showerror("Erreur", "Veuillez selectionner source et destination")
            return
        
        try:
            chemin, distance = calculer_routage_dijkstra(self.graphe, src, dest)
            afficher_reseau(self.graphe, chemin)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {e}")
    
    def afficher_graphe_complet(self):
        pos = nx.spring_layout(self.graphe, k=2, iterations=50)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        nx.draw(self.graphe, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=9, ax=ax)
        
        poids = nx.get_edge_attributes(self.graphe, 'weight')
        nx.draw_networkx_edge_labels(self.graphe, pos, edge_labels=poids, font_size=7, ax=ax)
        
        ax.set_title("Graphe du Réseau IP", fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def afficher_stats(self):
        self.text_stats.delete(1.0, tk.END)
        
        stats = "="*60 + "\n"
        stats += "STATISTIQUES DU GRAPHE\n"
        stats += "="*60 + "\n\n"
        stats += f"Nombre de nœuds: {self.graphe.number_of_nodes()}\n"
        stats += f"Nombre de liaisons: {self.graphe.number_of_edges()}\n"
        
        degrees = dict(self.graphe.degree(weight='weight'))
        top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:5]
        stats += "Top 5 nœuds les plus connectés:\n"
        for i, (node, degree) in enumerate(top_nodes, 1):
            stats += f"  {i}. {node}: {degree} connexions\n"
        
        stats += "\n" + "="*60
        
        self.text_stats.insert(tk.END, stats)
    
    def afficher_distances_gui(self):
        src = self.combo_src_dist.get()
        
        if not src:
            messagebox.showerror("Erreur", "Veuillez selectionner un serveur")
            return
        
        try:
            distances = nx.single_source_dijkstra_path_length(self.graphe, src, weight='weight')
            
            self.text_distances.delete(1.0, tk.END)
            
            resultat = "="*60 + "\n"
            resultat += f"DISTANCES DEPUIS {src}\n"
            resultat += "="*60 + "\n\n"
            
            for dest, dist in sorted(distances.items()):
                if dest != src:
                    resultat += f"{dest}: {dist}ms\n"
            
            resultat += "\n" + "="*60
            
            self.text_distances.insert(tk.END, resultat)
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {e}")

def calculer_routage_dijkstra(G, src, dest):
    chemin = nx.dijkstra_path(G, source=src, target=dest, weight='weight')
    distance = nx.dijkstra_path_length(G, source=src, target=dest, weight='weight')
    return chemin, distance

def afficher_reseau(G, chemin_trouve):
    pos = nx.spring_layout(G, k=2, iterations=50)
    plt.figure(figsize=(14, 10))

    nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=800, font_size=9)
    
    poids = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=poids, font_size=7)

    aretes_chemin = list(zip(chemin_trouve, chemin_trouve[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=aretes_chemin, edge_color='red', width=3)
    nx.draw_networkx_nodes(G, pos, nodelist=chemin_trouve, node_color='orange', node_size=900)

    plt.title("Simulation de routage IP avec Algorithme de Dijkstra", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    reseau = initialiser_graphe()
    
    root = tk.Tk()
    app = ApplicationGUI(root, reseau)
    root.mainloop()
