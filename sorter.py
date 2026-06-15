#!/usr/bin/env python3
"""
Arch File Sorter - CLI Automation Tool
Trie automatiquement les fichiers d'un dossier selon leur extension.
"""

from pathlib import Path          # Manipulation moderne des chemins (objets, cross-platform)
import argparse                   # Pour gérer les arguments en ligne de commande
import shutil                     # Pour déplacer les fichiers (shutil.move)

# Dictionnaire associant un nom de dossier de destination à une liste d'extensions
FILE_MAPPING = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".md"],
    "Archives": [".zip", ".tar.gz", ".tar.xz", ".rar"],
    "Scripts": [".sh", ".py", ".pl",".js",".ts",".php"],
}

# Fichiers/dossiers à ne jamais déplacer (le script lui-même, son venv, etc.)
IGNORED_NAMES = {"sorter.py", ".venv", "sorter.log", ".git", ".gitignore", "__pycache__"}


def get_destination_folder(extension: str) -> str:
    """
    Reçoit une extension (ex: '.png') et renvoie le nom du dossier cible.
    Si l'extension n'est dans aucune catégorie, renvoie 'Autres'.
    """
    extension = extension.lower()  # Normalise en minuscules (.PNG -> .png)
    for folder_name, extensions in FILE_MAPPING.items():
        if extension in extensions:
            return folder_name
    return "Autres"


def get_unique_destination(destination_path: Path) -> Path:
    """
    Si destination_path existe déjà, génère un nouveau nom avec un suffixe _1, _2, etc.
    Sinon renvoie le chemin tel quel.
    """
    if not destination_path.exists():
        return destination_path

    # Sépare le nom de base et l'extension (gère aussi les doubles extensions comme .tar.gz)
    stem = destination_path.stem       # nom sans la dernière extension
    suffix = destination_path.suffix   # dernière extension
    parent = destination_path.parent
    counter = 1

    # Boucle jusqu'à trouver un nom de fichier qui n'existe pas encore
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def scan_directory(target_dir: str, dry_run: bool = False):
    """
    Parcourt le dossier cible, trie les fichiers dans des sous-dossiers
    selon leur extension, et affiche un rapport final.
    """
    path = Path(target_dir).expanduser()  # Convertit '~' en chemin absolu (/home/user/...)

    # Vérifie que le dossier existe avant de continuer
    if not path.exists():
        print(f"❌ Le dossier {path} n'existe pas.")
        return

    # Dictionnaire pour compter les fichiers déplacés par catégorie
    stats = {}
    total_size = 0  # Taille totale réorganisée, en octets

    # Parcourt uniquement les éléments du dossier (pas les sous-dossiers récursivement)
    for item in path.iterdir():

        # Ignore les dossiers (on ne trie que les fichiers)
        if not item.is_file():
            continue

        # Ignore le script lui-même, son venv, son log, etc.
        if item.name in IGNORED_NAMES:
            continue

        # Récupère l'extension du fichier (ex: '.png')
        extension = item.suffix

        # Détermine le dossier de destination selon l'extension
        folder_name = get_destination_folder(extension)

        # Construit le chemin complet du dossier de destination
        destination_dir = path / folder_name

        # Construit le chemin complet du fichier de destination
        destination_file = destination_dir / item.name

        # Évite d'écraser un fichier existant en générant un nom unique si besoin
        destination_file = get_unique_destination(destination_file)

        # Récupère la taille du fichier en octets (pour le rapport final)
        file_size = item.stat().st_size

        if dry_run:
            # Mode simulation : affiche l'action sans rien déplacer
            print(f"[DRY-RUN] {item.name} -> {folder_name}/{destination_file.name}")
        else:
            # Crée le dossier de destination s'il n'existe pas
            # parents=True : crée les dossiers parents si nécessaire
            # exist_ok=True : ne plante pas si le dossier existe déjà
            destination_dir.mkdir(parents=True, exist_ok=True)

            # Déplace réellement le fichier vers sa destination
            shutil.move(str(item), str(destination_file))

            print(f"✅ {item.name} -> {folder_name}/{destination_file.name}")

        # Met à jour les statistiques (compteur par catégorie)
        stats[folder_name] = stats.get(folder_name, 0) + 1
        total_size += file_size

    # Affiche le rapport final
    print_report(stats, total_size, dry_run)


def print_report(stats: dict, total_size: int, dry_run: bool):
    """
    Affiche un résumé textuel du tri effectué (ou simulé).
    """
    print("\n" + "=" * 40)
    if dry_run:
        print("📊 RAPPORT (SIMULATION)")
    else:
        print("📊 RAPPORT DE TRI")
    print("=" * 40)

    total_files = sum(stats.values())  # Somme de tous les fichiers traités

    if total_files == 0:
        print("Aucun fichier à trier.")
        return

    # Affiche le détail par catégorie
    for folder_name, count in stats.items():
        word = "fichier déplacé" if count == 1 else "fichiers déplacés"
        print(f"  {folder_name} : {count} {word}")

    print("-" * 40)
    print(f"Total : {total_files} fichier(s)")

    # Convertit la taille totale en Mo pour un affichage plus lisible
    size_mb = total_size / (1024 * 1024)
    print(f"Espace réorganisé : {size_mb:.2f} Mo")
    print("=" * 40)


def main():
    """
    Point d'entrée du script : parse les arguments CLI et lance le tri.
    """
    # Crée le parseur d'arguments avec une description affichée via --help
    parser = argparse.ArgumentParser(
        description="Un trieur de fichiers automatisé pour Arch Linux."
    )

    # Argument --target : dossier à trier, avec valeur par défaut ~/Downloads
    parser.add_argument(
        "--target",
        type=str,
        default="~/Downloads",
        help="Le dossier à trier (par défaut : ~/Downloads)"
    )

    # Argument --dry-run : flag booléen (présent = True, absent = False)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simuler le tri sans déplacer les fichiers"
    )

    # Lit les arguments passés en ligne de commande
    args = parser.parse_args()

    # Lance le tri avec les paramètres choisis
    scan_directory(args.target, dry_run=args.dry_run)


# Exécute main() seulement si le script est lancé directement (pas importé)
if __name__ == "__main__":
    main()