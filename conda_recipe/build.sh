#!/bin/bash

#build.sh must be adapted to the logic in /src
#this small template is suitable for single file scripts
mkdir -p $PREFIX/bin/
cp expandsets.py $PREFIX/bin/expandsets
chmod +x $PREFIX/bin/
