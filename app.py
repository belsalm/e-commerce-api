from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

# Modelagem
# Produto (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
@app.route('/products/add', methods=["POST"])
def add_products():
    data = request.json
    if 'name' in data and 'price' in data: 
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added successfully!"})
    return jsonify({"message": "Invalid product data"}), 400

@app.route('/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product != None:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully!"})
    return jsonify({"message": "Product not found"}), 404

    
# @app.route('/products/delete/<int:product_id>', methods=["DELETE"])
# def delete_product(product_id):
#     # Recuperar o produto da base de dados
#     # Verificar se o produto existe
#     # Se existe, apagar da base de dados
#     # Se não existe, retornar 404 not found
#     product = Product.query.get(product_id)
#     if product:
#         db.session.delete(product)
#         db.session.commit()
#         return jsonify({"messsage": "Product deleted successfully"})
#     return jsonify({"message": "Product not found"}), 404


# Definir uma rota raiz (Página inicial) e a função que será executada ao  requisitar
@app.route('/test', methods=["GET"]) 
def hello_world():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)