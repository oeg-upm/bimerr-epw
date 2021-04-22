"""TDATA2RDFANDV URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from rest_framework_swagger.views import get_swagger_view

from converter.views import index, mapData, extract_Convert, extract_ConvertEnergyPlus, extract_ConvertDarkSkyAPI, mapDataEnergyPlus, downloadEPW, getEPWYears


schema_view = get_swagger_view(title='API')


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


openapi_info = openapi.Info(
      title="API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="sgonzalez@delicias.dia.fi.upm.es"),
      license=openapi.License(name="BSD License"),
   )

schema_view = get_schema_view(
   openapi_info,
   public=True,
   url='https://weather.bimerr.iot.linkeddata.es/', # CHANGE
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'getInfoMap/', mapData),
    url(r'getInfoMapEP/', mapDataEnergyPlus),
    url(r'makeExtractAndConversion', extract_Convert),
    url(r'makeECEnergyPlus', extract_ConvertEnergyPlus),
    url(r'makeECDarkSkyAPI', extract_ConvertDarkSkyAPI),
    url(r'downloadEPW/',downloadEPW, name='save_contact'),
    url(r'getEPWYears/',getEPWYears, name='get_contact'),
    url(r'^docs(?P<format>\.json)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
