from DeclaratiePDF import DeclaratiePDF

def generare_declaratie(req_data):
    pdf = DeclaratiePDF(req_data)
    print(req_data)
    pdf.composeDoc()
    encoded = pdf.output(dest='S').encode("latin-1")

    try:
        return encoded
    except Exception as e:
        return str(e), 500
