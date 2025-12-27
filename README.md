## Hardlink TV Shows & Movies Scanner
[EN] Scans a TV media library and reports video files that are **not hardlinked**. Designed for Linux/Unraid media servers.

[FR] Analyse une bibliothèque de médias TV et génère un rapport des fichiers vidéo qui ne sont **pas en hardlink**. Conçu pour les serveurs Linux/Unraid.

## 📝 Table of Contents

- English
  - [Hardlink TV Shows Scanner (English)](#hardlink-tv-shows-scanner-english)
  - [Why This Matters](#why-this-matters)
  - [What is a Hardlink?](#what-is-a-hardlink)
  - [Quick Start](#quick-start)
  - [Configuration](#configuration)
  - [Exclusion List](#exclusion-list)
  - [Output](#output)
  - [Cleanup (Sonarr/Radarr)](#cleanup-sonarrradarr)

- Français
  - [Hardlink TV Shows Scanner (Français)](#hardlink-tv-shows-scanner-english)
  - [Pourquoi c'est important](#pourquoi-cest-important)
  - [Qu'est-ce qu'un Hardlink ?](#quest-ce-quun-hardlink-)
  - [Démarrage rapide](#démarrage-rapide)
  - [Configuration](#configuration-1)
  - [Liste d'exclusion](#liste-dexclusion)
  - [Résultats](#résultats)
  - [Nettoyage (Sonarr/Radarr)](#nettoyage-sonarrradarr)

## 💡 Why This Matters

**Sonarr** and **Radarr** can create hardlinks to save disk space by making multiple directory entries pointing to the same physical file. However, hardlinks can break for various reasons:
- Moving files between filesystems
- Manual file operations
- Filesystem corruption

When a hardlink breaks, the file is duplicated on disk, wasting valuable storage. This script identifies these broken hardlinks so you can clean them up.

### What is a Hardlink?

A hardlink is a direct reference to a file's data on disk. Instead of copying a file (which doubles the storage), a hardlink creates another name pointing to the **same physical data**. It's invisible to users but saves disk space. One file, multiple paths.

## 🚀 Quick Start

1. Edit `config/config.json` - set your TV library path in `root_dir`
2. Run: `python3 scan.py`
3. Check results in `reports/non_hardlinked_tv_episodes_{timestamp}.txt`

## 🛠️Configuration

**config/config.json:**
```json
{
  "root_dir": "/mnt/user/data/media/tv",
  "root_dir_movies": "/mnt/user/data/media/movies",
  "enabled_tv": true,
  "enabled_movies": true,
  "exclusion_tv_file": "exclusion_tv.txt",
  "exclusion_movies_file": "exclusion_movies.txt",
  "video_extensions": [".mkv", ".mp4"],
  "verbose": true
}
```

**Config options:**
| Key | Description |
|---|---|
| `root_dir` | Root directory of your TV library |
| `root_dir_movies` | Root directory of your Movies library |
| `enabled_tv` | Enable/disable TV shows scan (default: `true`) |
| `enabled_movies` | Enable/disable movies scan (default: `true`) |
| `exclusion_tv_file` | Exclusion file for TV shows (default: `exclusion_tv.txt`) |
| `exclusion_movies_file` | Exclusion file for movies (default: `exclusion_movies.txt`) |
| `video_extensions` | File extensions to scan |

**Relocate config/reports folders** (optional):  
Edit these variables at the top of `scan.py`:
```python
CONFIG_DIR_OVERRIDE = "/custom/path/to/config"
REPORTS_DIR_OVERRIDE = "/custom/path/to/reports"
```

## 🚫 Exclusion List

Add files to ignore in `config/exclusion_tv.txt` for TV shows and `config/exclusion_movies.txt` for movies (one per line, relative to respective root directories).  
**Use the same path format as shown in the reports.**

Example for TV (`exclusion_tv.txt`):
```
# Ignore these specific episodes
us/Better Call Saul - Employee Training (2017) [tvdbid-365403]/Season 01/Better Call Saul - Employee Training (2017) - S01E01.mkv
```

Example for Movies (`exclusion_movies.txt`):
```
# Ignore these specific movies
us/Movie Title (2020)/Movie Title (2020).mkv
```

## ✅ Output

- **TV Report:** `reports/non_hardlinked_tv_episodes_{timestamp}.txt`  
- **Movies Report:** `reports/non_hardlinked_movies_{timestamp}.txt`  
- **Logs:** `reports/logs_{timestamp}.txt`

Both reports include timestamps and scan statistics.

## 🧼 Cleanup (Sonarr/Radarr)

To rebuild hardlinks with Sonarr:
- Go to: **Wanted** → **Manual Import**
- Pick the folder where the files were downloaded
- **Interactive Import**
- Match each Relative Path to the correct Series and Episodes
- At the bottom-left dropdown, pick: **Hardlink/Copy files**
- Click **Import**

Sonarr will rebuild the hardlinks for that show. The process is the same with Radarr.

---

## 💡 Pourquoi c'est important

**Sonarr** et **Radarr** peuvent créent des hardlinks pour économiser l'espace disque en créant plusieurs entrées de répertoire pointant vers le même fichier physique. Cependant, les hardlinks peuvent se rompre pour diverses raisons:
- Déplacement de fichiers entre systèmes de fichiers
- Opérations manuelles sur les fichiers
- Corruption du système de fichiers

Quand un hardlink se rompt, le fichier est dupliqué sur le disque, gaspillant de l'espace de stockage précieux. Ce script identifie ces hardlinks rompus pour que vous puissiez les nettoyer.

### Qu'est-ce qu'un Hardlink ?

Un hardlink est une référence directe aux données d'un fichier sur le disque. Au lieu de copier un fichier (ce qui doublerait le stockage), un hardlink crée un autre nom pointant vers les **mêmes données physiques**. C'est invisible pour l'utilisateur mais économise l'espace disque. Un fichier, plusieurs chemins.

## 🚀 Démarrage rapide

1. Modifiez `config/config.json` - définissez le chemin de votre bibliothèque TV dans `root_dir`
2. Exécutez : `python3 scan.py`
3. Vérifiez les résultats dans `reports/non_hardlinked_tv_episodes_{timestamp}.txt`

## 🛠️ Configuration

**config/config.json:**
```json
{
  "root_dir": "/mnt/user/data/media/tv",
  "root_dir_movies": "/mnt/user/data/media/movies",
  "enabled_tv": true,
  "enabled_movies": true,
  "exclusion_tv_file": "exclusion_tv.txt",
  "exclusion_movies_file": "exclusion_movies.txt",
  "video_extensions": [".mkv", ".mp4"],
  "verbose": true
}
```

**Options de configuration :**
| Clé | Description |
|---|---|
| `root_dir` | Répertoire racine de votre bibliothèque TV |
| `root_dir_movies` | Répertoire racine de votre bibliothèque de films |
| `enabled_tv` | Activer/désactiver l'analyse TV (défaut: `true`) |
| `enabled_movies` | Activer/désactiver l'analyse des films (défaut: `true`) |
| `exclusion_tv_file` | Fichier d'exclusion pour les séries TV (défaut: `exclusion_tv.txt`) |
| `exclusion_movies_file` | Fichier d'exclusion pour les films (défaut: `exclusion_movies.txt`) |
| `video_extensions` | Extensions de fichiers à analyser |

**Relocalisez les dossiers config/reports** (optionnel) :  
Modifiez ces variables en haut de `scan.py`:
```python
CONFIG_DIR_OVERRIDE = "/custom/path/to/config"
REPORTS_DIR_OVERRIDE = "/custom/path/to/reports"
```

## 🚫 Liste d'exclusion

Ajoutez les fichiers à ignorer dans `config/exclusion_tv.txt` pour les séries TV et `config/exclusion_movies.txt` pour les films (un par ligne, relatif aux répertoires respectifs).  
**Utilisez le même format de chemin que celui affiché dans les rapports.**

Exemple pour les séries TV (`exclusion_tv.txt`):
```
# Ignorer ces épisodes spécifiques
us/Better Call Saul - Employee Training (2017) [tvdbid-365403]/Season 01/Better Call Saul - Employee Training (2017) - S01E01.mkv
```

Exemple pour les films (`exclusion_movies.txt`):
```
# Ignorer ces films spécifiques
us/Movie Title (2020)/Movie Title (2020).mkv
```

## ✅ Résultats

- **Rapport TV :** `reports/non_hardlinked_tv_episodes_{timestamp}.txt`  
- **Rapport Films :** `reports/non_hardlinked_movies_{timestamp}.txt`  
- **Journaux :** `reports/logs_{timestamp}.txt`

Les deux fichiers incluent des horodatages et des statistiques de scan.

## 🧼 Nettoyage (Sonarr/Radarr)

Pour reconstruire les hardlinks avec Sonarr :
- **Recherché** → **Importation manuelle**
- Choisir le dossier où les fichiers ont été téléchargés
- **Importation interactive**
- Faire concorder le Chemin Relatif à la Série, Saison et Épisodes
- En bas à gauche (menu déroulant), choisir : **Lien physique/Copie de fichiers**
- **Importer**

Sonarr reconstruira les hardlinks pour cette série. Le processus est le même avec Radarr.