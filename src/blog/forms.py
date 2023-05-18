from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_ckeditor import CKEditorField


class ValidatorSwearInText:

    def __call__(self, form, field):
        ...
                

class PostAddForm(FlaskForm):
    title = StringField(label='Title', validators=[InputRequired(), Length(min=8, max=100)])
    text = TextAreaField(label='Content', validators=[InputRequired(), Length(min=255)])
    submit = SubmitField()

class PostChangeForm(FlaskForm):
    text = CKEditorField(label='Change text this post', validators=[Length(min=255)])
    save = SubmitField('Save') 
    cancel = SubmitField('Cancel')