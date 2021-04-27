from django.shortcuts import render

import calendar
from .admin_calendar import EventCalendar
from django.views import generic

from .forms import SendEmailForm
from .models import Event, Customer
from datetime import timedelta
from django.utils.safestring import mark_safe
from datetime import datetime
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        temp = datetime(year, month, 1)
        return temp
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get requested month

        d = get_date(self.request.GET.get('month', None))

        cal = EventCalendar()
        html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')

        context['calendar'] = mark_safe(html_calendar)

        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


class SendUserEmails(FormView):
    template_name = 'send_email.html'
    form_class = SendEmailForm
    success_url = reverse_lazy('mail_sent')

    def form_valid(self, form):
        users = form.cleaned_data['users']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        for user in users:
            print(user)
            print(user.email)

            mail = EmailMessage(
                subject,
                'Hi''\n' + user.username + '\n' + message,
                'admin@EFS.com',
                [user.email])

            mail.send()
        return redirect('mail_sent')


def mail_sent(request):
    return render(request, 'mail_sent.html')
