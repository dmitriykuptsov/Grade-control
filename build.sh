#!/bin/bash
pyinstaller --onefile -w run.py
mkdir -p dist/data
cp -rv data/* dist/data

