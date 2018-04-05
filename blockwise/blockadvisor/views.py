from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Location, Crime
from django.views import generic

# Create your views here.

def index(request):
    num_instances=2

    num_locations=Location.objects.all().count()

    return render(
        request,
        'index.html',
        context={'num_locations':num_locations}
    )

class LocationListView(generic.ListView):
    model = Location
    paginate_by = 10
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(LocationListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class LocationDetailView(generic.DetailView):
    model = Location
