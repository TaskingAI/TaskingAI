def get_m_ef_construction(capacity: int, embedding_size: int):
    delta_m, delta_ef_construction = 0, 0
    if embedding_size <= 384:
        pass
    elif embedding_size <= 768:
        delta_m, delta_ef_construction = 0.075, 0.075
    elif embedding_size <= 2000:
        delta_m, delta_ef_construction = 0.15, 0.15
    else:
        raise Exception("embedding_size too large")

    if capacity <= 1000:
        m, ef_construction = 8, 32
    elif capacity <= 10000:
        m, ef_construction = 16, 64
    elif capacity <= 100000:
        m, ef_construction = 24, 128
    elif capacity <= 1000000:
        m, ef_construction = 32, 192
    else:
        raise Exception("capacity is too large")

    m = round(m * (1 + delta_m))
    ef_construction = round(ef_construction * (1 + delta_ef_construction))
    return m, ef_construction


def get_ef_search(capacity: int, num_chunks: int, embedding_size: int):
    m, ef_construction = get_m_ef_construction(capacity=capacity, embedding_size=embedding_size)
    ef_search = round(ef_construction * 0.65)
    return ef_search
