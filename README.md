# Novi
A dictionary for your terminal.

![](https://i.imgur.com/TFrD1nd.png)

# Features
- Clickable words (it will open the definition of the word on your browser).
- Scrapes Cambridge Dictionary.
- Word definition examples.

# Installation
### First Method
```bash
git clone --depth 1 --branch main <REPO URL> novi
pip install ./novi
```
### Second Method
```bash
pip install git+<REPO URL>@main
```

# Command-line Arguments
```
usage: novi [-h] [--debug] [-V] [words ...]

positional arguments:
  words          Words to search. You can specify multiple words by splitting
                 them by whitespace.

options:
  -h, --help     show this help message and exit
  --debug        Enable debug logs.
  -V, --version  Show program version.
```

# License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

* * *

Feel free to enhance Novi according to your needs and contribute back to the project! If you encounter any issues or have suggestions for improvement, please open an issue on the repository. Thank you for using Novi!
