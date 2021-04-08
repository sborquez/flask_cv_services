# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
#from wtforms import PasswordField, StringField
from flask_wtf.file import FileField, FileAllowed, FileRequired



class ImageForm(FlaskForm):
    """Generic image form."""

    #image = StringField("Image", validators=[DataRequired()])
    image = FileField("Image", validators=[
        FileRequired(),
        FileAllowed(["jpg", "png"], "Images only!")
    ])

    def validate(self):
        """Validate the form."""
        initial_validation = super(ImageForm, self).validate()
        if not initial_validation:
            return False
        return True
