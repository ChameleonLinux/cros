class Config:
    options = {'environment': 'development',
               'title': '',
               'description': '',
               'disallow_sysfiles': 'true',
               'allowed_sysfiles': '_css',
               'basepath': '/',
               'baseurl': 'http://localhost',
               'footer_text': '<a href="https://github.com/ProjectCros/cros">Proudly powered by cros.</a>',
               'footer_year': '<<!---->? echo date("Y");?>'
    }

    def __init__(self, path):
        c = open(path + "/_config.t", "r").read()
        c = c.strip()
        c = c.replace("\n", "")
        c = c.split(";")
        for ln in c:
            if ln in ('\n', '', '\r', '\r\n'): continue
            arr = ln.split(" ", 1)
            obj = arr[0]
            value = arr[1]
            if value == 'true': value = True
            if value == 'false': value = False
            self.options[obj] = value
