from django.shortcuts import redirect, get_object_or_404 , render
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .models import Table, Booking
from datetime import date

def table_list(request):
    tables = Table.objects.filter(available=True)

    return render(request, 'booking/tables.html', {'tables': tables})

@login_required
def reserve_table(request, table_id):
    if request.method == 'POST':
        with transaction.atomic():
            table = get_object_or_404(Table, id=table_id, available=True)

            Booking.objects.create(
                user=request.user,
                table=table,
                booking_date=date.today(),
            )

            table.is_available = False
            table.save()

        return redirect('menu:menu_list')
    return redirect('booking:table_list')