[🇫🇷 Français](README.fr.md) | [🇬🇧 English](README.md)

# Échecs pour NumWorks

Un jeu d'échecs à deux joueurs écrit en MicroPython pour la calculatrice graphique [NumWorks](https://www.numworks.com/). Le jeu tient dans un seul script (`chess.py`, environ 20 Ko) : le plateau, les pièces, la validation des coups et la détection de fin de partie sont entièrement dessinés et calculés par la calculatrice elle-même.

Page du script : <https://my.numworks.com/python/leandre-hiron-latourte/chess>

## Fonctionnalités

- Plateau 8×8 complet, avec des sprites de 20×20 pixels dessinés à la main pour les douze pièces
- Génération des coups légaux pour chaque pièce, en écartant ceux qui laisseraient votre propre roi en échec
- Coups spéciaux : **roque**, **prise en passant** et **promotion** du pion (avec un menu de choix)
- Mise en évidence des cases d'arrivée légales de la pièce sélectionnée
- Détection de l'**échec et mat** et du **pat**, avec affichage du résultat à l'écran
- Déplacement fluide du curseur grâce à un délai entre deux mouvements

## Installation

1. Ouvrez la [page du script](https://my.numworks.com/python/leandre-hiron-latourte/chess).
2. Envoyez le script vers votre calculatrice depuis votre compte NumWorks (connexion USB), ou copiez-le dans l'application Python du [simulateur en ligne](https://www.numworks.com/emulator/graphing/) (les touches ne vont pas marcher sur le simulateur).
3. Sur la calculatrice, ouvrez l'application **Python**, sélectionnez `chess.py` et lancez-le.

Le script n'utilise que les modules disponibles sur la NumWorks : `kandinsky` (dessin), `ion` (clavier) et `time`.

## Comment jouer

Les Blancs jouent en premier, puis les joueurs se relaient sur la même calculatrice.

| Touche | Action |
|--------|--------|
| Flèches | Déplacer le curseur vert |
| OK | Sélectionner l'une de vos pièces, puis appuyer de nouveau sur OK sur une case en surbrillance pour la déplacer |
| OK sur une autre case | Désélectionner la pièce en cours |
| ↑ / ↓ puis OK | Choisir une pièce dans le menu de promotion |

Une fois une pièce sélectionnée, ses cases d'arrivée légales sont entourées en rose. Après chaque coup, le curseur revient au centre du plateau pour le joueur suivant.

Lorsqu'un pion atteint la dernière rangée, un menu apparaît à gauche de l'écran : choisissez une dame, une tour, un fou ou un cavalier avec les flèches haut et bas, puis validez avec OK.

À la fin de la partie, l'écran affiche soit `WHITE WON` / `BLACK WON` en cas d'échec et mat, soit `DRAW` en cas de pat. Pour rejouer, relancez le script.

## Fonctionnement

- **Sprites :** chaque pièce est une liste de 20 entiers, un par ligne de pixels. Chaque entier est un nombre de 20 chiffres en base 3 (`0` transparent, `1` noir, `2` blanc), décodé au moment de dessiner la pièce. Cela garde les sprites compacts dans la mémoire limitée de la calculatrice.
- **Plateau :** une liste plate de 64 chaînes (`""` pour une case vide, sinon la couleur suivie de la pièce, par exemple `"WK"` ou `"BP"`). Les cases sont indexées par `col + row * 8`.
- **Génération des coups :** une fonction `gen_*_moves` par type de pièce. Tous les coups candidats sont ensuite testés sur une copie du plateau avec `is_king_in_check`, et ceux qui exposent le roi sont retirés.
- **Affichage :** le plateau est dessiné avec `kandinsky`, sur des cases de 22×22 pixels. La variable `angle` (de 0 à 3) contrôle l'orientation du plateau et vaut 0 par défaut.
- **Boucle principale :** `input_engine` gère les touches et le déroulement des tours, et `game_ends` affiche le résultat final.

## Limitations connues

- Jeu à deux joueurs en local uniquement : il n'y a ni adversaire informatique, ni annulation de coup, ni pendule.
- Seul le pat est détecté comme partie nulle. La triple répétition, la règle des cinquante coups et le matériel insuffisant ne sont pas gérés.
- Le suivi des droits de roque est incomplet : déplacer une tour ne fait pas perdre le droit de roquer, si bien que le roque peut être autorisé ou refusé à tort dans certaines positions.
- Il n'y a pas d'option pour recommencer : relancez le script pour démarrer une nouvelle partie.

## Structure du projet

```
chess.py    Tout le jeu (sprites, affichage, règles, gestion des touches)
```