[![Build Status](https://travis-ci.org/Ross-Alexandra/SudokuPlayer.svg?branch=master)](https://travis-ci.org/Ross-Alexandra/SudokuPlayer)

# SudokuPlayer
This project comes in two parts. One is a puzzle solver. This solver
will solve Sudoku puzzles using human methods (ie, it will not
use back tracking to brute force the puzzle.) The other part is
generating Sudoku puzzles.

# Usage
As of current, this project is being re-built. There is currently
no code written. Thus, there is no usage yet.

# Setup
This will guide you through setting up the environment to develop on
this project.

## Creating/Setting up a Virtual Environment
First create your virtual environment using
``` commandline
python -m venv {environment name}
```
After a short while, a new directory under the name {environment
name} will be created.

Next, you need to activate the vm. This is done differently
on different operating systems. Deactvating however can be done the
same on both systems.

### Linux / MacOS
``` commandline
source {environment name}/bin/activate
```

### Windows
``` commandline
{environment name}\Scripts\activate
```

### Deactivation
``` commandline
{environment name}\Scripts\deactivate
```

## Installing Requirements
In order to install the development requirements, run
``` commandline
python -m pip install -r requirements-dev.txt
```
