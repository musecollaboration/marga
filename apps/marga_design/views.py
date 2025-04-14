from django.shortcuts import render


# макет https://preview.colorlib.com/#marga
# https://colorlib.com/wp/templates/

def index(request):
    return render(request, 'marga_design/home.html')
