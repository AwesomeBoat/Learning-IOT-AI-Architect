# Heroes vs Monsters 🗡️🐺

## Bienvenue à Shorewood!

Un jeu de rôle en console basé sur les concepts de programmation orientée objet (POO) en Python. Incarnez un héros légendaire et affrontez des monstres terrifiants dans la forêt enchantée de Shorewood, au pays de Stormwall.

---

## 📋 Architecture du Projet

### Structure Modulaire

```
hvm/
├── dice.py              # Mécanique des dés (4d6 best-3, 1d4)
├── loot.py              # Système de butin (Or, Cuir)
├── character.py         # Classe de base Character
├── heroes.py            # Héros: Human, Dwarf
├── monsters.py          # Monstres: Wolf, Orc, Dragonlet
├── game.py              # Moteur: Combat, Board, Game
├── main.py              # Point d'entrée et boucle de jeu
├── test_game.py         # Suite de tests
└── README.md            # Ce fichier
```

### Hiérarchie des Classes

```
Character (classe abstraite)
├── Hero (classe abstraite)
│   ├── Human (Hero avec +1 Force, +1 Endurance)
│   └── Dwarf (Hero avec +2 Endurance)
└── Monster (classe abstraite)
    ├── Wolf (donne du Cuir)
    ├── Orc (+1 Force, donne de l'Or)
    └── Dragonlet (+1 Endurance, donne Or + Cuir)

Loot
├── Gold (pièces d'or)
└── Leather (cuir)

Game Engine
├── Combat (gestion des combats)
├── Board (grille 15x15)
└── Game (contrôleur principal)
```

---

## 🎮 Mécanique de Jeu

### Création du Personnage

Les attributs (Force et Endurance) sont générés avec **4d6 meilleur 3** (standard RPG).

- **Humain**: +1 Force, +1 Endurance (équilibré, polyvalent)
- **Nain**: +2 Endurance (durabilité exceptionnelle)

**Points de Vie** = Endurance + Modificateur(Endurance)

### Système de Modificateurs

```
Caractéristique  Modificateur
< 5              -1
5-9              0
10-14            +1
≥ 15             +2
```

Les modificateurs s'appliquent aux:
- **Dégâts de frappe**: 1d4 + Modificateur(Force)
- **Points de Vie**: Endurance + Modificateur(Endurance)

### Combat

1. Le héros et le monstre se frappent alternativement
2. Chaque attaque: **1d4 + Modificateur(Force)** = dégâts (min 1)
3. Combat continue jusqu'à la mort d'un adversaire
4. **Héros gagne**: récupère le butin, restaure tous les PV, affronte le suivant
5. **Héros meurt**: Fin de partie

### Butin

- **Loup**: 1d4 Cuir
- **Orque**: 1d6 Or
- **Dragonnet**: 1d6 Or + 1d4 Cuir

Le héros peut stocker le butin **sans limite**.

### Grille de Jeu

- **Taille**: 15×15 cases
- **Monstres**: 10 placés aléatoirement, espacés minimum 2 cases
- **Combat**: Se déclenche automatiquement quand le héros est **adjacent** (horizontal ou vertical)
- **Affichage**:
  - `H` = Héro
  - `L`, `O`, `D` = Monstres découverts (Loup, Orque, Dragonnet)
  - `?` = Monstres cachés
  - `.` = Case vide

### Conditions de Victoire / Défaite

- **Victoire**: Tous les monstres vaincus (tableau vide de monstres vivants)
- **Défaite**: Héros tué (PV ≤ 0)

---

## 🎯 Comment Jouer

### Lancer le jeu

```bash
python main.py
```

### Contrôles

```
Mouvement:
  Z ou ↑  : Aller au Nord
  S ou ↓  : Aller au Sud
  Q ou ←  : Aller à l'Ouest
  D ou →  : Aller à l'Est

Actions:
  C       : Combattre monstre adjacent (auto-trigger)
  H       : Afficher l'aide
  QUIT    : Quitter le jeu
```

### Flux de Jeu

1. **Écran d'accueil**: Choisissez votre héros (Humain ou Nain)
2. **Affichage des stats**: Visualisez vos caractéristiques initiales
3. **Exploration**: Naviguez la grille pour trouver les monstres
4. **Combat automatique**: Quand vous êtes adjacent à un monstre, le combat démarre
5. **Butin & Repos**: Après victoire, le héros se repose et récupère son butin
6. **Fin**: Victoire si tous monstres vaincus, défaite si héros meurt

---

## 🧪 Tests

Validez l'implémentation avec la suite de tests :

```bash
python test_game.py
```

Inclut les vérifications de:
- ✓ Calcul des modificateurs
- ✓ Création des héros avec bonus corrects
- ✓ Création des monstres et génération de butin
- ✓ Mécanique de combat
- ✓ Placement des monstres et adjacence
- ✓ Initialisation du jeu complet

---

## 📊 Exemple de Session

```
╔════════════════════════════════════════╗
║     HEROES vs MONSTERS                 ║
║     Forêt de Shorewood                 ║
║     Stormwall                          ║
╚════════════════════════════════════════╝

Choose your hero:

1. Human  [+1 Strength, +1 Endurance]
2. Dwarf  [+2 Endurance]

Enter your choice (1 or 2): 1
Enter your hero's name: Aragorn

Welcome, Aragorn!
You are a Human.
Stats: Strength=16, Endurance=13, HP=14

[Affichage de la grille de jeu]

> d           # Aller à l'Est
Moved to (8, 7).

> d
Moved to (9, 7).

> d
Moved to (10, 7). Combat with Orc!

[Combat automatique démarre]
Round 1: Aragorn strikes Orc for 4 damage! Orc HP: 8/13
Round 1: Orc counterattacks Aragorn for 2 damage! Aragorn HP: 12/14
...
Victory! Aragorn defeated Orc!
  Collected: Gold(6)
  Aragorn rests and heals to full HP (14)

[Continuez jusqu'à victoire ou défaite]
```

---

## 🏗️ Décisions de Design

### OOP & Architecture

- **Héritage**: `Character` → `Hero`/`Monster` → types spécifiques
- **Polymorphisme**: Méthodes `strike()`, `generate_loot()`, `get_symbol()` surchargées
- **Encapsulation**: Attributs privés protégés, accesseurs/mutateurs
- **Type Hints**: Annotations complètes pour clarté et détection d'erreurs
- **Docstrings**: Chaque classe/méthode documentée

### Séparation des Préoccupations

- **dice.py**: Pures utilitaires de dés
- **character.py**: Logique de base (modificateurs, PV, frappe)
- **heroes.py** / **monsters.py**: Spécialisations avec bonus et butin
- **game.py**: Moteur (Combat, Board, Game)
- **main.py**: Interface utilisateur et boucle de jeu

### Flexibilité

- Facile d'ajouter de nouveaux héros/monstres
- Système de loot extensible
- Combat peut être étendu (initiative, compétences, etc.)

---

## 📚 Concepts POO Illustrés

1. **Classe & Objet**: Character, Hero, Monster, Loot
2. **Héritage**: Hero et Monster héritent de Character
3. **Polymorphisme**: Méthodes surchargées selon le type
4. **Encapsulation**: Attributs privés, interface publique
5. **Abstraction**: Classe abstraite Character avec méthodes abstraites
6. **Composition**: Game contient Board qui contient Hero et Monsters
7. **Type Hints**: Annotations de types pour la sécurité
8. **Docstrings**: Documentation intégrée aux classes

---

## 🐛 Gestion d'Erreurs

- ✓ Validation des positions (limites grille)
- ✓ Gestion des entrées invalides
- ✓ Détection des conditions de jeu terminé
- ✓ Sécurité des dégâts (minimum 1)

---

## 📝 Notes d'Implémentation

### Génération de Caractéristiques
```python
# 4d6, garder les 3 meilleurs
characteristic = sum(sorted(roll_dice(4, 6))[1:])  # Exclut le plus faible
```

### Calcul des Dégâts
```python
damage = roll_d4() + calculate_modifier(attacker.strength)
damage = max(1, damage)  # Minimum 1 dégât
```

### Distance sur la Grille
```python
# Distance de Chebyshev (max de dx, dy) pour l'espacement
# Distance de Manhattan (dx + dy = 1) pour l'adjacence
```

### Affichage de la Grille
```python
# H : Héro à sa position
# L/O/D : Monstres découverts (visibles)
# ? : Monstres cachés
# . : Case vide
```

---

## 🎓 Pour Apprendre

Ce projet est une excellente base pour explorer:
- Conception OOP avec Python
- Patterns de design (Observer, State, Strategy)
- Tests unitaires (pytest)
- Documentation (docstrings, type hints)
- Gestion d'état dans les applications interactives

---

## 🔥 Améliorations Possibles

- [ ] Initiative basée sur Agilité
- [ ] Compétences spéciales par héros
- [ ] Système d'expérience et de niveaux
- [ ] Sauvegarde/Charger partie
- [ ] UI graphique (Pygame)
- [ ] Écran de santé animé
- [ ] Bruits et musique
- [ ] Mode multijoueur

---

## 📜 Licence

Exercice pédagogique - Libre d'utilisation et de modification pour la formation.

---

**Bon amusement dans la forêt de Shorewood! 🌲⚔️**
