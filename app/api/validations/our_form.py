from wtforms import Form


class OurForm(Form):
    def generate_form_error_string(self):
        error = ""
        for k, v in self.errors.items():
            error += f"{k} : {','.join(v)} "
        return error
