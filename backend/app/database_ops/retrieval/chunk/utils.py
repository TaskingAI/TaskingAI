def get_m_ef_construction(capacity: int, embedding_size: int):
    if capacity <= 1000:
        m, ef_construction = 8, 32
    else:
        # todo: support more capacity
        raise Exception("capacity is too large")

    return m, ef_construction


def get_ef_search(capacity: int, num_chunks: int, embedding_size: int):
    m, ef_construction = get_m_ef_construction(capacity=capacity, embedding_size=embedding_size)
    ef_search = round(ef_construction * 0.65)
    return ef_search
