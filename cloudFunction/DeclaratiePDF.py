# -*- coding: utf8 -*-
from fpdf import FPDF

class DeclaratiePDF(FPDF):

    def __init__(self, req_data):
        self.req_data = req_data
        super(DeclaratiePDF, self).__init__()
        self.add_font('FreeSans', '', 'fonts/FreeSans.ttf', uni=True)
        self.add_font('FreeSans', 'B', 'fonts/FreeSansBold.ttf', uni=True)
        self.add_font('FreeSans', 'I', 'fonts/FreeSansOblique.ttf', uni=True)
        self.set_top_margin(20)
        self.set_left_margin(20)
        self.set_right_margin(20)
        self.imgs = ['img/blank-check-box.png', 'img/check-box.png']

    def header(self):
        self.set_font('FreeSans', '', 14)
        self.cell(0, 5, "DECLARAȚIE PE PROPRIE RĂSPUNDERE", ln=1, align='C')

    def _timp_de_noapte(self):
        nume = self.req_data.get('nume', '')
        self.set_font('FreeSans', 'B', 10)
        self.ln(20)
        self.cell(50, 10, 'Subsemnatul/a:', ln=0)
        self.set_font('FreeSans', 'I', 10)
        self.cell(0, 10, '{}'.format(nume), ln=1)

        domiciliu = self.req_data.get('domiciliu', '')
        self.set_font('FreeSans', 'B', 10)
        self.cell(50, 10, 'domiciliat/ă în:', ln=0)
        self.set_font('FreeSans', 'I', 10)
        self.cell(0, 10, '{}'.format(domiciliu), ln=1)

        resedinta = self.req_data.get('resedinta', '')
        self.set_font('FreeSans', 'B', 10)
        self.cell(50, 10, 'cu reședința în fapt în:', ln=0)
        self.set_font('FreeSans', 'I', 10)
        self.cell(0, 10, '{}'.format(resedinta), ln=1)

        dataNastere = self.req_data.get('dataNastere', '')
        localitateNastere = self.req_data.get('localitateNastere', '')
        self.set_font('FreeSans', 'B', 10)
        self.cell(50, 10, 'născut/ă în data de:', ln=0)
        self.set_font('FreeSans', 'I', 10)
        self.cell(30, 10, '{}'.format(dataNastere), ln=0)
        self.set_font('FreeSans', 'B', 10)
        self.cell(30, 10, 'în localitatea', ln=0)
        self.set_font('FreeSans', 'I', 10)
        self.cell(0, 10, '{}'.format(localitateNastere), ln=1)

        self.ln(10)

        self.set_font('FreeSans', '', 10)
        text = "declar pe proprie răspundere, cunoscând prevederile articolului 326 din Codul Penal privind falsul " \
               "în declarații, că mă deplasez în afara locuinței, în intervalul orar 20.00 – 05.00, din " \
               "următorul/următoarele motive:"
        self.multi_cell(0, 5, text)
        self.ln(10)

        motive = self.req_data.get('motive', '')
        # profesional
        text_profesional = "În interes profesional. Menționez că îmi desfășor activitatea profesională la " \
                           "instituția/societatea/organizația: {} \n cu sediul în: {} \n și cu punct/e de lucru: " \
                           "la următoarele adrese: {}"
        if 'profesional' in motive:
            img_profesional = self.imgs[1]
            text_profesional = text_profesional.format(*motive['profesional'])
        else:
            img_profesional = self.imgs[0]
            text_profesional = text_profesional.format("", "", "")
        self.image(img_profesional, 30, 120, 3)
        self.cell(20, 10, '', ln=0)
        self.multi_cell(0, 5, text_profesional, 0, 'L')
        self.ln(10)

        # medical
        text_medical = "Asistență medicală care nu poate fi amânată și nici realizată de la distanță (inclusiv vaccinare)"
        img_medical = self.imgs[1] if 'medical' in motive else self.imgs[0]
        self.image(img_medical, 30, 150, 3)
        self.cell(20, 10, '', ln=0)
        self.multi_cell(0, 5, text_medical, 0, 'L')
        self.ln(5)

        # meds
        text_meds = "Achiziționarea de medicamente"
        img_meds = self.imgs[1] if 'meds' in motive else self.imgs[0]
        self.image(img_meds, 30, 160, 3)
        self.cell(20, 10, '', ln=0)
        self.multi_cell(0, 5, text_meds, 0, 'L')
        self.ln(5)

        # ingrijire
        text_ingrijire = "Îngrijirea/însoțirea copilului și/sau asistența persoanelor vârstnice, bolnave sau cu dizabilități"
        img_ingrijire = self.imgs[1] if 'ingrijire' in motive else self.imgs[0]
        self.image(img_ingrijire, 30, 170, 3)
        self.cell(20, 10, '', ln=0)
        self.multi_cell(0, 5, text_ingrijire, 0, 'L')
        self.ln(5)

        # deces
        text_deces = "Deces al unui membru al familiei"
        img_deces = self.imgs[1] if 'deces' in motive else self.imgs[0]
        self.image(img_deces, 30, 180, 3)
        self.cell(20, 10, '', ln=0)
        self.multi_cell(0, 5, text_deces, 0, 'L')

        self.ln(50)

        data = self.req_data.get('data', '')
        self.cell(130, 10, '{}'.format(data), ln=0)
        self.cell(0, 10, '.'*40, ln=1)

    def composeDoc(self):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self._timp_de_noapte()


if __name__ == '__main__':
    import json
    req_data = json.load(open('rest_call.json'))
    pdf = DeclaratiePDF(req_data)
    pdf.composeDoc()

    encodedStr = pdf.output('form.pdf').encode("utf-8")
    print(encodedStr)
