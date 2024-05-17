## Content
This repo contains a collection of tools for working with DSI Quantitys (Vectors [even with only on value]) and list of DSI Quantitys (Tables).
As well as the tools needed to generate visualisations of the data. Using Bokeh
# Visualisation
![Image of DSI Multivectorplot showing Gui Elements to change language, lin/log axis and selected Index](/doc/mvPloter.png)

## Installation
for usage in your project, you can install the package via pip:
```bash
pip install dccQuantities
```

For development, you can clone the repository and install the package in editable mode:
```bash
git clone https://gitlab1.ptb.de/digitaldynamicmeasurement/dccQuantities.git
cd dccQuantities
pip install -e .[testing]
```

## Usage
See the examples in the `doc` folder for usage of the package.
1. [Vector and Table Usage](doc/pyDCCToolsExamplesNoteBook.ipynb)
2. [MultiVector Plot](tests/bokePlotTest.py)


