from flask import render_template
from flask.views import MethodView
import gbmodel

class Index(MethodView):
    def get(self):
        model = gbmodel.get_model()
        entries = [dict(title=t, author=a, date=d, prep_time=p, ingredients=i) for t, a, d, p, i in model.select()]
        return render_template('index.html',entries=entries)
