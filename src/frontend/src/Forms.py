from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class NewProject(FlaskForm):
    name = StringField("Project Name:")
    desc = StringField("Description:")
    owner = StringField("Owner:")
    members = StringField("Members:")
    analysis_hours = StringField("Analysis Hours:")
    design_hours = StringField("Design Hours:")
    coding_hours = StringField("Coding Hours:")
    testing_hours = StringField("Testing Hours:")
    mgt_hours = StringField("Management Hours:")
    func_requirement = StringField("Functional Requirement:")
    func_requirement_owner = StringField("Functional Requirement Owner:")
    nonfunc_requirement = StringField("Non Functional Requirement:")
    nonfunc_requirement_owner = StringField("Non Functional Requirement Owner:")
    risk = StringField("Risk:")
    risk_status = StringField("Risk Status:")
    submit = SubmitField("Press to Submit Project")