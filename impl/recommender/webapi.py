
import bottle
import json

from . import DatabaseManager
from .product import Product
import recommender.vector.arithmetic


@bottle.route('/product/get/<doc_id:int>')
def product_get(doc_id):
    d = product_manager.get_product(doc_id).as_dictionary()
    return d

@bottle.route('/product/all')
def product_get_all():
    l = [ p.as_dictionary() for p in product_manager.get_all_products()]
    result = {'result': l}
    #bottle.response.content_type = 'application/json'
    return result

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

    product_manager.add_document(p)
    pass



@bottle.route('/vector/default/<doc_id:int>')
def vector_default(doc_id):
    d = (product_vector_manager
        .get_vector_for_document_id(doc_id)
        .as_dictionary()
        )
    result = {'result': d}
    return result

@bottle.route('/vector/df')
def vector_df():
    d = (
        product_vector_manager
        .get_document_frequency_vector()
        .as_dictionary()
    )
    result = {'result': d}
    return result

@bottle.route('/vector/idf')
def vector_idf():
    d = (
        product_vector_manager
        .get_inverse_document_frequency_vector()
        .as_dictionary()
    )
    result = {'result': d}
    return result

@bottle.route('/vector/tf/<doc_id:int>')
def vector_tf(doc_id):
    d = (
        product_vector_manager
        .get_term_frequency_vector(doc_id)
        .as_dictionary()
    )
    result = {'result': d}
    return result

@bottle.route('/vector/tfidf/<doc_id:int>')
def vector_tfidf(doc_id):
    d = (
        product_vector_manager
        .get_tfidf_vector(doc_id)
        .as_dictionary()
    )
    result = {'result': d}
    return result
    

@bottle.route('/vector/user/<user_id:int>')
def vector_user_by_id(user_id):
    d = (
        user_vector_manager
            .get_user_vector_for_id(user_id)
            .as_dictionary()
    )
    result = {'result': d}
    return result

@bottle.route('/vector/user/<user_name>')
def vector_user_by_name(user_name):
    d = (
        user_vector_manager
            .get_user_vector_for_name(user_name)
            .as_dictionary()
    )
    result = {'result': d}
    return result

@bottle.route('/user/create/<user_name>')
def create_user_by_name(user_name):
    user_vector_manager.create_user(user_name)
    pass

@bottle.route('/user/exists/<user_name>')
def exists_user_by_name(user_name):
    d = {}
    d['exists'] = user_vector_manager.has_user_with_name(user_name)
    result = {'result': d}
    return result

@bottle.route('/user/setpreference/<user_name>/<product_id:int>')
def add_preference_to_user(user_name, product_id):
    user_id = user_vector_manager.get_user_id_from_name(user_name)
    user_vector_manager.set_user_preference(user_id, product_id, True)
    pass

@bottle.route('/user/setnopreference/<user_name>/<product_id:int>')
def add_preference_to_user(user_name, product_id):
    user_id = user_vector_manager.get_user_id_from_name(user_name)
    user_vector_manager.set_user_preference(user_id, product_id, False)
    pass


@bottle.route('/recommendations/<user_name>/<k:int>')
def get_recommendation(user_name, k):
    vector = user_vector_manager.get_user_vector_for_name(user_name)
    others = product_vector_manager.get_all_vectors()
    recommendations = vector_arithmetic.k_nearest_neighbours(k, vector, others)
    result = {'result': recommendations}
    return result
    

database_manager = None
product_manager = None
product_vector_manager = None
document_manager = None
user_vector_manager = None
term_manager = None

vector_arithmetic = recommender.vector.arithmetic

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

