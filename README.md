## Table of Contents

- English
  - [Hardlink TV Shows Scanner (English)] (#hardlink-tv-shows-scanner-english)
  - [Why This Matters](#why-this-matters)
  - [What is a Hardlink?](#what-is-a-hardlink)
  - [Quick Start](#quick-start)
  - [Configuration](#configuration)
  - [Exclusion List](#exclusion-list)
  - [Output](#output)
  - [Cleanup (Sonarr/Radarr)](#cleanup-sonarrradarr)

- Français
  - [Hardlink TV Shows Scanner (Français)] (#hardlink-tv-shows-scanner-english)
  - [Pourquoi c'est important](#pourquoi-cest-important)
  - [Qu'est-ce qu'un Hardlink ?](#quest-ce-quun-hardlink-)
  - [Démarrage rapide](#démarrage-rapide)
  - [Configuration](#configuration-1)
  - [Liste d'exclusion](#liste-dexclusion)
  - [Résultats](#résultats)
  - [Nettoyage (Sonarr/Radarr)](#nettoyage-sonarrradarr)

# Hardlink TV Shows Scanner (English)

Scans a TV media library and reports video files that are **not hardlinked**. Designed for Linux/Unraid media servers.

## Why This Matters

**Sonarr** and **Radarr** can create hardlinks to save disk space by making multiple directory entries pointing to the same physical file. However, hardlinks can break for various reasons:
- Moving files between filesystems
- Manual file operations
- Filesystem corruption

When a hardlink breaks, the file is duplicated on disk, wasting valuable storage. This script identifies these broken hardlinks so you can clean them up.

### What is a Hardlink?

A hardlink is a direct reference to a file's data on disk. Instead of copying a file (which doubles the storage), a hardlink creates another name pointing to the **same physical data**. It's invisible to users but saves disk space. One file, multiple paths.

## Quick Start

1. Edit `config/config.json` - set your TV library path in `root_dir`
2. Run: `python3 scan.py`
3. Check results in `reports/non_hardlinked_tv_episodes_{timestamp}.txt`

## Configuration

**config/config.json:**
```json
{
  "root_dir": "/mnt/user/data/media/tv",
  "exclusion_file": "exclusion.txt",
  "video_extensions": [".mkv", ".mp4"],
  "verbose": true
}
```

**Relocate config/reports folders** (optional):  
Edit these variables at the top of `scan.py`:
```python
CONFIG_DIR_OVERRIDE = "/custom/path/to/config"
REPORTS_DIR_OVERRIDE = "/custom/path/to/reports"
```

## Exclusion List

Add files to ignore in `config/exclusion.txt` (one per line, relative to `root_dir`).  
**Use the same path format as shown in the reports.**

Example:
```
# Ignore these specific episodes
us/Better Call Saul - Employee Training (2017) [tvdbid-365403]/Season 01/Better Call Saul - Employee Training (2017) - S01E01.mkv
```

## Output

- **Report:** `reports/non_hardlinked_tv_episodes_{timestamp}.txt`  
- **Logs:** `reports/logs_{timestamp}.txt`

Both files include timestamps and scan statistics.

## Cleanup (Sonarr/Radarr)

To rebuild hardlinks with Sonarr:
- Go to: **Wanted** → **Manual Import**
- Pick the folder where the files were downloaded
- **Interactive Import**
- Match each Relative Path to the correct Series and Episodes
- At the bottom-left dropdown, pick: **Hardlink/Copy files**
- Click **Import**

Sonarr will rebuild the hardlinks for that show. The process is the same with Radarr.

---

# Hardlink TV Shows Scanner (Français)

Analyse une bibliothèque de médias TV et génère un rapport des fichiers vidéo qui ne sont **pas en hardlink**. Conçu pour les serveurs Linux/Unraid.

## Pourquoi c'est important

**Sonarr** et **Radarr** peuvent créent des hardlinks pour économiser l'espace disque en créant plusieurs entrées de répertoire pointant vers le même fichier physique. Cependant, les hardlinks peuvent se rompre pour diverses raisons:
- Déplacement de fichiers entre systèmes de fichiers
- Opérations manuelles sur les fichiers
- Corruption du système de fichiers

Quand un hardlink se rompt, le fichier est dupliqué sur le disque, gaspillant de l'espace de stockage précieux. Ce script identifie ces hardlinks rompus pour que vous puissiez les nettoyer.

### Qu'est-ce qu'un Hardlink ?

Un hardlink est une référence directe aux données d'un fichier sur le disque. Au lieu de copier un fichier (ce qui doublerait le stockage), un hardlink crée un autre nom pointant vers les **mêmes données physiques**. C'est invisible pour l'utilisateur mais économise l'espace disque. Un fichier, plusieurs chemins.

## Démarrage rapide

1. Modifiez `config/config.json` - définissez le chemin de votre bibliothèque TV dans `root_dir`
2. Exécutez : `python3 scan.py`
3. Vérifiez les résultats dans `reports/non_hardlinked_tv_episodes_{timestamp}.txt`

## Configuration

**config/config.json:**
```json
{
  "root_dir": "/mnt/user/data/media/tv",
  "exclusion_file": "exclusion.txt",
  "video_extensions": [".mkv", ".mp4"],
  "verbose": true
}
```

**Relocalisez les dossiers config/reports** (optionnel) :  
Modifiez ces variables en haut de `scan.py`:
```python
CONFIG_DIR_OVERRIDE = "/custom/path/to/config"
REPORTS_DIR_OVERRIDE = "/custom/path/to/reports"
```

## Liste d'exclusion

Ajoutez les fichiers à ignorer dans `config/exclusion.txt` (un par ligne, relatif à `root_dir`).  
**Utilisez le même format de chemin que celui affiché dans les rapports.**

Exemple :
```
# Ignorer ces épisodes spécifiques
us/Better Call Saul - Employee Training (2017) [tvdbid-365403]/Season 01/Better Call Saul - Employee Training (2017) - S01E01.mkv
```

## Résultats

- **Rapport :** `reports/non_hardlinked_tv_episodes_{timestamp}.txt`  
- **Journaux :** `reports/logs_{timestamp}.txt`

Les deux fichiers incluent des horodatages et des statistiques de scan.

## Nettoyage (Sonarr/Radarr)

Pour reconstruire les hardlinks avec Sonarr :
- **Recherché** → **Importation manuelle**
- Choisir le dossier où les fichiers ont été téléchargés
- **Importation interactive**
- Faire concorder le Chemin Relatif à la Série, Saison et Épisodes
- En bas à gauche (menu déroulant), choisir : **Lien physique/Copie de fichiers**
- **Importer**

Sonarr reconstruira les hardlinks pour cette série. Le processus est le même avec Radarr.

