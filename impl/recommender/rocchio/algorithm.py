
from ..vector.arithmetic import scalar_multiplication

def default_weights():
    a = 1
    b = 0.85
    c = 0.15
    return (a, b, c)


def calculate(q_0, list_d_related, list_d_unrelated, weights=default_weights()):
    a, b, c = weights
    q_m = (
        q_0.scalar_multiplication( a )
        + (sum(list_d_related).scalar_multiplication(1/len(list_d_related))).scalar_multiplication(b )
        + (sum(list_d_unrelated).scalar_multiplication(1/len(list_d_unrelated))).scalar_multiplication(c)
    )
    return q_m

