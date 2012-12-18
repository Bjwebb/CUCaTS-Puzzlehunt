def pagehit(request):
    return {'pagehit_id': request.pagehit.pk}
