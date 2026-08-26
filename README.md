#  Secure File Transfer Monitoring System

A simple Python-based cybersecurity project that monitors file activity, detects file movement and unauthorized modifications, verifies file integrity using **SHA-256 hashing**, and maintains security audit logs.

---

##  Project Overview

File movement and modification can create security risks such as:

* Unauthorized data movement
* Data leakage
* File tampering
* Accidental or malicious deletion
* Unauthorized modification of sensitive files

The **Secure File Transfer Monitoring System** monitors a selected directory and detects important filesystem activities.

The system currently monitors:

* File creation
* File modification
* File deletion
* File movement
* SHA-256 file integrity
* Security logging
* Integrity violation alerts

---

##  Project Objectives

The main objectives of this project are:

1. Monitor file activity in a specific directory.
2. Record file creation, modification, deletion, and movement.
3. Calculate SHA-256 hashes for monitored files.
4. Compare previous and current hashes.
5. Detect possible file tampering.
6. Generate security alerts for suspicious activity.
7. Maintain an audit log for investigation.

---

##  Project Architecture

```text
                 Secure File Transfer Monitoring System
                              |
                              v
                    ┌──────────────────┐
                    │ Monitored Folder │
                    └────────┬─────────┘
                             |
                             v
                    ┌──────────────────┐
                    │ Watchdog Monitor │
                    └────────┬─────────┘
                             |
             ┌───────────────┼───────────────┐
             |               |               |
             v               v               v
        File Events      SHA-256          Logging
             |           Integrity           |
             |            Check               |
             └───────────────┬───────────────┘
                             |
                             v
                    ┌──────────────────┐
                    │ Security Alerts  │
                    └──────────────────┘
```

### How it works

```text
File Activity
      ↓
Watchdog detects event
      ↓
Create / Modify / Delete / Move
      ↓
Calculate SHA-256 when required
      ↓
Compare old and new hash
      ↓
Generate alert if integrity is violated
      ↓
Save event in security.log
```

---

##  Project Structure

```text
Secure-File-Transfer-Monitor/
│
├── data/
│   └── hashes.json
│
├── logs/
│   └── security.log
│
├── monitored_folder/
│   ├── important.txt
│   └── backup/
│
├── screenshots/
│
├── monitor.py
├── requirements.txt
└── venv/
```

### Important files

| File/Directory      | Purpose                      |
| ------------------- | ---------------------------- |
| `monitor.py`        | Main monitoring program      |
| `monitored_folder/` | Directory being monitored    |
| `data/hashes.json`  | Stores SHA-256 hashes        |
| `logs/security.log` | Stores security events       |
| `screenshots/`      | Project evidence/screenshots |
| `requirements.txt`  | Python dependency            |
| `venv/`             | Python virtual environment   |

---

##  Technologies Used

* **Python 3.13**
* **Watchdog 6.0.0**
* **SHA-256**
* **JSON**
* **Python Logging**
* **Kali Linux**

### Python Libraries

```text
os
json
hashlib
logging
watchdog
```

---

##  Installation

### 1. Clone or create the project

```bash
mkdir Secure-File-Transfer-Monitor
cd Secure-File-Transfer-Monitor
```

### 2. Create project directories

```bash
mkdir monitored_folder
mkdir logs
mkdir data
mkdir screenshots
```

### 3. Create a Python virtual environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### 4. Install Watchdog

```bash
pip install watchdog
```

Verify the installation:

```bash
pip freeze
```

Expected:

```text
watchdog==6.0.0
```

---

##  requirements.txt

The project uses:

```text
watchdog
```

Install the dependency using:

```bash
pip install -r requirements.txt
```

---

##  Running the Project

Make sure you are inside the project directory:

```bash
cd ~/Secure-File-Transfer-Monitor
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Start the monitoring system:

```bash
python3 monitor.py
```

Expected output:

```text
==================================================
 Secure File Transfer Monitoring System
==================================================
Monitoring folder: monitored_folder
Press CTRL+C to stop.
```

The program will now continuously monitor the folder.

---

#  Testing the System

For testing, use **two terminals**.

This is important because Terminal 1 runs the monitoring program while Terminal 2 performs file operations.

---

## Terminal 1 — Start Monitoring

```bash
cd ~/Secure-File-Transfer-Monitor
source venv/bin/activate
python3 monitor.py
```

Leave this terminal running.

---

## Terminal 2 — File Creation Test

Open another terminal:

```bash
cd ~/Secure-File-Transfer-Monitor
```

Create a file:

```bash
echo "Confidential Information" > monitored_folder/important.txt
```

Terminal 1 should show:

```text
[+] FILE CREATED: monitored_folder/important.txt
```

The system also calculates and stores the file's SHA-256 hash.

---

##  Check Stored Hash

Run:

```bash
cat data/hashes.json
```

The file will contain information similar to:

```json
{
    "monitored_folder/important.txt": "SHA256_HASH_VALUE"
}
```

The exact hash will depend on the file content.

---

#  Integrity Violation Test

Now modify the file.

In Terminal 2:

```bash
echo "Unauthorized modification" >> monitored_folder/important.txt
```

The monitoring system calculates a new hash and compares it with the previously stored hash.

Terminal 1 should display:

```text
[!] INTEGRITY VIOLATION: monitored_folder/important.txt
```

### Detection logic

```text
Original File
     ↓
SHA-256
     ↓
Old Hash
     ↓
File Modified
     ↓
SHA-256 again
     ↓
New Hash
     ↓
Old Hash != New Hash
     ↓
 INTEGRITY VIOLATION
```

This is the main security detection feature of the project.

---

#  Security Log

View the security log:

```bash
cat logs/security.log
```

Example:

```text
INFO | FILE CREATED | monitored_folder/important.txt | SHA256=...
WARNING | INTEGRITY VIOLATION | monitored_folder/important.txt | OLD_HASH=... | NEW_HASH=...
```

The log provides an audit trail of file activity.

---

#  File Movement Test

Create another file:

```bash
echo "Test data" > monitored_folder/test.txt
```

Create a destination directory:

```bash
mkdir monitored_folder/backup
```

Move the file:

```bash
mv monitored_folder/test.txt monitored_folder/backup/
```

The monitoring terminal should show a file movement event similar to:

```text
[!] FILE MOVED:
monitored_folder/test.txt ->
monitored_folder/backup/test.txt
```

The event records:

* Original location
* Destination location
* File movement time

---

#  File Deletion Test

Delete the test file:

```bash
rm monitored_folder/backup/test.txt
```

The monitoring terminal should display:

```text
[!] FILE DELETED: monitored_folder/backup/test.txt
```

The deletion is also recorded in:

```text
logs/security.log
```

---

#  SHA-256 Integrity Verification

SHA-256 is used as a digital fingerprint for the monitored file.

For example:

```text
File:
important.txt

Original SHA-256:
ABC123...

File modified

New SHA-256:
XYZ789...
```

Because:

```text
ABC123... != XYZ789...
```

the system identifies a possible integrity violation.

> Note: A hash change proves that the file content changed; by itself, it does not prove who changed the file or whether the change was malicious.

---

#  Project Demonstration

A simple demonstration can follow this sequence:

```text
1. Start monitor.py
        ↓
2. Create important.txt
        ↓
3. SHA-256 hash is stored
        ↓
4. Modify important.txt
        ↓
5. New hash is calculated
        ↓
6. Old hash != New hash
        ↓
7. Integrity Violation alert
        ↓
8. View security.log
        ↓
9. Move a file
        ↓
10. Delete a file
```

This demonstrates the complete monitoring workflow.

---

#  Security Use Cases

This type of monitoring can be useful for detecting:

* Unauthorized file modification
* Suspicious file movement
* Possible data leakage
* File tampering
* Accidental deletion
* Suspicious activity involving sensitive files

---

#  Current Project Scope

This is a **filesystem-based monitoring project**.

The current version monitors activities inside the configured directory using Watchdog.

It does **not automatically monitor every possible:

* USB transfer
* Network upload/download
* Cloud upload
* Browser file transfer
* User identity
* Process responsible for the transfer

These can be added as future enhancements.

---

#  Future Improvements

Possible improvements include:

### 1. User Identification

Record which operating-system user performed the action.

### 2. Process Tracking

Use `psutil` to identify the process responsible for file activity.

### 3. Sensitive File Detection

Create rules for files such as:

```text
*.pdf
*.docx
*.xlsx
*.key
*.pem
*.env
```

### 4. USB Monitoring

Detect when removable storage devices are connected.

### 5. Network Share Monitoring

Monitor files transferred to network-mounted directories.

### 6. SIEM Integration

Send security events to:

* Wazuh
* Splunk
* Elasticsearch

### 7. Web Dashboard

Create a dashboard showing:

```text
Total Events
File Creations
File Modifications
File Deletions
File Movements
Integrity Violations
```

---

#  Learning Outcomes

This project demonstrates practical knowledge of:

* Python programming
* Filesystem monitoring
* Watchdog
* SHA-256 hashing
* File integrity monitoring
* JSON data storage
* Security logging
* Event detection
* Basic cybersecurity monitoring
* Security auditing

---

# 📸 Suggested Screenshots

For GitHub/project documentation, capture:

1. Project directory structure
2. `pip install watchdog`
3. Running `monitor.py`
4. File creation detection
5. `hashes.json`
6. Integrity violation alert
7. File movement detection
8. File deletion detection
9. `security.log`
10. Final project structure

Store the screenshots in:

```text
screenshots/
```

---

#  Conclusion

The **Secure File Transfer Monitoring System** is a simple Python-based security monitoring project that demonstrates how filesystem activity can be monitored and investigated.

The system detects file creation, modification, deletion, and movement. It also uses SHA-256 hashing to identify changes in file contents and generates an **Integrity Violation** alert when the stored and current hashes do not match.

The project provides a practical introduction to **File Integrity Monitoring (FIM), security logging, event detection, and cybersecurity monitoring**.

---

##  Author

**Amandeep**

Cybersecurity / SOC Analyst Project

---

##  Disclaimer

This project is developed for **educational and authorized security-monitoring purposes**. Only monitor files and systems that you own or have permission to monitor.
