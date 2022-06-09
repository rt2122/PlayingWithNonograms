"""Module for translation function."""
import gettext
import locale
import os

lang = locale.getdefaultlocale()[0][:2]
if lang != "ru":
    lang = "en"

if not os.environ.get('READTHEDOCS'):
    tr = gettext.translation("PWN", os.path.join(os.path.dirname(__file__), "./po"), [lang])
    _ = tr.gettext
else:
    def _(x):
        return x
