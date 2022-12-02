# Extract complete accounting data from Scopevisio

Use the [Scopevisio API](https://appload.scopevisio.com/static/swagger/index.html)
to extract all accounting data and accounting documents.

## Setup
The python3 environment should be setup with the command

```
$ pip install -r requirements.txt
```

To use the API, credentials need to be provided in the file `scopevisio.ini`.
Use the file [scopevisio_example.ini](scopevisio_example.ini) as reference:
```
$ cp scopevisio_example.ini scopevisio.ini
```
Then edit the file `scopevisio.ini` accordingly.

## How to use
The Scopevisio extract is generated with the command:
```
$ python extract_accounting.py
```
The script will take a while to run.
After it is finished the accounting data is available in the folder `exports`.

Use the following command to get help on all script options:
```
$ python extract_accounting.py --help
usage: extract_accounting.py [-h] [-c CONFIGFILE] [-e EXPORTFOLDER] [-s]

Extract all accounting data of a company from Scopevisio

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIGFILE, --configfile CONFIGFILE
                        Path of the file containing the Scopevisio configuration [scopevisio.ini]
  -e EXPORTFOLDER, --exportfolder EXPORTFOLDER
                        Path of the folder that will contain the export [export]
  -s, --skipdocumentdownload
                        Skip downloading of document files [false]
```
