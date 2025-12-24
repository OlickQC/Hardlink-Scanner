#!/usr/bin/env python3
"""
Scan TV show directories and identify non-hardlinked video files.

"""

import json
import logging
import os
from collections import defaultdict
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------
# Configuration
# ---------------------------

# Base directory (script location)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# Load configuration from JSON file
if not os.path.exists(CONFIG_FILE):
    raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

# Configuration values
VERBOSE = CONFIG.get("verbose", True)
ROOT_DIR = CONFIG["root_dir"]
EXCLUSION_FILE = os.path.join(CONFIG_DIR, CONFIG["exclusion_file"])
VIDEO_EXTENSIONS = tuple(
    ext.lower() for ext in CONFIG["video_extensions"]
)
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Create reports directory if it doesn't exist
os.makedirs(REPORTS_DIR, exist_ok=True)

# Generate timestamped report filename
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M")
REPORT_FILE = os.path.join(
    REPORTS_DIR,
    f"non_hardlinked_tv_episodes_{TIMESTAMP}.txt"
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


def scan_for_non_hardlinked_files(root_dir, video_exts, exclusions):
    """
    Scan directory for non-hardlinked video files.

    Args:
        root_dir (str): Root directory to scan.
        video_exts (tuple): Tuple of video file extensions to look for.
        exclusions (set): Set of excluded paths.

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
                    show_title = (
                        path_parts[-3]
                        if len(path_parts) >= 3
                        else "UNKNOWN_SHOW"
                    )

                    non_hardlinked[show_title].append(relative_path)
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
    logging.info("Script started")
    logging.info("Root media directory: %s", ROOT_DIR)
    logging.info("Exclusion file: %s", EXCLUSION_FILE)
    logging.info("Reports directory: %s", REPORTS_DIR)
    logging.info("Report file: %s", REPORT_FILE)

    # Load exclusion list
    exclusions = load_exclusions(EXCLUSION_FILE)
    logging.info("Loaded %d exclusions", len(exclusions))

    # Scan for non-hardlinked files
    (
        non_hardlinked,
        total_files,
        excluded_files,
        non_hardlinked_files,
    ) = scan_for_non_hardlinked_files(
        ROOT_DIR, VIDEO_EXTENSIONS, exclusions
    )

    # Write report
    write_report(REPORT_FILE, non_hardlinked)

    # Log summary
    logging.info("-" * 40)
    logging.info("SUMMARY")
    logging.info("-" * 40)
    logging.info("Total video files scanned: %d", total_files)
    logging.info("Excluded files: %d", excluded_files)
    logging.info("Non-hardlinked files: %d", non_hardlinked_files)
    logging.info("Shows in report: %d", len(non_hardlinked))
    logging.info("Report path: %s", REPORT_FILE)
    logging.info("Script finished")


# ---------------------------
# Entry point
# ---------------------------

if __name__ == "__main__":
    main()