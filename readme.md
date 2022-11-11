## `JSON Boards CLI`

A CLI application to combine all board lists inside the JSON files into a single JSON output.

**Installation**:

* `Create Virtual Environment [optional]`
 
venv will usually install the most recent version of Python that you have available. 
```console
python -m venv <DIR>
```
Once you’ve created a virtual environment, you may activate it.

On Windows, run:
```console
<DIR>\Scripts\activate.bat
```
On Unix or MacOS, run:
```console
source <DIR>/bin/activate
```

* `Create Virtual Environment [optional]`
```console
python -m pip install -r requirements.txt
```


**Usage**:

```console
$ python app.py [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `merge`: JSON files from a given directory using the --file-path option are combined into a single output.
    If no directory is provided, the default directory 'boards' is used.

## `Merge Command`

JSON files from a given directory using the --file-path option are combined into a single output.
    If no directory is provided, the default directory 'boards' is used.

    An example JSON file for this program may look like this:
    {
        "boards": [
            {
            "name": "D4-200S",
            "vendor": "Boards R Us",
            "core": "Cortex-M4",
            "has_wifi": false
            }
        ]
    }

    A JSON file without the 'boards' object will be ignored.

**Usage**:

```console
$ python app.py merge [OPTIONS]
```

**Options**:

* `--file-path`: Specify a valid directory of JSON files to be combined.
* `--help`: Show this message and exit.
