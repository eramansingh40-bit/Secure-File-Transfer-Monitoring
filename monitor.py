import os
import json
import hashlib
import logging
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

MONITORED_FOLDER = "monitored_folder"
HASH_FILE = "data/hashes.json"
LOG_FILE = "logs/security.log"

os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while chunk := file.read(4096):
                sha256.update(chunk)

        return sha256.hexdigest()

    except (FileNotFoundError, PermissionError):
        return None


def load_hashes():
    try:
        with open(HASH_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_hashes(hashes):
    with open(HASH_FILE, "w") as file:
        json.dump(hashes, file, indent=4)


class FileMonitor(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        file_path = event.src_path

        file_hash = calculate_hash(file_path)

        hashes = load_hashes()

        if file_hash:
            hashes[file_path] = file_hash
            save_hashes(hashes)

        logging.info(
            f"FILE CREATED | {file_path} | SHA256={file_hash}"
        )

        print(f"[+] FILE CREATED: {file_path}")

    def on_modified(self, event):

        if event.is_directory:
            return

        file_path = event.src_path

        new_hash = calculate_hash(file_path)

        hashes = load_hashes()
        old_hash = hashes.get(file_path)

        if old_hash and new_hash != old_hash:

            logging.warning(
                f"INTEGRITY VIOLATION | {file_path} | "
                f"OLD_HASH={old_hash} | NEW_HASH={new_hash}"
            )

            print(f"[!] INTEGRITY VIOLATION: {file_path}")

        elif new_hash:

            logging.info(
                f"FILE MODIFIED | {file_path} | SHA256={new_hash}"
            )

        if new_hash:
            hashes[file_path] = new_hash
            save_hashes(hashes)

    def on_deleted(self, event):

        if event.is_directory:
            return

        file_path = event.src_path

        hashes = load_hashes()
        hashes.pop(file_path, None)
        save_hashes(hashes)

        logging.warning(
            f"FILE DELETED | {file_path}"
        )

        print(f"[!] FILE DELETED: {file_path}")

    def on_moved(self, event):

        if event.is_directory:
            return

        logging.warning(
            f"FILE MOVED | FROM={event.src_path} | "
            f"TO={event.dest_path}"
        )

        print(
            f"[!] FILE MOVED: "
            f"{event.src_path} -> {event.dest_path}"
        )


if __name__ == "__main__":

    print("=" * 50)
    print(" Secure File Transfer Monitoring System")
    print("=" * 50)

    print(f"Monitoring folder: {MONITORED_FOLDER}")
    print("Press CTRL+C to stop.")
    print()

    event_handler = FileMonitor()

    observer = Observer()

    observer.schedule(
        event_handler,
        MONITORED_FOLDER,
        recursive=True
    )

    observer.start()

    try:

        while True:
            pass

    except KeyboardInterrupt:

        observer.stop()
        print("\n[+] Monitoring stopped.")

    observer.join()
