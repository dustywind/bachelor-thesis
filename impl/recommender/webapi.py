
import bottle
import json

from . import DatabaseManager
from .product import Product


@bottle.route('/product/get/<doc_id:int>')
def product_get(doc_id):
    d = product_manager.get_product(doc_id).as_dictionary()
    return json.dumps(
        d
    )

@bottle.route('/product/insert', method='POST')
def product_insert():
    """
    curl -X POST -d "product={'image_name':'img.jpg','terms':{'a':1,'b':3}}"
    """
    product_json = bottle.request.forms.get('product')
    product_dict = json.loads(product_json)

    p = Product()
    p.image_name = product_dict['image_name']
    p.terms = product_dict['terms']

    print(p.as_dictionary())

    product_manager.add_document(p)
    pass



@bottle.route('/vector/default/<doc_id:int>')
def vector_default(doc_id):
    document_id = int(doc_id)
    return json.dumps(
        product_vector_manager
        .get_vector_for_document_id(document_id)
        .as_description_dictionary()
    )

@bottle.route('/vector/df')
def vector_df():
    return json.dumps(
        product_vector_manager
        .get_document_frequency_vector()
        .as_description_dictionary()
    )

@bottle.route('/vector/idf')
def vector_idf():
    return json.dumps(
        product_vector_manager
        .get_inverse_document_frequency_vector()
        .as_description_dictionary()
    )

@bottle.route('/vector/tf/<doc_id:int>')
def vector_tf(doc_id):
    return json.dumps(
        product_vector_manager
        .get_term_frequency_vector(doc_id)
        .as_description_dictionary()
    )

@bottle.route('/vector/tfidf/<doc_id:int>')
def vector_tfidf(doc_id):
    return json.dumps(
        product_vector_manager
        .get_tfidf_vector(doc_id)
        .as_description_dictionary()
    )
    

@bottle.route('/vector/user/<doc_id:int>')
def vector_user_by_id(user_id):
    return json.dumps(
        user_vector_manager.get_user_vector_for_id(user_id)
    )

@bottle.route('/vector/user/<doc_str>')
def vector_user_by_name(user_name):
    return json.dumps(
        user_vector_manager.get_user_vector_for_name(user_name)
    )

@bottle.route('/user/create/<user_name>')
def create_user_by_name(user_name):
    user_vector_manager.create_user(user_name)
    pass


database_manager = None
product_manager = None
product_vector_manager = None
document_manager = None
user_vector_manager = None
term_manager = None


def run(database_path, host, port):
    _init(database_path)
    bottle.run(host=host, port=port, debug=True)

def _init(database_path):
    global database_manager
    global product_manager
    global product_vector_manager
    global document_manager 
    global user_vector_manager 
    global term_manager 
    
    database_manager = DatabaseManager(database_path)
    product_manager = database_manager.get_product_manager()
    product_vector_manager = database_manager.get_product_vector_manager()
    document_manager = database_manager.get_document_manager()
    user_vector_manager  = database_manager.get_user_vector_manager()
    term_manager = database_manager.get_term_manager()

