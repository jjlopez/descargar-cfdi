import lxml.html


class HTMLForm:

    def __init__(self, htmlSource, xpathForm):
        self.xpathForm = xpathForm
        self.htmlSource = htmlSource

    def get_form_values(self):
        inputValues = self.readInputValues()
        selectValues = self.readSelectValues()
        values = inputValues.copy()
        values.update(selectValues)
        return values

    def read_input_values(self):
        return self.readAndGetValues("input")

    def read_select_vValues(self):
        return self.readAndGetValues("select")

    def read_and_get_values(self, element):
        document = lxml.html.fromstring(self.htmlSource)
        inputValues = {}
        for input in document.xpath("//"+self.xpathForm+"/"+element):
            inputValues[input.name] = input.value
        return inputValues
