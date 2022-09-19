from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'asdasdaw212423fwefw23332eql23lpe90209-==1oek2030921'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(100), unique=True)
    role = db.Column(db.SmallInteger, default='ROLE_USER')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def __repr__(self):
        return '<User: %r>' % self.name


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title


@app.route('/home')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', items=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)
    from cloudipsp import Api, Checkout
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": str(item.price) + '00'
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/del/<int:id>')
def item_del(id):
    item = Item.query.get_or_404(id)

    try:
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('index'))

    except:
        return 'При удалении произошла ошибка'


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        text = request.form.get('text')
        item = Item(title=title, price=price, text=text)

        try:
            db.session.add(item)
            db.session.commit()
            flash('Item succesfully added')
            return redirect(url_for('index'))
        except:
            return flash('Thats an error in database')

    else:
        flash('Error of adding')

    return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)
