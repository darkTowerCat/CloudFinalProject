from flask import render_template
from flask.views import MethodView
import gbmodel

class Index(MethodView):
    def get(self):
        model = gbmodel.get_model()
        entries = [dict(title=row[0], author=row[1], signed_on=row[2], prep_time=row[3], ingredients=row[4]) for row in model.select()]
        return render_template('index.html',entries=entries)
