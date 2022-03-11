from search_app.documents import ProductOptionDocument


def search_obj(query_search):
    result = ProductOptionDocument.search().query(query_search)
    res = elastic_filter(result)
    return res


def elastic_filter(obj):
    try:
        res = obj.filter('match_phrase', is_active=True).filter(
            'match_phrase', product__is_active=True).filter(
            'match_phrase', product__category__is_active=True).filter(
            'match_phrase', product__company__is_active=True).filter(
            'match_phrase', product__company__company__is_active=True
        ).sort('price', '-rate', '-term')
    except AttributeError:
        res = []
    return res
