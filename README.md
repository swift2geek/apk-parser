# APK Metadata Extractor

This script extracts metadata and app icons from Android APK files. It utilizes the Android Asset Packaging Tool (aapt) to gather metadata and the Python Imaging Library (PIL) to process the app icons.

## Features

- Extracts metadata such as package name, version code, version name, SDK versions, and app name
- Extracts and saves the app icon as a PNG file
- Converts metadata keys to snake_case
- Saves metadata to a JSON file (optional)

## Requirements

- Python 3.6+
- [Android Asset Packaging Tool (aapt)](https://developer.android.com/studio/command-line/aapt2)
- [Pillow (Python Imaging Library)](https://pillow.readthedocs.io/en/stable/)

To install the Pillow library, run:

```bash
pip install Pillow
```

## Usage

1. Place the APK file you want to extract metadata from in a directory accessible by the script.
2. Run the script with the following command:

```bash
python apk_metadata_extractor.py /path/to/your/apk_file.apk
```

This will print the metadata to the console and save the app icon as `app_icon.png` in the same directory as the APK file.

To save the metadata as a JSON file, include the `-j` flag:

```bash
python apk_metadata_extractor.py /path/to/your/apk_file.apk -j
```

This will save the metadata to a JSON file with the same name as the APK file in the same directory.

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
