import lxml.html


class HTMLForm:

    def __init__(self, html_source, xpath_form):
        self.xpath_form = xpath_form
        self.html_source = html_source

    def get_form_values(self):
        input_values = self.read_input_values()
        select_values = self.read_select_values()
        values = input_values.copy()
        values.update(select_values)
        return values

    def read_input_values(self):
        return self.read_and_get_values("input")

    def read_select_values(self):
        return self.read_and_get_values("select")

    def read_and_get_values(self, element):
        document = lxml.html.fromstring(self.html_source)
        input_values = {}
        for input in document.xpath("//"+self.xpath_form+"/"+element):
            input_values[input.name] = input.value
        return input_values
