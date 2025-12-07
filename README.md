# 🚀 BeamMP-Updater

A lightweight, automated updater for the **BeamMP Launcher**. This tool monitors your installed BeamMP Launcher and keeps it synchronized with the latest GitHub releases.

---

## ✨ Features

- **Automatic Version Detection** - Reads your installed BeamMP Launcher version from its executable
- **Latest Release Tracking** - Fetches the newest version directly from GitHub
- **One-Click Updates** - Automatically downloads and installs the latest release
- **Start Menu Integration** - Creates a convenient shortcut in your Windows Start Menu
- **Smart Dependency Checking** - Ensures the launcher is installed before attempting updates

---

## 📋 Requirements

- **Python 3.6+**
- **Windows OS** (uses Windows-specific APIs)
- **BeamMP Launcher** installed in `%APPDATA%\BeamMP-Launcher\`

### Python Dependencies

```
pefile
pypiwin32
requests
```

---

## 🎯 Usage

### As a Python Script

```bash
python BeamMP-Updater.py
```

The updater will:
1. Check if BeamMP Launcher is installed
2. Offer to install itself to the BeamMP Launcher directory
3. Create a Start Menu shortcut (if run as an executable)
4. Compare your current version with the latest release
5. Download and install updates if available

### As an Executable

Simply run `BeamMP-Updater.exe` - no Python installation required!

---

## 🔨 Building

### Prerequisites

Install PyInstaller and dependencies:

```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Build Command

```bash
pyinstaller BeamMP-Updater.spec
```

Or build without a spec file:

```bash
pyinstaller --onefile --windowed BeamMP-Updater.py
```

### Output

The compiled executable will be located in the `dist/` folder:

```
dist/
└── BeamMP-Updater.exe
```

---

## 📁 Project Structure

```
BeamMP-Updater/
├── BeamMP-Updater.py          # Main script
├── BeamMP-Updater.spec        # PyInstaller build configuration
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── LICENSE                    # Project license
```

---

## 🔧 How It Works

1. **Version Detection** - Uses the `pefile` library to extract file version info from the launcher executable
2. **GitHub Integration** - Queries the BeamMP Launcher GitHub API for the latest release
3. **Smart Download** - Streams the download in chunks for efficient memory usage
4. **Windows Integration** - Creates a `.lnk` shortcut for easy access from the Start Menu

---

## 📝 License

See the `LICENSE` file for details.

---

## 🐛 Troubleshooting

**"BeamMP Launcher is not installed"**
- Ensure BeamMP Launcher is installed in `%APPDATA%\BeamMP-Launcher\`

**Network errors during download**
- Check your internet connection
- Verify GitHub API is accessible

**Shortcut creation fails**
- The script requires administrator privileges to create Start Menu shortcuts
- Run as administrator if needed
