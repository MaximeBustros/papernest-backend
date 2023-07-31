# Prerequisites to run project
- Open project in vscode, have docker and remote container extensions installed
- Proceed to open project as a devcontainer
- If you need intellisense make sure to change interpreter to the one used by poetry
- Proceed to activate python environment in your shell by running
```
poetry shell
```

# To run extractor and convert values in datafile from csv to geojson with GPS coordinates
```
python src/extractor.py
```

# To run endpoint
```
python src/main.py
```