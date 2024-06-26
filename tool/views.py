from django.shortcuts import render
from django.http import HttpResponse
import tempfile
import pandas as pd
import tabula
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings

def notfound(request):
    return render(request,"notfound.html")

def home(request):
    return render(request,"home.html")

# Función para extraer las tablas de un pdf y guardarlas en un excel
@csrf_exempt
def extract_table_pdf(request):
    # Verifica si la solicitud es POST y si hay un archivo PDF en los archivos enviados
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        archivo_pdf = request.FILES['pdf_file']

        # Validar si el archivo es un PDF
        if not archivo_pdf.name.endswith('.pdf'):
            return HttpResponse('Solo se permiten archivos PDF.', status=400)

        # Validar si el archivo es menor a 25 MB
        if archivo_pdf.size > 26214400:  # 25 MB
            return HttpResponse('El tamaño máximo del PDF permitido es 25 MB.', status=400)

        try:
            # Lee todas las tablas del archivo PDF usando Tabula
            tablas = tabula.read_pdf(archivo_pdf, pages='all', pandas_options={'dtype': str})

            # Crea un archivo temporal para guardar el archivo Excel
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmpfile:
                archivo_excel = tmpfile.name

                # Crea un escritor de Excel usando xlsxwriter
                with pd.ExcelWriter(archivo_excel, engine='xlsxwriter') as writer:
                    worksheet = writer.book.add_worksheet('Sheet1')
                    fila_actual = 0

                    # Variable para almacenar el ancho de cada columna
                    col_widths = []

                    # Itera sobre cada tabla extraída del PDF
                    for tabla in tablas:
                        # Escribe la tabla en la hoja de Excel
                        tabla.to_excel(writer, sheet_name='Sheet1', startrow=fila_actual, index=False)

                        # Actualiza la fila actual
                        fila_actual += len(tabla.index) + 2

                        # Ajusta el ancho de las columnas
                        for col_num, col_name in enumerate(tabla.columns):
                            column_length = tabla[col_name].astype(str).map(len).max()
                            header_length = len(col_name)
                            max_length = max(column_length, header_length) + 2

                            if len(col_widths) > col_num:
                                if col_widths[col_num] < max_length:
                                    col_widths[col_num] = max_length
                            else:
                                col_widths.append(max_length)

                    for i, width in enumerate(col_widths):
                        worksheet.set_column(i, i, width)

                # Lee el contenido del archivo Excel temporal
                with open(archivo_excel, 'rb') as excel_file:
                    contenido_archivo = excel_file.read()

                # Crea una respuesta HTTP con el archivo Excel como adjunto
                response = HttpResponse(contenido_archivo, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="output.xlsx"'
                return response

        except Exception as e:
            return HttpResponse(f'No se pudo procesar el archivo: {str(e)}', status=500)
    else:
        return HttpResponse('No se proporcionó un archivo PDF.', status=400)
    

# Función para obtener el archivo pdf de prueba
def download_pdf(request):
    # Ruta al archivo PDF dentro de la carpeta static
    pdf_path = os.path.join(settings.BASE_DIR, 'mysite', 'static', 'pdf-demo.pdf')

    # Descarga el archivo pdf de prueba
    with open(pdf_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        # Configurar el encabezado para forzar la descarga del archivo
        response['Content-Disposition'] = 'attachment; filename="pdf-demo.pdf"'
        return response