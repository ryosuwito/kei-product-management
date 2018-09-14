from purchase_order.models import PurchaseOrder
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


def check_current_selling(user, reward):
    now = datetime.datetime.now()
    reward = reward
    orders = PurchaseOrder.objects.filter(user=user, is_verified=True, is_valid=True,
        created_date__year=now.year, created_date__month=now.month)
    return sum([o.total_price for o in orders])
