#!/bin/bash

echo "Test setup."
cd ..

echo "Virtual env"
if [ -d "venv" ]; then
  echo "Found virtualenv folder or symlink"
else
  echo "Could not find virtualenv folder or symlink. Create it and install the packages in requirements.txt inside it."; exit 1
fi;

# Todo - how to exit on failure?
source venv/bin/activate || echo "failed to activate" ; echo FAIL
echo "activated"
echo

cd app
echo "working in:"
pwd
echo
