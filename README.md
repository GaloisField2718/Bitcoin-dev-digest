# Bitcoin-dev Digest python script saver

This script provides a way to save each mail which is distributed `To: bitcoin-dev@lists.linuxfoundation.org`. 
This info is used at  `18 status, msgnums = imap.search(None, 'TO "bitcoin-dev@lists.linuxfoundation.org"')`.

The script will create a folder for each Volume and save each mail indexed by `issue_xx` in MarkDown Format.

You can consult folders and file in this repo to see the behavior of this script. 

You can adapt easily for other saving purposes. 
Let me know if you need my help to do so <u>galoisfield2718@gmail.com</u>.

[Simple Mail Checker in Python](https://www.youtube.com/watch?v=4iMZUhkpWAc)

## Build

```
pipenv shell

> pipenv install --ignore-pipfile
```

If `--ignore-pipfile` flag doesn't work try `--dev-dependencies` flag.

## Setup

We need to setup the config in `.env` file. I used `email` and `KEY` names for constants.

## Run

In the python virtual environnement simply run `python3 script.py`.


