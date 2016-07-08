from django.conf.urls import patterns, url
from getpaid.backends.webpay.views import pago, resultado, webpay_confirmation, success, failure, reject

urlpatterns = [
    url(r'^pago/(?P<pk>\d+)/$', pago, name='webpay_pago'),
    url(r'^resultado/(?P<pk>\d+)/$', resultado, name='webpay_resultado'),
    url(r'^confirmation/$', webpay_confirmation, name='webpay_confirmation'),
    url(r'^success/$', success, name='webpay_success'),
    url(r'^reject/$', reject, name='webpay_reject'),
    url(r'^failure/$', failure, name='webpay_failure'),
]
