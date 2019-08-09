from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel

class AddRecipe(MethodView):
    def get(self):
        return render_template('addRecipe.html')

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        model = gbmodel.get_model()
        model.insert(request.form['title'], request.form['author'], request.form['prep_time'], request.form['ingredients'])
        return redirect(url_for('index'))
