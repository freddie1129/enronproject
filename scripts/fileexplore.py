from pathlib import Path


def run():
    p = Path('/home/freddie/dirtest/')
    tree = {'data':[dir.name for dir in p.iterdir()]}
    pass

