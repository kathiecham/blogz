from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:12345@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))


    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['GET'])
def index():

    if request.args.get("id"):
        blog_id = request.args.get("id")
        blog = Blog.query.get(blog_id)

        return render_template('single_post.html', blog=blog)

    else:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)

@app.route('/add_post', methods=['GET', 'POST'])
def add_blog():
    if request.method == 'GET':
        return render_template('add_post.html')

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        title_error = ""
        body_error = ""

        if not title:
            title_error = "Please fill in the title"

        if len(body) < 1:
            body_error = "Please fill in the body"

        if not title_error and not body_error:
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()
            query_param_url = "/blog?id=" + str(new_blog.id)
            return redirect(query_param_url)

        else:
            return render_template('add_post.html', title_error=title_error, body_error=body_error)

if __name__ == '__main__':
    app.run()