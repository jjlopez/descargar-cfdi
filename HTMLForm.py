import lxml.html

class HTMLForm:
    def __init__(self, htmlSource, xpathForm):
        self.xpathForm = xpathForm
        self.htmlSource = htmlSource

