
from informationretrieval.vector.arithmetic import scalar_multiplication

class RocchioConstant(object):

    a = 1
    b = 0.8
    c = 0.1


def calculate(q_0, list_d_related, list_d_unrelated):
    q_m = (  q_0.scalar_multiplication( RocchioConstant.a )
            + (sum(list_d_related).scalar_multiplication(1/len(list_d_related))).scalar_multiplication(RocchioConstant.b )
            + (sum(list_d_unrelated).scalar_multiplication((1/len(list_d_unrelated))).scalar_multiplication(RocchioConstant.c)
        )
        )
    return q_m


