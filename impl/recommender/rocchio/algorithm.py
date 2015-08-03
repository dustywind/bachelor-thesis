
from ..vector.arithmetic import scalar_multiplication

class RocchioConstant(object):

    a = 1
    b = 0.85
    c = 0.15

default_rocchio_constant = RocchioConstant()

def calculate(q_0, list_d_related, list_d_unrelated, constant=default_rocchio_constant):
    q_m = (
        q_0.scalar_multiplication( constant.a )
        + (sum(list_d_related).scalar_multiplication(1/len(list_d_related))).scalar_multiplication(constant.b )
        + (sum(list_d_unrelated).scalar_multiplication(1/len(list_d_unrelated))).scalar_multiplication(constant.c)
    )
    return q_m








