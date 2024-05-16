"""
github
shaiksamad/lockscreen-magic
latest
"""

# FILES = [
#     "config.json",
#     "igcmdWin10.exe",
#     "LICENCE",
#     "README.md",
#     "locscreen_magic.pyw"
# ]
DRIVE = 'D'

# SOURCE = "src/invoice_parser"
SOURCE = "."

FILES = [
    # "errors.py",
    # 'gst.py',
    # "notafile.py"
]


# TODO: Improve IGNORE. Add wildcards. *

IGNORE = [
    '.gitignore',
    '.version',
    "LICENSE",
    "README.md",
    "pyproject.toml",
]

# INSTALL_FOLDER = "Lockscreen Magic"

from project_installer import Installer

# print(globals())
i = Installer(__doc__, globals())
print(i.__dict__)
i.install()
