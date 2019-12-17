from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods=['GET', 'POST'])
def index():
    posts = Blog.query.all()

    if request.args.get('id'):
        post_id = request.args.get('id')
        single_post = Blog.query.get(post_id)
        return render_template('view_post.html', post=single_post)
    return render_template('todos.html', posts=posts, page_title="Build A Blog")   


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        strikes = 0 
        missing_title = ""
        missing_body = ""

        if len(title) == 0:
            strikes += 1
            missing_title = ("Missing Title")
            
        if len(body) == 0:
            strikes += 1
            missing_body = ('Missing Body')
        
        if strikes == 0: 
            new_post = Blog(title,body)
            db.session.add(new_post)
            db.session.commit()

            return redirect('/blog?id=' + {{post.id}}) 
        else:            
            return render_template('add_post.html', title=title, body=body, missing_body=missing_body, missing_title=missing_title )
           
    return render_template('add_post.html')

if __name__ == '__main__':
    app.run()