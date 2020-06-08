from django.shortcuts import render
from django.utils import timezone
from django.views import generic

class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        template_name = 'mir/index.html'

        context = {
            'date_time': str(timezone.now()),
        }

        return render(request, template_name, context=context)