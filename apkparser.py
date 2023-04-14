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

# Get the APK file path from the command-line argument
apk_file = sys.argv[1]

# Open the APK file as a Zip archive
apk_zip = zipfile.ZipFile(apk_file)

# Find the icon file in the res/ directory
icon_file = None
for f in apk_zip.namelist():
    if 'res/' in f and '/mipmap' in f and 'ic_launcher.png' in f:
        icon_file = f
        break

# Extract the metadata from the APK using aapt
aapt_cmd = ['aapt', 'dump', 'badging', apk_file]
aapt_output = subprocess.check_output(aapt_cmd, universal_newlines=True)
metadata = {}
for line in aapt_output.splitlines():
    if line.startswith('package:'):
        package_info = line.split(' ')
        metadata['Package Name'] = package_info[1].split('=')[1]
        metadata['Version Code'] = package_info[2].split('=')[1]
        metadata['Version Name'] = package_info[3].split('=')[1]
        if len(package_info) > 4:
            metadata['Target SDK Version'] = package_info[4].split('=')[1]
        if len(package_info) > 5:
            metadata['Min SDK Version'] = package_info[5].split('=')[1]
        if len(package_info) > 6:
            metadata['Max SDK Version'] = package_info[6].split('=')[1]
    elif line.startswith('application:'):
        app_info = line.split(' ')
        metadata['App Name'] = app_info[1].split('=')[1]
        if 'icon=' in app_info:
            metadata['Icon Path'] = app_info[app_info.index('icon=') + 1].strip("'")
        elif 'ic_launcher_foreground.png' in app_info:
            metadata['Icon Path'] = os.path.join('res', 'mipmap-xxxhdpi-v4')

# Extract the app icon from the APK using aapt and save it as a PNG file
if icon_file:
    with apk_zip.open(icon_file) as icon_data:
        icon_image = Image.open(icon_data)
        icon_path = os.path.join(os.path.dirname(apk_file), 'app_icon.png')
        icon_image.save(icon_path)
        metadata['Icon Path'] = icon_path
else:
    if 'Icon Path' in metadata:
        icon_data = subprocess.check_output(['aapt', 'get', apk_file, metadata['Icon Path']])
        icon_image = Image.open(BytesIO(icon_data))
        icon_path = os.path.join(os.path.dirname(apk_file), 'app_icon.png')
        icon_image.save(icon_path)
        metadata['Icon Path'] = icon_path
    else:
        print("App icon not found in APK")

# Print out the metadata
for key, value in metadata.items():
    print(f"{key}: {value}")
