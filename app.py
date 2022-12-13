from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20), unique = False, nullable = False)
    product_category = db.Column(db.String(20), unique = False, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)

    def __init__(self, product_name, product_category, quantity):
        self.product_name = product_name
        self.product_category = product_category
        self.quantity = quantity



@app.route('/')
def check():
    return render_template('index.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/addnew')
def addnew():
    return render_template('addnew.html')

@app.route('/add', methods=['POST'])
def addProduct():
    
    product_name = request.form.get("productName")
    product_category = request.form.get("productCategory")
    product_quantity = request.form.get("quantity")

    if product_name != '' and product_category != '' and product_quantity != None:

        new_product = Inventory(product_name=product_name,product_category=product_category,product_quantity=product_quantity)
        db.session.add(new_product)
        db.session.commit()
        return redirect('/addnew')
    else:
        return redirect('/addnew')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()