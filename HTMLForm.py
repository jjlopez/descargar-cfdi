import lxml.html

class HTMLForm:
    def __init__(self, htmlSource, xpathForm):
        self.xpathForm = xpathForm
        self.htmlSource = htmlSource

    def getFormValues(self):
        inputValues = self.readInputValues()
        selectValues = self.readSelectValues()
        values=inputValues.copy()
        values.update(selectValues)
        return values

    def readInputValues(self):
        return self.readAndGetValues("input")

    def readSelectValues(self):
        return self.readAndGetValues("select")

    def readAndGetValues(self, element):
        document=lxml.html.fromstring(self.htmlSource)
        inputValues = {}
        for input in document.xpath("//"+self.xpathForm+"/"+element):
            inputValues[input.name] = input.value
        return inputValues;
