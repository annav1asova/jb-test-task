from flask import Flask, g, redirect, url_for, render_template, flash
from forms import SearchForm
from request_processor import prepare_table

app = Flask(__name__)

@app.before_request
def before_request():
    g.search_form = SearchForm()

@app.route('/')
def explore():
    return render_template('base.html')


@app.route('/search')
def search():
    if not g.search_form.validate():
        return redirect(url_for('explore'))

    if not g.search_form.is_correct():
        flash('You can use only english letters, digits and double quotes to specify your search request.')
        return render_template('base.html')


    result_table, num_articles = prepare_table(g.search_form.q.data)

    if result_table.empty:
        return render_template('empty_table.html')

    return render_template('table.html', table=result_table.to_html(classes=["table","table-bordered", "table-striped"]),
                           num_articles=num_articles)

if __name__ == "__main__":
    app.secret_key = 'very secret key'
    app.run(debug=True)

