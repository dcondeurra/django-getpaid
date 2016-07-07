# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.db.models import CharField, DecimalField
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)

DEBUG = getattr(settings, "DEBUG", True)

USD_TO_CLP_EXCHANGE = 700
AMOUNT_ORDER_CHARGE = 3000
DEFAULT_CURRENCY = 'CLP'

KCC_TBK_PAGO_URL = 'http://payments.pre.mercadodelfrutero.cl/webpay/cgi-bin/tbk_bp_pago.cgi'
KCC_WORKING_DIR = '/var/www/webpay/cgi-bin/'
KCC_LOG_DIR = '/var/www/webpay/cgi-bin/log/'
KCC_CHECK_MAC_EXEC = '/var/www/webpay/cgi-bin/tbk_check_mac.cgi'


try:
    from siteprefs.toolbox import patch_locals, register_prefs, pref, pref_group

    patch_locals()  # That's bootstrap.

    register_prefs(
        pref(DEFAULT_CURRENCY, verbose_name=_('Moneda por defecto'), static=False, field=CharField(max_length=3),
             help_text='Moneda que se utiliza por defecto para pagar las publicaciones.'),
        pref(AMOUNT_ORDER_CHARGE, verbose_name=_('Costo de publicación'), static=False,
             field=DecimalField(decimal_places=2, max_digits=20),
             help_text='Valor que se cobra por realizar una publicación.'),
        pref(USD_TO_CLP_EXCHANGE, verbose_name=_('Valor del USD en CLP'), static=False,
             field=DecimalField(decimal_places=2, max_digits=5), help_text='Taza de cambio de USD a CLP.'),
    )

except ImportError as exc:
    logger.error(exc, exc_info=True)
    pass
