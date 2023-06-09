import os
import shutil
from pathlib import Path

from invoke import run, task

from mtas import __version__ as __program_version__

os.environ["PIPENV_VERBOSITY"] = "-1"


def prun(command, **kwargs):
    """ Pipenv run """
    run(f"pipenv run {command}", **kwargs)


@task
def srv(context):
    prun("mtas_server.py")


@task
def clean(context):
    patterns = [l.strip() for l in open(
        '.gitignore', 'r', encoding='utf8').readlines()]
    patterns.remove('__pycache__/')
    patterns.remove('config.toml')

    patterns = [p for p in patterns if os.path.exists(p.strip())]
    found_smth = False

    for pattern in patterns:
        found_smth = True

        print("Removing %s" % pattern)
        try:
            shutil.rmtree(pattern)
        except:
            os.remove(pattern)

    if (log_files := list(Path(os.path.join(".", "log")).rglob("*.log*"))):
        found_smth = True
        print("Removing logs...")
        [os.remove(p) for p in log_files]

    if (pycache := list(Path('.').rglob('__pycache__'))):
        found_smth = True
        print("Removing python cache...")
        [shutil.rmtree(p) for p in pycache]

    if not found_smth:
        print("Nothing was found to delete, exitting...")


@task
def test(context):
    prun("pytest")


@task()
def tg(context):
    """Auto add tag to git commit depending on shprote.__version__"""
    run(f"git tag {__program_version__}")

