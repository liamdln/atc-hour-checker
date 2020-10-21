# VATSIM ATCHourCount

A Python script designed to search for a VATSIM user's ATC hours between two specific dates.

## Running

To run the script, either download the program from Github, or if you want to work on it, fork and clone it to your computer. PRs welcome!

Once the files have been downloaded, open terminal and ensure you have Python installed by running:

```sh
python --version
```

This should return a Python version, if not, please install Python first. I recommend you use Python version 3.7.

Now navigate to the `src` folder, and run:

```sh
python Main.py
```

This will start the script.

## Configuration

Before searching for a user's hours, you must first setup the minimum hours required, the dates to search between, and the positions you would like to search. This can be done from the menu of the program.

Once these values have been entered, you can choose option `a) Search user.` and input the user's VATSIM CID, the program will return the hours they have put in on any of the position you entered before searching.
