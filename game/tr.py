import gettext
import locale

lang = locale.getdefaultlocale()[0][:2]
if lang != "ru":
    lang = "en"

tr = gettext.translation("PWN", "./po", [lang])
_ = tr.gettext
