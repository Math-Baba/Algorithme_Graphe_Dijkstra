# Projet Visualisation de Graphe

Interface web pour visualiser et tester les algorithmes de graphe (Dijkstra et Coloriage).

## Utilisation

1. **Créer la base de donnée PostgreSQL**
   
   Créez une base de donnée sur PG en suivant le schéma ci-après
   ```bash
   CREATE TABLE nodes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    pos_x FLOAT NOT NULL,
    pos_y FLOAT NOT NULL
   );

   CREATE TABLE edges (
    id SERIAL PRIMARY KEY,
    node_a VARCHAR(100) NOT NULL,
    node_b VARCHAR(100) NOT NULL,
    weight FLOAT NOT NULL,
    penalty FLOAT NOT NULL DEFAULT 0,

    CONSTRAINT fk_node_a FOREIGN KEY (node_a) REFERENCES nodes(name) ON DELETE CASCADE,
    CONSTRAINT fk_node_b FOREIGN KEY (node_b) REFERENCES nodes(name) ON DELETE CASCADE
   );
   ```

3. **Créer le fichier .env**
   
   Créez un fichier .env avec vos variables d'environnement pour vous connecter à votre base de données PostgreSQL
   ```bash
   DB_NAME=nom de votre base de donnée
   DB_USER=postgres
   DB_PASSWORD= votre mot de passe
   DB_HOST=localhost
   DB_PORT=5432
   ```
   
5. **Démarrer le serveur backend** :
   ```bash
   cd backend
   python server.py
   ```
   Le serveur doit être accessible sur `http://localhost:5000`

6. **Ouvrir le frontend** :
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

## Auteur
**Math-Baba** - [GitHub](https://github.com/Math-Baba)

