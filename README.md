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
us/Breaking Bad/Season 05/Breaking Bad - S05E14 - Ozymandias.mp4
```

## Output

- **Report:** `reports/non_hardlinked_tv_episodes_{timestamp}.txt`  
- **Logs:** `reports/logs_{timestamp}.txt`

Both files include timestamps and scan statistics.

