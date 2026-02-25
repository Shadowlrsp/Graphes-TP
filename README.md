# Systeme de Routage IP - Algorithme de Dijkstra

## Auteurs en S2B1
- Leo Krakovinsky
- Brian Lecoq

## Description du Projet

Ce projet implémente un **système de routage IP basé sur l'algorithme de Dijkstra** pour trouver le chemin le plus court entre deux serveurs dans un réseau informatique.

L'application simule un réseau composé de 20 serveurs (A à T) reliés par 30 liaisons pondérées représentant des latences de communication. L'objectif principal est de calculer le chemin optimal (chemin de latence minimale) entre n'importe quels deux serveurs du réseau.
 
## Technologies Utilisées

### Bibliothèques Python Principales:
- **NetworkX** (v3.0+) - Création et manipulation de graphes
- **Matplotlib** (v3.8+) - Visualisation des graphes et chemins
- **Tkinter** - Interface graphique utilisateur (GUI)

## Architecture du Projet

### Structure du Reseau

Le réseau est représenté comme un **graphe non-orienté pondéré** où:
- **Noeuds**: 20 serveurs (Serveur A à Serveur T)
- **Aretes**: 30 liaisons avec des poids (latences en ms)
- **Topologie**: Arbre hiérarchique avec quelques connexions de secours

Cette structure réaliste garantit que l'algorithme de Dijkstra trouve des chemins intéressants avec plusieurs alternatives.

## Installation

### Prérequis
- Python 3.8+
- pip

### Installation des Dépendances

```bash
pip install -r requirements.txt
```
## Utilisation

### Mode GUI (Interface Graphique)

```bash
python3 main.py
```

La fenêtre s'ouvre avec 5 onglets pour:
1. Choisir deux serveurs et calculer le chemin optimal
2. Consulter la liste des serveurs
3. Voir les statistiques du réseau
4. Afficher les distances depuis n'importe quel serveur
5. Visualiser le graphe complet

## Statistiques du Graphe

### Configuration du Réseau
- **Nombre de noeuds**: 20
- **Nombre de liaisons**: 30

### Noeuds les Plus Connectés
- Serveur B: 4 connexions
- Serveur D: 5 connexions
- Serveur G: 4 connexions