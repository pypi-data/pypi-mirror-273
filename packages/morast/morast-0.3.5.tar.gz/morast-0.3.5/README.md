# Module reference by analyzing the syntax tree

_Create reference documentation from sources using AST_

```
pip install morast
```

Installation in a virtual environment is strongly recommended.


## Usage

Output of `python -m morast --help`:

```
usage: morast [-h] [--version] [-d | -v | -q]
              {auto,extract,init,config,module} ...

Create reference documentation from sources using AST

positional arguments:
  {auto,extract,init,config,module}
    auto                automatically detect and document all modules
    extract             extract override templates from modules
    init                initialize the Morast project
    config              show the configuration
    module              document a single module

options:
  -h, --help            show this help message and exit
  --version             print version and exit

Logging options:
  control log level (default is WARNING)

  -d, --debug           output all messages (log level DEBUG)
  -v, --verbose         be more verbose (log level INFO)
  -q, --quiet           be more quiet (log level ERROR)
```


## Further reading

Please see the documentation at <https://blackstream-x.gitlab.io/morast>
for detailed usage information.

If you found a bug or have a feature suggestion,
please open an issue [here](https://gitlab.com/blackstream-x/morast/-/issues)

