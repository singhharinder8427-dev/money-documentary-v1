#!/usr/bin/env bash
# Downloads the free fonts used by the scripts into ./fonts (OFL / Apache licensed).
set -e; mkdir -p fonts; cd fonts
G=https://raw.githubusercontent.com/google/fonts/main
for f in ofl/alfaslabone/AlfaSlabOne-Regular.ttf apache/specialelite/SpecialElite-Regular.ttf ofl/barlowcondensed/BarlowCondensed-Bold.ttf \
         ofl/barlowcondensed/BarlowCondensed-SemiBold.ttf ofl/caveatbrush/CaveatBrush-Regular.ttf ofl/kalam/Kalam-Bold.ttf apache/permanentmarker/PermanentMarker-Regular.ttf; do
  curl -sSL -O "$G/$f"; done
curl -sSL -o dseg.zip https://github.com/keshikan/DSEG/releases/download/v0.46/fonts-DSEG_v046.zip && unzip -q -o dseg.zip -d dseg && find dseg -name DSEG7Classic-Bold.ttf -exec cp {} . \; && rm -rf dseg dseg.zip
echo "fonts ready"
