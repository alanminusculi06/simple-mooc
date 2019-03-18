from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView

from .models import Thread

# index = TemplateView.as_view(template_name='index.html')
# class ForumView(TemplateView):
#     template_name = 'index.html'

#     def get(self, request, *args, **kwargs):
#         return render(request, template_name)

class ForumView(ListView):
    model = Thread
    paginate_by = 10
    template_name = 'threads.html'

index = ForumView.as_view()
