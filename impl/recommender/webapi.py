

import bottle
import json

from . import DatabaseManager


@bottle.route('/hello/<name>')
def greeting(name):
    return bottle.template('<b>Hello {{name}}</b>!', name=name)


@bottle.route('/vector/default/<doc_id>')
def vector_default(doc_id):
    document_id = int(doc_id)
    return bottle.template('{{vector}}', vector=json.dumps(
            dbm.get_product_vector_manager().get_vector_for_document_id(document_id).as_description_dictionary()
        )
    )

@bottle.route('/vector/df')
def vector_df():
    return bottle.template('{{vector}}', vector=json.dumps(
            dbm.get_product_vector_manager().get_document_frequency_vector().as_description_dictionary()
        )
    )

@bottle.route('/vector/idf')
def vector_idf():
    return bottle.template('{{vector}}', vector=json.dumps(
            dbm.get_product_vector_manager().get_inverse_document_frequency_vector().as_description_dictionary()
        )
    )

@bottle.route('/vector/tf/<doc_id>')
def vector_tf(doc_id):
    document_id = int(doc_id)
    return bottle.template('{{vector}}', vector=json.dumps(
            dbm.get_product_vector_manager().get_term_frequency_vector(document_id).as_description_dictionary()
        )
    )

@bottle.route('/vector/tfidf/<doc_id>')
def vector_tfidf(doc_id):
    document_id = int(doc_id)
    return bottle.template('{{vector}}', vector=json.dumps(
            dbm.get_product_vector_manager().get_tfidf_vector(document_id).as_description_dictionary()
        )
    )
    
def run(database_path, host, port):
    global dbm
    dbm = DatabaseManager(database_path)
    bottle.run(host=host, port=port, debug=True)





