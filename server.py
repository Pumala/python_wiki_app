from flask import Flask, redirect, render_template, request
from wiki_linkify import wiki_linkify
import re
import pg

app = Flask('MyApp')

db = pg.DB(dbname='wiki_db')

@app.route('/')
def render_homepage():
    return render_template(
        'homepage.html',
        title='Homepage'
    )

@app.route('/<page_name>')
def render_placeholder(page_name):
    query = db.query("select * from wiki where pagename = '%s'" % page_name)
    print "Query: %r" % query
    is_available = False
    print "Length: %d" % len(query.namedresult())
    if len(query.namedresult()) < 1:
        is_available = True
        db.insert(
            'wiki', {
                'pagename': page_name,
                'content': ""
            }
        )
        wiki_page = None
    else:
        wiki_page = query.namedresult()[0]
    # if page_name in db.('wiki',)
    # db.insert('wiki', pagename=page_name,content="")
    return render_template(
        'placeholder.html',
        page_name = page_name,
        is_available = is_available,
        wiki_page = wiki_page
    )

@app.route('/<page_name>/edit')
def render_pageEdit(page_name):
    query = db.query("select * from wiki where pagename = '%s'" % page_name)
    wiki_page = query.namedresult()[0]
    return render_template(
        'page_edit.html',
        page_name = page_name,
        wiki_page = wiki_page
    )

@app.route('/<page_name>/save', methods=['POST'])
def saveEdit(page_name):
    wiki_id = request.form.get('id')
    print "ID: %r" % wiki_id
    print "PAGE NAME: %r" % page_name
    content=request.form.get('content')
    db.update(
        'wiki', {
            'id': wiki_id,
            'pagename': page_name,
            'content': content
        }
    )

    return redirect('/%s' % page_name)

@app.route('/allpages')
def allPages():
    query = db.query('select * from wiki')
    return render_template(
        'allpages.html',
        results = query.namedresult()
    )

if __name__ == '__main__':
    app.run(debug=True)
