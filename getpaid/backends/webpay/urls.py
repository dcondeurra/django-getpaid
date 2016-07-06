from django.conf.urls import patterns, url
from getpaid.backends.webpay.views import pago, resultado, close, success, failure

urlpatterns = [
    url(r'^pago/(?P<pk>\d+)/$', pago, name='webpay_pago'),
    url(r'^resultado/(?P<pk>\d+)/$', resultado, name='webpay_resultado'),
    url(r'^purchase/$', close, name='webpay_purchase'),
    url(r'^success/$', success, name='webpay_success'),
    url(r'^failure/$', failure, name='webpay_failure'),
]
