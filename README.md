# Arch File Sorter - CLI Automation Tool

Un outil en ligne de commande écrit en Python pour trier automatiquement les fichiers d'un dossier (par défaut `~/Downloads`) selon leur type, en les déplaçant dans des sous-dossiers organisés (Images, Documents, Archives, Scripts, Autres).

## Pourquoi ce projet ?

Le dossier Téléchargements devient vite un fourre-tout ingérable. Plutôt que de trier manuellement, ce script automatise le rangement en se basant sur l'extension de chaque fichier. C'est aussi un projet pensé pour découvrir et pratiquer :

- `pathlib` pour la manipulation de chemins moderne et cross-platform
- `argparse` pour construire une vraie interface CLI
- La gestion des doublons et des cas limites (fichiers déjà existants, fichiers à ignorer)

## Fonctionnalités

- Tri automatique par type de fichier (Images, Documents, Archives, Scripts, Autres)
- Gestion des doublons : un fichier existant n'est jamais écrasé (renommage automatique en `nom_1.ext`, `nom_2.ext`, etc.)
- Mode simulation (`--dry-run`) pour visualiser les actions sans rien déplacer
- Rapport final détaillé (nombre de fichiers triés par catégorie, espace réorganisé)
- Aucune dépendance externe : 100% bibliothèque standard Python

## Prérequis

- Python 3.8 ou supérieur

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/Ldrekoh/file-sorter.git
cd file-sorter

# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement virtuel
source .venv/bin/activate
```

Aucune dépendance externe à installer : le script repose uniquement sur la bibliothèque standard Python.

## Utilisation

### Simulation (recommandé avant un vrai tri)

```bash
python sorter.py --target ~/Downloads --dry-run
```

Affiche les actions qui seraient effectuées, sans déplacer aucun fichier :

```
[DRY-RUN] photo.png -> Images/photo.png
[DRY-RUN] rapport.pdf -> Documents/rapport.pdf
[DRY-RUN] archive.zip -> Archives/archive.zip
```

### Tri réel

```bash
python sorter.py --target ~/Downloads
```

### Trier un autre dossier

```bash
python sorter.py --target ~/Desktop
```

### Options disponibles

| Option       | Description                                              | Valeur par défaut |
|--------------|-----------------------------------------------------------|--------------------|
| `--target`   | Dossier à trier                                            | `~/Downloads`      |
| `--dry-run`  | Simule le tri sans déplacer les fichiers                   | désactivé          |

## Exemple de rapport final

```
========================================
📊 RAPPORT DE TRI
========================================
  Images : 12 fichiers déplacés
  Documents : 5 fichiers déplacés
  Archives : 2 fichiers déplacés
----------------------------------------
Total : 19 fichier(s)
Espace réorganisé : 134.52 Mo
========================================
```

## Catégories de tri

| Catégorie  | Extensions                                  |
|------------|----------------------------------------------|
| Images     | `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`      |
| Documents  | `.pdf`, `.docx`, `.txt`, `.xlsx`, `.md`      |
| Archives   | `.zip`, `.tar.gz`, `.tar.xz`, `.rar`         |
| Scripts    | `.sh`, `.py`, `.pl`                           |
| Autres     | Tout fichier ne correspondant à aucune extension ci-dessus |

## Limitations connues

- Le tri n'est pas récursif (seuls les fichiers à la racine du dossier ciblé sont traités)
- Le script, son environnement virtuel et son fichier de log sont automatiquement ignorés s'ils se trouvent dans le dossier ciblé

## Licence

MIT
