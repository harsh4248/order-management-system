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
    product_price = db.Column(db.Float, unique = False, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)

    def __init__(self, product_name, product_category, product_price, quantity):
        self.product_name = product_name
        self.product_category = product_category
        self.product_price = product_price
        self.quantity = quantity



@app.route('/')
def check():
    return render_template('index.html')

@app.route('/user')
def user():
    inventory = Inventory.query.all()
    return render_template('user.html', inventory = inventory)

@app.route('/admin')
def admin():
    inventory = Inventory.query.all()
    return render_template('admin.html',inventory = inventory)

@app.route('/admin/addnew')
def addnew():
    return render_template('addnew.html')

@app.route('/delete/<int:id>')
def erase(id):
    # Deletes the data on the basis of unique id and
    # redirects to home page
    data = Inventory.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/admin')

@app.route('/sell/<int:id>')
def sell(id):
    data = Inventory.query.get(id)
    if(data.quantity > 0):
        data.quantity = data.quantity - 1
    db.session.commit()
    return redirect('/user')

@app.route('/update/<int:id>')
def update(id):
    data = Inventory.query.get(id)
    return render_template('/update.html', inventory = data)

@app.route('/update',methods=['POST'])
def updateData():
    product_id = request.form.get('productID')
    print(product_id)
    product_name = request.form.get("productName")
    product_category = request.form.get("productCategory")
    product_quantity = request.form.get("quantity")
    product_price = request.form.get("productPrice")

    data = Inventory.query.get(product_id)
    data.product_name = product_name
    data.product_category = product_category
    data.product_price = product_price
    data.quantity = product_quantity

    db.session.commit()
    print('done')
    return redirect('admin')
    

@app.route('/add', methods=['POST'])
def addProduct():
    
    product_name = request.form.get("productName")
    product_category = request.form.get("productCategory")
    product_quantity = request.form.get("quantity")
    product_price = request.form.get("productPrice")

    if product_name != '' and product_category != '' and product_quantity != None and product_price != None:
    
        new_product = Inventory(product_name=product_name,product_category=product_category,product_price=product_price,quantity=int(product_quantity))
        db.session.add(new_product)
        db.session.commit()
        print('done')
        return redirect('admin')
    else:
        return redirect('admin/addnew')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()