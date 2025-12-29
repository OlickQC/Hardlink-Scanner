#!/usr/bin/env python3
"""
Scan TV show directories and identify non-hardlinked video files.

"""

import json
import logging
import os
from collections import defaultdict
from datetime import datetime

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# THOSE ARE MODIFIABLE. Quick user overrides. Leave as None to use defaults.
CONFIG_DIR_OVERRIDE = None
REPORTS_DIR_OVERRIDE = None

# ---------------------------
# Configuration
# ---------------------------

# Base directory (script location)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Optional override for config directory via user setting or environment variable.
config_dir_setting = CONFIG_DIR_OVERRIDE or os.environ.get("HARDLINK_SCANNER_CONFIG_DIR")

if config_dir_setting:
    resolved_config_dir = os.path.expanduser(config_dir_setting)
    if not os.path.isabs(resolved_config_dir):
        resolved_config_dir = os.path.join(BASE_DIR, resolved_config_dir)
else:
    resolved_config_dir = os.path.join(BASE_DIR, "config")

CONFIG_DIR = os.path.normpath(resolved_config_dir)
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# Load configuration from JSON file
if not os.path.exists(CONFIG_FILE):
    raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

# Configuration values
VERBOSE = CONFIG.get("verbose", True)

# TV & Movies roots and enable switches
ROOT_DIR_TV = CONFIG["root_dir"]
ROOT_DIR_MOVIES = CONFIG.get("root_dir_movies")
ENABLED_TV = CONFIG.get("enabled_tv", True)
ENABLED_MOVIES = CONFIG.get("enabled_movies", False)

# Excluded directories (folders to skip during scan)
EXCLUDED_DIRS_TV = CONFIG.get("excluded_dirs_tv", [])
EXCLUDED_DIRS_MOVIES = CONFIG.get("excluded_dirs_movies", [])

# Exclusions (separate files, with sensible defaults)
EXCLUSION_TV_FILE = os.path.join(
    CONFIG_DIR,
    CONFIG.get("exclusion_tv_file", CONFIG.get("exclusion_file", "exclusion_tv.txt")),
)
EXCLUSION_MOVIES_FILE = os.path.join(
    CONFIG_DIR,
    CONFIG.get("exclusion_movies_file", "exclusion_movies.txt"),
)

VIDEO_EXTENSIONS = tuple(
    ext.lower() for ext in CONFIG["video_extensions"]
)
if REPORTS_DIR_OVERRIDE:
    resolved_reports_dir = os.path.expanduser(REPORTS_DIR_OVERRIDE)
    if not os.path.isabs(resolved_reports_dir):
        resolved_reports_dir = os.path.join(BASE_DIR, resolved_reports_dir)
else:
    resolved_reports_dir = os.path.join(BASE_DIR, "reports")

REPORTS_DIR = os.path.normpath(resolved_reports_dir)
os.makedirs(REPORTS_DIR, exist_ok=True)

# Generate timestamped report filenames
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M")
REPORT_FILE_TV = os.path.join(
    REPORTS_DIR,
    f"non_hardlinked_tv_episodes_{TIMESTAMP}.txt"
)
REPORT_FILE_MOVIES = os.path.join(
    REPORTS_DIR,
    f"non_hardlinked_movies_{TIMESTAMP}.txt"
)
LOG_FILE = os.path.join(REPORTS_DIR, f"logs_{TIMESTAMP}.txt")


def configure_logging(log_path):
    """Configure logging to console and a log file."""
    handlers = [
        logging.StreamHandler(),
        logging.FileHandler(log_path, encoding="utf-8"),
    ]

    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        handlers=handlers,
        force=True,
    )


# ---------------------------
# Functions
# ---------------------------


def load_exclusions(exclusion_file_path):
    """
    Load exclusion list from file.

    Args:
        exclusion_file_path (str): Path to the exclusion file.

    Returns:
        set: Set of excluded paths.
    """
    exclusions = set()
    if os.path.exists(exclusion_file_path):
        with open(exclusion_file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    exclusions.add(line)
    return exclusions


def scan_for_non_hardlinked_files(root_dir, video_exts, exclusions, excluded_dirs, group_index, unknown_label):
    """
    Scan directory for non-hardlinked video files.

    Args:
        root_dir (str): Root directory to scan.
        video_exts (tuple): Tuple of video file extensions to look for.
        exclusions (set): Set of excluded paths.
        excluded_dirs (list): List of directory paths to exclude from scan.
        group_index (int): Index for grouping files.
        unknown_label (str): Label for unknown groups.

    Returns:
        tuple: (non_hardlinked_dict, total_files, excluded_files,
                non_hardlinked_files)
    """
    non_hardlinked = defaultdict(list)
    total_files = 0
    excluded_files = 0
    non_hardlinked_files = 0

    logging.info("Starting filesystem scan...")

    for root, dirs, files in os.walk(root_dir):
        # Remove excluded directories from dirs to prevent os.walk from descending into them
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in excluded_dirs and os.path.relpath(os.path.join(root, d), root_dir) not in excluded_dirs]
        for file in files:
            if file.lower().endswith(video_exts):
                total_files += 1
                full_path = os.path.join(root, file)

                try:
                    stat = os.stat(full_path)
                except OSError:
                    continue

                if stat.st_nlink == 1:
                    relative_path = os.path.relpath(full_path, root_dir)

                    if relative_path in exclusions:
                        excluded_files += 1
                        continue

                    path_parts = relative_path.split(os.sep)
                    idx = group_index
                    # Ensure index is valid relative to parts length
                    if idx < 0:
                        needed = -idx
                    else:
                        needed = idx + 1
                    title = (
                        path_parts[idx]
                        if len(path_parts) >= needed
                        else unknown_label
                    )

                    non_hardlinked[title].append(relative_path)
                    non_hardlinked_files += 1

    logging.info("Scan complete")
    return (
        non_hardlinked,
        total_files,
        excluded_files,
        non_hardlinked_files,
    )


def write_report(report_path, non_hardlinked_data):
    """
    Write scan results to report file.

    Args:
        report_path (str): Path where the report will be written.
        non_hardlinked_data (dict): Dictionary of shows and their files.
    """
    logging.info("Writing report...")

    with open(report_path, "w", encoding="utf-8") as report:
        for show in sorted(non_hardlinked_data):
            report.write(f"{show}\n")
            report.write("-" * len(show) + "\n")

            for episode in sorted(non_hardlinked_data[show]):
                report.write(f"{episode}\n")

            report.write("\n\n")

    logging.info("Report written successfully")


def main():
    """
    Main entry point of the script.
    """
    configure_logging(LOG_FILE)

    logging.info("Script started")
    logging.info("-" * 40)
    logging.info("CONFIGURATION")
    logging.info("-" * 40)
    logging.info("Config directory: %s", CONFIG_DIR)
    logging.info("TV enabled: %s", ENABLED_TV)
    logging.info("Movies enabled: %s", ENABLED_MOVIES)
    logging.info("Reports directory: %s", REPORTS_DIR)
    logging.info("TV report file: %s", REPORT_FILE_TV)
    logging.info("Movies report file: %s", REPORT_FILE_MOVIES)
    logging.info("Logs file: %s", LOG_FILE)
    if ENABLED_TV and EXCLUDED_DIRS_TV:
        logging.info("Excluded TV directories: %d", len(EXCLUDED_DIRS_TV))
        for excluded_dir in EXCLUDED_DIRS_TV:
            logging.info("  - %s", excluded_dir)
    if ENABLED_MOVIES and EXCLUDED_DIRS_MOVIES:
        logging.info("Excluded Movies directories: %d", len(EXCLUDED_DIRS_MOVIES))
        for excluded_dir in EXCLUDED_DIRS_MOVIES:
            logging.info("  - %s", excluded_dir)
    logging.info("") # Spacer before switching to TV
    
    # TV scan
    if ENABLED_TV:
        logging.info("-" * 40)
        logging.info("TV SCAN")
        logging.info("-" * 40)
        logging.info("Root media directory (TV): %s", ROOT_DIR_TV)
        logging.info("Exclusion file (TV): %s", EXCLUSION_TV_FILE)
        tv_exclusions = load_exclusions(EXCLUSION_TV_FILE)
        logging.info("Loaded %d TV exclusions", len(tv_exclusions))
        if EXCLUDED_DIRS_TV:
            logging.info("Excluded TV directories: %d", len(EXCLUDED_DIRS_TV))
            for excluded_dir in EXCLUDED_DIRS_TV:
                logging.info("  - %s", excluded_dir)

        (
            tv_non_hardlinked,
            tv_total_files,
            tv_excluded_files,
            tv_non_hardlinked_files,
        ) = scan_for_non_hardlinked_files(
            ROOT_DIR_TV, VIDEO_EXTENSIONS, tv_exclusions, EXCLUDED_DIRS_TV, group_index=-3, unknown_label="UNKNOWN_SHOW"
        )

        write_report(REPORT_FILE_TV, tv_non_hardlinked)

        logging.info("-" * 40)
        logging.info("TV SUMMARY")
        logging.info("-" * 40)
        logging.info("Total TV video files scanned: %d", tv_total_files)
        logging.info("Excluded TV files: %d", tv_excluded_files)
        logging.info("Non-hardlinked TV files: %d", tv_non_hardlinked_files)
        logging.info("Shows in TV report: %d", len(tv_non_hardlinked))
        logging.info("TV report path: %s", REPORT_FILE_TV)
        logging.info("") # Spacer before switching to movies

    # Movies scan
    if ENABLED_MOVIES:
        logging.info("-" * 40)
        logging.info("MOVIES SCAN")
        logging.info("-" * 40)
        if not ROOT_DIR_MOVIES:
            logging.warning("Movies enabled but 'root_dir_movies' is not set in config; skipping movies scan.")
        else:
            logging.info("Root media directory (Movies): %s", ROOT_DIR_MOVIES)
            logging.info("Exclusion file (Movies): %s", EXCLUSION_MOVIES_FILE)
            movies_exclusions = load_exclusions(EXCLUSION_MOVIES_FILE)
            logging.info("Loaded %d Movies exclusions", len(movies_exclusions))
            if EXCLUDED_DIRS_MOVIES:
                logging.info("Excluded Movies directories: %d", len(EXCLUDED_DIRS_MOVIES))
                for excluded_dir in EXCLUDED_DIRS_MOVIES:
                    logging.info("  - %s", excluded_dir)

            (
                movies_non_hardlinked,
                movies_total_files,
                movies_excluded_files,
                movies_non_hardlinked_files,
            ) = scan_for_non_hardlinked_files(
                ROOT_DIR_MOVIES, VIDEO_EXTENSIONS, movies_exclusions, EXCLUDED_DIRS_MOVIES, group_index=-2, unknown_label="UNKNOWN_MOVIE"
            )

            write_report(REPORT_FILE_MOVIES, movies_non_hardlinked)

            logging.info("-" * 40)
            logging.info("MOVIES SUMMARY")
            logging.info("-" * 40)
            logging.info("Total movie files scanned: %d", movies_total_files)
            logging.info("Excluded movie files: %d", movies_excluded_files)
            logging.info("Non-hardlinked movie files: %d", movies_non_hardlinked_files)
            logging.info("Movies in report: %d", len(movies_non_hardlinked))
            logging.info("Movies report path: %s", REPORT_FILE_MOVIES)

    logging.info("Script finished")


# ---------------------------
# Entry point
# ---------------------------

if __name__ == "__main__":
    main()