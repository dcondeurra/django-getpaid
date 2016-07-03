from django.conf.urls import patterns, url
from getpaid.backends.webpay.views import pago, resultado, close, success, failure

urlpatterns = [
    url(r'^pago/(?P<pk>\d+)/$', pago, name='getpaid-webpay-pago'),
    url(r'^resultado/(?P<pk>\d+)/$', resultado, name='getpaid-webpay-resultado'),
    url(r'^close/$', close, name='getpaid-webpay-close'),
    url(r'^success/$', success, name='getpaid-webpay-success'),
    url(r'^failure/$', failure, name='getpaid-webpay-failure'),
]
