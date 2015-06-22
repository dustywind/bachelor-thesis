


class RocchioConstant(object):
    
    class MetaVariables(type):
        _a = 1
        _b = 0.8
        _c = 0.1
        
        def get_a(cls):
            return cls._a
        def get_b(cls):
            return cls._b
        def get_c(cls):
            return cls._c

        a = property(get_a)
        b = property(get_b)
        c = property(get_c)

    __metaclass__ = MetaVariables


def caluculate(q_0, list_d_related, list_d_unrelated):
    q_m = ( RocchioConstant.a * q_0
            + RocchioConstant.b * ((1/len(list_d_related)) * sum(list_d_related))
            + RocchioConstant.c * ((1/len(list_d_unrelated)) * sum(list_d_unrelated))
        )
    return q_m
    pass



