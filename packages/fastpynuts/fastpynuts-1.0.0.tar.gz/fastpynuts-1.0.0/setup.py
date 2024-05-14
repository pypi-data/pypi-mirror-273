import os, io, re
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

version = os.environ.get("FASTPYNUTS_VERSION", None)
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
        #re.sub(pattern, repl, string, count=0, flags=0)
        # long_description = re.sub(
            # r"![Figure: NUTS levels (Eurostat)](https://github.com/ColinMoldenhauer/FastPyNUTS/blob/main/levels.gif)",
            # r"![Figure: NUTS levels (Eurostat)](https://raw.githubusercontent.com/ColinMoldenhauer/FastPyNUTS/main/levels.png)",
            # r"![Figure: NUTS levels (Eurostat)](https://github.com/ColinMoldenhauer/FastPyNUTS/blob/main/levels.png?raw=true)",
            # r"![Figure: NUTS levels (Eurostat)](https://github.com/ColinMoldenhauer/FastPyNUTS/blob/main/levels.png)",
            # long_description
        # )
except FileNotFoundError:
    long_description = None

print()
print("here:", here)
print()


setup(
    version=version,
    long_description=long_description
)