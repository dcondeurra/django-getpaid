# coding: utf-8
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from getpaid.models import Payment, Order
from . import PaymentProcessor, webpay_run
from settings import KCC_TBK_PAGO_URL
import requests
import logging

logger = logging.getLogger(__name__)

@require_POST
@csrf_exempt
def pago(request, pk):

    url = KCC_TBK_PAGO_URL
    data = {}
    for item, value in request.POST.iteritems():
        data.update({item: value})

    response = requests.post(url, data=data, headers={'Accept-encoding': 'html'})

    if response.status_code == 200:
        return HttpResponse(response.content)
    else:
        Payment.objects.delete(pk=pk)
        logger.error(
            'Código %s enviado desde webpay por la petición al método pago.' % response.status_code, exc_info=True)

# @require_POST
@csrf_exempt
def resultado(request, pk):
    with webpay_run('tbk_bp_resultado.cgi', pk) as cgi:
        params = request.body + "\n"
        output, _ = cgi.communicate(params)
        _, body, _ = output.split("\n\n")
        return HttpResponse(body)


@require_POST
@csrf_exempt
def webpay_confirmation(request):
    answer = request.POST.get('TBK_RESPUESTA', None)
    order_pk = int(request.POST['TBK_ORDEN_COMPRA'])
    payment_pk = int(request.POST['TBK_SESION'])

    # Check if Transaction autorized by webpay
    if answer != '0':
        logger.warning('La Orden de compra #%s ha sido rechazada por webpay.' % order_pk, exc_info=True)
        return HttpResponse('RECHAZADO')

    # Check mac validation
    # if not PaymentProcessor.validate(payment, request):
    #     payment.on_failure()
    #     return HttpResponse('RECHAZADO')

    # Check if Order was already paid in another Payment before

    previous_payments = Payment.objects.filter(order__pk=order_pk, status='paid', backend=PaymentProcessor.BACKEND)
    if previous_payments:
        logger.warning('La Orden de compra #%s ya ha sido pagada.' % order_pk, exc_info=True)
        return HttpResponse('RECHAZADO')

    # Check if Order have an a Payment
    try:
        payment = Payment.objects.get(pk=payment_pk, status='in_progress', backend=PaymentProcessor.BACKEND)
        payment.on_success()
    except Payment.DoesNotExist:
        logger.warning('La Orden de compra #%s no tiene pago asociado con #%s.' % (order_pk, payment_pk), exc_info=True)

    return HttpResponse('ACEPTADO')


@require_POST
@csrf_exempt
def success(request):
    site = get_current_site(request)
    payment_pk = request.POST.get('TBK_ID_SESION')
    try:
        payment = Payment.objects.get(pk=payment_pk, paid_on__isnull=False)
    except (Payment.DoesNotExist, ValueError):
        return redirect('getpaid:webpay-failure')
    order = payment.order
    params = payment.journalentry_set.latest('date').params

    PAYMENT_TYPE_DESCRIPTIONS = {u'VN': u'Crédito',
                                 u'VC': u'Crédito',
                                 u'SI': u'Crédito',
                                 u'CI': u'Crédito',
                                 u'VD': u'Redcompra'}

    INSTALLMENT_TYPE_DESCRIPTIONS = {u'VN': u'Sin cuotas',
                                     u'VC': u'Cuotas normales',
                                     u'SI': u'Sin interés',
                                     u'CI': u'Cuotas comercio',
                                     u'VD': u'Venta débito'}

    context = {'payment_items': order.items,
               'order': payment.order,
               'site_url': 'http://%s/' % site,
               'customer_name': order.customer_name,
               'order_id': order.pk,
               'payment_type': PAYMENT_TYPE_DESCRIPTIONS[params['TBK_TIPO_PAGO']],
               'installment_type': INSTALLMENT_TYPE_DESCRIPTIONS[params['TBK_TIPO_PAGO']],
               'last_digits': params['TBK_FINAL_NUMERO_TARJETA'],
               'transaction_date': payment.paid_on,
               'authorization_code': params['TBK_CODIGO_AUTORIZACION'],
               'amount': "{} ${}".format(payment.currency, int(payment.amount)),
               'installments': params['TBK_NUMERO_CUOTAS'].zfill(2)}
    return render(request, 'getpaid/success.html', context)


# @require_POST
@csrf_exempt
def failure(request):
    """
    Method that used for get a failure redirect from webpay.

    TBK_ID_SESION = Payment PK
    TBK_ORDEN_COMPRA = Order PK

    """
    order_id = request.POST.get('TBK_ORDEN_COMPRA')
    order = get_object_or_404(Order, pk=order_id)
    context = {'object': order}
    return render(request, 'getpaid/failure.html', context)