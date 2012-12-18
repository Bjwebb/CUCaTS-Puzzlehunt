def pagehit(request):
    try:
        return {'pagehit_id': request.pagehit.pk}
    except AttributeError:
        return {}
