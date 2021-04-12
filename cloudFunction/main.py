from generareDeclaratie import generare_declaratie

def declaratiepdf(request):
    req_data = request.get_json()
    return generare_declaratie(req_data)
