# Hardlink TV Shows Scanner

A Python utility to scan a TV media library and generate a report of video files that are **not hardlinked**, grouped by TV show.

This tool is designed for Linux / Unraid / media-server environments where hardlinks are expected (Sonarr, torrent seeding setups, etc.).

---

## Why this exists

In a proper media setup:
- Torrented files are hardlinked into the library
- One physical file can have multiple directory entries
- Disk space is saved

If a file has **no hardlinks**, it often means:
- It was copied instead of hardlinked
- It broke out of the seeding workflow
- It is wasting disk space

This script helps you **audit and detect those files**.

---

## Features

- Recursively scans a TV library
- Detects non-hardlinked video files (`st_nlink == 1`)
- Groups results by **TV show title**
- Supports an exclusion list
- Uses a JSON configuration file
- Generates timestamped reports
- Optional verbose mode
- Read-only (never modifies files)

---

## Project Structure

```
Hardlink-checker/
├─ scan.py
├─ README.md
├─ config/
│  ├─ config.json
│  └─ exclusion.txt
└─ reports/
   └─ non_hardlinked_tv_episodes_YYYY-MM-DD_HH-MM.txt
```

---

## Configuration

### `config/config.json`

```json
{
  "root_dir": "/mnt/user/data/media/tv",
  "exclusion_file": "exclusion.txt",
  "video_extensions": [
    ".mkv",
    ".mp4"
  ],
  "reports_dir": "/reports",
  "verbose": true
}
```

### Configuration options

| Key | Description |
|---|---|
| `root_dir` | Root directory of your TV library |
| `exclusion_file` | Exclusion list filename (relative to `/config`) |
| `video_extensions` | File extensions to scan |
| `reports_dir` | Directory where reports are written |

---

## Exclusion List

### `config/exclusion.txt`

- One file path per line
- Paths are **relative to `root_dir`**
- Blank lines are ignored
- Lines starting with `#` are comments

Example:

```
# Ignore special training videos
us/Better Call Saul - Employee Training (2017) [tvdbid-365403]/Season 01/Better Call Saul - Employee Training (2017) - S01E01.mp4
us/Better Call Saul - Employee Training (2017) [tvdbid-365403]/Season 01/Better Call Saul - Employee Training (2017) - S01E02.mp4
```

---

## How TV Shows Are Grouped

The script assumes this directory structure:

```
category/Show Title/Season XX/episode.mkv
```

---

## Report Output

Reports are written to the directory defined by `reports_dir`
and include a timestamp in the filename.

Example filename:

```
non_hardlinked_tv_episodes_2025-12-24_06-29.txt
```

---

## Running the Script

From the project directory:

```
python3 scan.py
```

The script will:
1. Load configuration
2. Load exclusions
3. Scan the filesystem
4. Generate a report

---

## Verbose Mode

Verbose mode prints detailed runtime information:
- Paths being used
- Number of files scanned
- Number of excluded files
- Number of non-hardlinked files
- Final report location

---

## Requirements

- Python 3.8+
- Linux filesystem supporting hardlinks (ext4, XFS, ZFS, btrfs)
- Read access to media library
- Write access to the reports directory

---

## Safety

- The script is **read-only**
- It does not modify, delete, or relink files
- It only reads filesystem metadata
