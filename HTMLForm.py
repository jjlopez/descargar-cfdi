import lxml.html

class HTMLForm:
    def __init__(self, htmlSource, xpathForm):
        self.xpathForm = xpathForm
        self.htmlSource = htmlSource

    def readAndGetInputValues(self):
        document=lxml.html.fromstring(self.htmlSource)
        inputValues = {}
        for input in document.xpath("//"+self.xpathForm+"/input"):
            inputValues[input.name] = input.value
        return inputValues;
