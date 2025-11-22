# Frontend - Visualisation de Graphe

Interface web pour visualiser et tester les algorithmes de graphe (Dijkstra et Coloriage).

## Utilisation

1. **Démarrer le serveur backend** :
   ```bash
   cd backend
   python server.py
   ```
   Le serveur doit être accessible sur `http://localhost:5000`

2. **Ouvrir le frontend** :
   - Ouvrir le fichier `index.html` dans votre navigateur
   - Ou utiliser un serveur local (ex: Live Server dans VS Code)

## Fonctionnalités

### Visualisation du graphe
- Chargement automatique du graphe depuis la base de données
- Affichage des nœuds et des arêtes sur un canvas
- Visualisation des poids des arêtes

### Gestion du graphe
- **Ajouter un nœud** : Créer de nouveaux nœuds avec un nom
- **Ajouter une arête** : Connecter deux nœuds avec un poids

### Algorithme de Dijkstra
- Calculer le chemin le plus court entre deux nœuds
- Visualisation du chemin en vert sur le graphe
- Affichage de la distance totale et du chemin complet

### Algorithme de Coloriage
- Appliquer un coloriage au graphe
- Visualisation des couleurs sur les nœuds
- Garantit que deux nœuds adjacents n'ont jamais la même couleur

## Interface

- **Design moderne** avec dégradés et effets visuels
- **Responsive** : s'adapte aux différentes tailles d'écran
- **Panneau de contrôle** : toutes les actions à portée de main
- **Zone de visualisation** : canvas interactif pour le graphe

## Notes

- Assurez-vous que le backend est démarré avant d'utiliser l'interface
- Les nœuds sont positionnés automatiquement en cercle si leurs coordonnées ne sont pas définies
- Le chemin Dijkstra est mis en évidence en vert
- Les couleurs du coloriage sont appliquées directement sur les nœuds

