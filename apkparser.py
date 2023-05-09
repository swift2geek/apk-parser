# Author:  Vladimir Valter
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.


import os
import subprocess
import sys
from io import BytesIO
from PIL import Image
import zipfile
import json


def extract_app_icon(apk_zip, icon_file, apk_file):
    with apk_zip.open(icon_file) as icon_data:
        icon_image = Image.open(icon_data)
        icon_path = os.path.join(os.path.dirname(apk_file), 'app_icon.png')
        icon_image.save(icon_path)
    return icon_path


def extract_metadata(aapt_output):
    metadata = {}
    for line in aapt_output.splitlines():
        if line.startswith('package:'):
            package_info = line.split(' ')
            metadata['package_name'] = package_info[1].split('=')[1].strip("'")
            metadata['version_code'] = package_info[2].split('=')[1].strip("'")
            metadata['version_name'] = package_info[3].split('=')[1].strip("'")
            if len(package_info) > 4:
                metadata['target_sdk_version'] = package_info[4].split('=')[1].strip("'")
            if len(package_info) > 5:
                metadata['min_sdk_version'] = package_info[5].split('=')[1].strip("'")
            if len(package_info) > 6:
                metadata['max_sdk_version'] = package_info[6].split('=')[1].strip("'")
        elif line.startswith('application:'):
            app_info = line.split(' ')
            metadata['app_name'] = app_info[1].split('=')[1].strip("'")
            if 'icon=' in app_info:
                metadata['icon_path'] = app_info[app_info.index('icon=') + 1].strip("'")
            elif 'ic_launcher_foreground.png' in app_info:
                metadata['icon_path'] = os.path.join('res', 'mipmap-xxxhdpi-v4')
    return metadata


def convert_to_snake_case(data):
    return {k.lower().replace(' ', '_'): v for k, v in data.items()}


def main():
    apk_file = sys.argv[1]
    apk_zip = zipfile.ZipFile(apk_file)

    icon_folders = [
        "/mipmap-xxxhdpi-v4/",
        "/mipmap-xxhdpi/",
        "/mipmap-xhdpi/",
        "/mipmap-hdpi/",
        "/mipmap-mdpi/",
        "/mipmap-ldpi/"
    ]
    icon_names = [
        "ic_launcher_foreground.png",
        "ic_launcher.png"
    ]

    icon_file = None
    for folder in icon_folders:
        for name in icon_names:
            icon_file = next(
                (f for f in apk_zip.namelist() if 'res/' in f and folder in f and name in f),
                None
            )
            if icon_file:
                break
        if icon_file:
            break

    aapt_cmd = ['aapt', 'dump', 'badging', apk_file]
    aapt_output = subprocess.check_output(aapt_cmd, universal_newlines=True)

    metadata = extract_metadata(aapt_output)

    if icon_file:
        metadata['icon_path'] = extract_app_icon(apk_zip, icon_file, apk_file)
    else:
        print("App icon not found in APK")

    metadata = convert_to_snake_case(metadata)

    for key, value in metadata.items():
        print(f"{key}: {value}")

    if '-j' in sys.argv:
        apk_name = os.path.splitext(os.path.basename(apk_file))[0]
        json_file = os.path.join(os.path.dirname(apk_file), f"{apk_name}.json")

        with open(json_file, 'w') as f:
            json.dump(metadata, f, indent=4)

        print(f"Metadata saved to: {json_file}")


if __name__ == '__main__':
    main()


