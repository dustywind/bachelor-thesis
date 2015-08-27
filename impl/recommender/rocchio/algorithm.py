
from ..vector.arithmetic import scalar_multiplication
from ..vector.empty import EmptyVectorCreator

def default_weights():
    a = 1
    b = 0.85
    c = 0.15
    return (a, b, c)


def calculate(q_0, list_d_related, list_d_unrelated, weights=default_weights()):
    a, b, c = weights

    def calculate_a():
        return q_0.scalar_multiplication( a )

    def calculate_b():
        if len(list_d_related) > 0:
            return (
                    sum(list_d_related).scalar_multiplication(1/len(list_d_related))
                ).scalar_multiplication(b )
        return null_vector()

    def calculate_c():
        if len(list_d_unrelated) > 0:
            return (
                    sum(list_d_unrelated)
                    .scalar_multiplication(1/len(list_d_unrelated))
                ).scalar_multiplication(c)
        return null_vector()

    def null_vector():
        empty = q_0.scalar_multiplication(0)
        return empty
        
    q_m = calculate_a() + calculate_b() - calculate_c()
    """
    # this simpler calculation may divede through zero --> big problem!
    q_m = (
        q_0.scalar_multiplication( a )
        + (sum(list_d_related).scalar_multiplication(1/len(list_d_related))).scalar_multiplication(b )
        - (sum(list_d_unrelated).scalar_multiplication(1/len(list_d_unrelated))).scalar_multiplication(c)
    )
    """
    return q_m



