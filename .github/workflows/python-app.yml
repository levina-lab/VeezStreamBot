name: FailCheck

on: [push, pull_request]

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      max-parallel: 5
      matrix:
        python-version: [3.9]

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        sudo apt-get install libpq-dev
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install flake8 flake8-print flake8-quotes
    - name: Check for showstoppers
      run: |
        flake8 . --count --select=E999 --show-source --statistics
  shellcheck:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Check for install script errors
      uses: ludeeus/action-shellcheck@0.1.0
