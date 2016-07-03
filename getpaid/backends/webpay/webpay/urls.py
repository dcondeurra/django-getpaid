from django.conf.urls import patterns, url
from getpaid.backends.webpay.views import pago, resultado, close, success, failure

urlpatterns = [
    url(r'^pago/(?P<pk>\d+)/$', pago, name='webpay-pago'),
    url(r'^resultado/(?P<pk>\d+)/$', resultado, name='webpay-resultado'),
    url(r'^purchase/$', close, name='webpay-purchase'),
    url(r'^success/$', success, name='webpay-success'),
    url(r'^failure/$', failure, name='webpay-failure'),
]
