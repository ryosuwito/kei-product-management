from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from database_wilayah.models import Provinsi, Kota, Kecamatan, Kelurahan
from .shipping_check import get_province as province
from .shipping_check import get_province_id as province_id
from .shipping_check import get_city_id as city_id
from .shipping_check import get_city as city
from .shipping_check import get_cost as cost
from .forms import ShippingOriginForm
from .models import ShippingOrigin

@user_passes_test(lambda u:u.is_staff,login_url='/admin/login')
def set_shipping_origin(request):
    origins = ShippingOrigin.objects.all()
    action = request.POST.get('action', 'none')
    form = ShippingOriginForm()
    if request.method == "POST":
        if(action == 'DELETE'):
            origin_pk = request.POST.get('origin_pk')
            try:
                origin = ShippingOrigin.objects.get(pk=origin_pk)
                origin.delete()
            except:
                pass
        else:
            form = ShippingOriginForm(request.POST)
            if form.is_valid():
                response = HttpResponse("NOT OK")
                data = form.cleaned_data
                """
                */ cek apakah semua field lengkap, jika tidak kembalikan form 
                """
                if request.POST['provinsi'] and request.POST['kota'] and \
                request.POST['kecamatan'] and request.POST['kelurahan'] and request.POST['name']:
                    name = data.get('name')
                    alamat = data.get('alamat')
                    provinsi = Provinsi.objects.get(pk=request.POST['provinsi'])
                    kota = Kota.objects.get(pk=data.get('kota'))
                    kecamatan = Kecamatan.objects.get(pk=data.get('kecamatan'))
                    kelurahan = Kelurahan.objects.get(pk=data.get('kelurahan'))

                shipping_origin = ShippingOrigin.objects.get_or_create(name = name)[0]
                shipping_origin.provinsi = provinsi
                shipping_origin.kota = kota
                shipping_origin.kecamatan = kecamatan
                shipping_origin.kelurahan = kelurahan
                shipping_origin.alamat = alamat
                shipping_origin.save()
                return HttpResponseRedirect('/admin/shipping_backend/shippingorigin/')
    return render(request, "shipping_backend/set_origin.html", {"form":form, "origins":origins})

def get_province(request):
    return HttpResponse(province())

def get_province_id(request):
    return HttpResponse(province_id('Papua Barat'))

def get_city(request):
    return HttpResponse(city())

def get_city_id(request):
    return HttpResponse(city_id('3', 'Kabupaten Tangerang'))

def get_cost(request):
    return HttpResponse(cost(request.user, 'tiki'))