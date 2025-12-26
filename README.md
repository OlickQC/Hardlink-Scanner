# Hardlink TV Shows Scanner

Scans a TV media library and reports video files that are **not hardlinked**. Designed for Linux/Unraid media servers.

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

---

# Analyseur de Hardlinks pour Séries TV

Analyse une bibliothèque de médias TV et génère un rapport des fichiers vidéo qui ne sont **pas en hardlink**. Conçu pour les serveurs Linux/Unraid.

---

## Démarrage Rapide

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

## Liste d'Exclusion

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

