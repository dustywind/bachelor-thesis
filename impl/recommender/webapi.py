
import bottle
import json
import random

from . import DatabaseManager
from .product import Product
import recommender.vector.arithmetic
import recommender.rocchio.algorithm


@bottle.route('/product/get/<doc_id:int>')
def product_get(doc_id):
    d = product_manager.get_product(doc_id).as_dictionary()
    result = {'result': d}
    return result

@bottle.route('/product/remove/<doc_id:int>', method='DELETE')
def product_remove(doc_id):
    try:
        product_manager.remove_document(doc_id)
    except:
        return {'result': False}
    return {'result': True}

@bottle.route('/product/all')
def product_get_all():
    l = [ p.as_dictionary() for p in product_manager.get_all_products()]
    result = {'result': l}
    #bottle.response.content_type = 'application/json'
    return result

@bottle.route('/product/random/<count:int>')
def product_random(count):
    products = product_manager.get_all_products()
    rands = []
    while len(rands) < count:
        index = random_generator.randint(0, len(products)-1)

        rands.append(products[index].as_dictionary())

        products.remove(products[index])
        pass
    result = {'result': rands};
    return result

@bottle.route('/product/insert', method='POST')
def product_insert():
    """
    curl -X POST -d "product={'image_name':'img.jpg','terms':{'a':1,'b':3}}"
    """
    try:
        product_json = bottle.request.forms.get('product')
        product_dict = json.loads(product_json)

        p = Product()
        p.image_name = product_dict['image_name']
        p.terms = product_dict['terms']

        product_manager.add_document(p)
    except:
        return {'result': False}
    return {'result': True}



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

@bottle.route('/user/all')
def get_all_users():
    user_list = user_vector_manager.get_all_users_by_name()
    result = {'result': user_list}
    return result

@bottle.route('/user/create/<user_name>')
def create_user_by_name(user_name):
    user_vector_manager.create_user(user_name)
    return {'result': True}

@bottle.route('/user/exists/<user_name>')
def exists_user_by_name(user_name):
    d = {}
    d['exists'] = user_vector_manager.has_user_with_name(user_name)
    result = {'result': d}
    return result

@bottle.route('/user/remove/<user_name>', method='DELETE')
def remove_user_by_name(user_name):
    try:
        user_id = user_vector_manager.get_user_id_for_name(user_name)
        user_vector_manager.remove_user(user_id)
    except:
        return {'result': False}
    return {'result': True}

@bottle.route('/user/createifnotexist/<user_name>')
def create_user_if_not_exists(user_name):
    if not user_vector_manager.has_user_with_name(user_name):
        create_user_by_name(user_name)
    return {'result': True}

@bottle.route('/user/setpreference/<user_name>/<product_id:int>')
def add_preference_to_user(user_name, product_id):
    user_id = user_vector_manager.get_user_id_for_name(user_name)
    user_vector_manager.set_user_preference(user_id, product_id, True)
    return {'result': True}

@bottle.route('/user/setnopreference/<user_name>/<product_id:int>')
def add_preference_to_user(user_name, product_id):
    user_id = user_vector_manager.get_user_id_for_name(user_name)
    user_vector_manager.set_user_preference(user_id, product_id, False)
    return {'result': True}

@bottle.route('/user/update/<user_name>')
def get_user_update(user_name):
    user_id = user_vector_manager.get_user_id_for_name(user_name)

    weights = recommender.rocchio.default_weights()

    update_user(user_id, weights)

    return {'result': True}

@bottle.route('/user/update/<user_name>/<alpha:int>/<beta:int>/<gamma:int>')
def get_user_update(user_name, alpha, beta, gamma):
    user_id = user_vector_manager.get_user_id_for_name(user_name)

    if alpha < 0:
        alpha = 0
    elif alpha > 100:
        alpha = 100;
    if beta < 0:
        beta = 0
    elif beta > 100:
        beta = 100
    if gamma < 0:
        gamma = 0
    elif gamma > 100:
        gamma = 100

    weights = alpha / 100, beta / 100, gamma / 100

    update_user(user_id, weights)
    return {'result': True}


@bottle.route('/user/relevant/<user_name>')
def get_user_preference(user_name):
    user_id = user_vector_manager.get_user_id_for_name(user_name)
    relevant_vectors = user_vector_manager.get_relevant_document_vector_list(user_id)
    relevant_products = [
        product_manager.get_product(v.document_id).as_dictionary()
        for v in relevant_vectors
    ]

    result = {'result': relevant_products}
    return result

@bottle.route('/user/nonrelevant/<user_name>')
def get_user_no_preference(user_name):
    user_id = user_vector_manager.get_user_id_for_name(user_name)
    non_relevant_vectors = user_vector_manager.get_non_relevant_document_vector_list(user_id)
    non_relevant_products = [
        product_manager.get_product(v.document_id).as_dictionary()
        for v in non_relevant_vectors
    ]

    result = {'result': non_relevant_products}
    return result

@bottle.route('/recommendations/<user_name>/<k:int>')
def get_recommendation(user_name, k):
    vector = user_vector_manager.get_user_vector_for_name(user_name)
    others = product_vector_manager.get_all_vectors()

    #distance_function = recommender.vector.arithmetic.hamming_distance
    #distance_function = recommender.vector.arithmetic.euclidean_distance

    recommendations = vector_arithmetic.k_nearest_neighbours(k, vector, others)
    products = [
        product_manager.get_product(vector.document_id).as_dictionary()
        for _, vector in recommendations
    ]
    result = {'result': products}
    return result
    

database_manager = None
product_manager = None
product_vector_manager = None
document_manager = None
user_vector_manager = None
term_manager = None

random_generator = None

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

    global random_generator
    
    database_manager = DatabaseManager(database_path)
    product_manager = database_manager.get_product_manager()
    product_vector_manager = database_manager.get_product_vector_manager()
    document_manager = database_manager.get_document_manager()
    user_vector_manager  = database_manager.get_user_vector_manager()
    term_manager = database_manager.get_term_manager()

    random_generator = random.Random()

def update_user(user_id, weights):
    user_vector = user_vector_manager.get_user_vector_for_id(user_id)
    relevant = user_vector_manager.get_relevant_document_vector_list(user_id)
    non_relevant = user_vector_manager.get_non_relevant_document_vector_list(user_id)

    uvector = recommender.rocchio.algorithm.calculate(user_vector, relevant, non_relevant, weights)
    user_vector_manager.update_user_vector(user_id, uvector);
    pass
