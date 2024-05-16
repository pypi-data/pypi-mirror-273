# Move Unmarker
Very small CLI utility to remove PII watermarks from pdfs downloaded from Move USP/ESALQ, using [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/).

## Installation
1. Make sure Python 3.8 or higher and pip are installed
1. Run `pip install move-unmarker`

## Usage
    usage: unmarker [-h] [-o OUTPUT] [-g GARBAGE] input

    Utility to remove PII watermarks from pdfs downloaded from Move USP/ESALQ.

    positional arguments:
    input                   input filename

    options:
    -h, --help              show this help message and exit
    -o OUTPUT, --output OUTPUT
                            output filename (default: unmarked.pdf)
    -g GARBAGE, --garbage GARBAGE
                            level of garbage collection (default: 1)  
[pymupdf.Document.save](https://pymupdf.readthedocs.io/en/latest/document.html#Document.save) method for more details on garbage collection.  

### TLDR
- `unmarker watermarker.pdf`  
- `unmarker -o unmarked.pdf watermarked.pdf`  
- `unmarker --garbage 3 watermarked.pdf`

## Development
1. Check Python's version `python -V`
1. Install Python 3.8 or higher and pip, if they aren't already installed:

    - Windows `winget install Python.Python.3.X` (replace X with the desired minor version)
    - Ubuntu/Debian based distros `apt install python3 python3-pip`
    - Arch based distros `pacman -S python python-pip`
    - Fedora `dnf install python3 python3-pip`

1. [Install poetry](https://python-poetry.org/docs/#installation) 
1. Clone this repo   
`git clone https://github.com/joaofauvel/move-unmarker.git && cd move-unmarker`
1. Install requirements   
`poetry install`