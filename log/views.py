from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Trip
from .models import Entry
from .forms import EntryForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

# List all trips
def trip_list(request):
    trips = Trip.objects.all()
    return render(request, 'trip_list.html', {'trips': trips})

# View details of a single trip
def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    return render(request, 'trip_detail.html', {'trip': trip})

# Create a new trip
def trip_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        location = request.POST['location']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        theme = request.POST['theme']
        description = request.POST['description']
        photo = request.FILES.get('photo')

        Trip.objects.create(
            title=title, location=location,
            start_date=start_date, end_date=end_date,
            theme=theme, description=description,
            photo=photo
        )
        return redirect('trip_list')
    return render(request, 'trip_form.html')

# Update an existing trip
def trip_update(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == 'POST':
        trip.title = request.POST['title']
        trip.location = request.POST['location']
        trip.start_date = request.POST['start_date']
        trip.end_date = request.POST['end_date']
        trip.theme = request.POST['theme']
        trip.description = request.POST['description']
        if request.FILES.get('photo'):
            trip.photo = request.FILES['photo']
        trip.save()
        return redirect('trip_detail', pk=trip.pk)
    return render(request, 'trip_form.html', {'trip': trip})

# Delete a trip
def trip_delete(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == 'POST':
        trip.delete()
        return redirect('trip_list')
    return render(request, 'trip_confirm_delete.html', {'trip': trip})


# List all entries for a specific trip
def entry_list(request, trip_pk):
    trip = get_object_or_404(Trip, pk=trip_pk)
    entries = trip.entries.all()
    return render(request, 'entry_list.html', {'trip': trip, 'entries': entries})

# View details of a single entry
def entry_detail(request, trip_pk, entry_pk):
    entry = get_object_or_404(Entry, pk=entry_pk, trip_id=trip_pk)
    return render(request, 'entry_detail.html', {'entry': entry})

# Create a new entry for a specific trip
def entry_create(request, trip_pk):
    trip = get_object_or_404(Trip, pk=trip_pk)
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.trip = trip
            entry.save()
            return redirect('entry_list', trip_pk=trip.pk)
    else:
        form = EntryForm()
    return render(request, 'entry_form.html', {'form': form, 'trip': trip})

# Update an existing entry
def entry_update(request, trip_pk, entry_pk):
    trip = get_object_or_404(Trip, pk=trip_pk)
    entry = get_object_or_404(Entry, pk=entry_pk, trip=trip)

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('entry_list', trip_pk=trip.pk)
    else:
        form = EntryForm(instance=entry)

    return render(request, 'entry_form.html', {'form': form, 'trip': trip, 'entry': entry})

# Delete an entry
def entry_delete(request, trip_pk, entry_pk):
    entry = get_object_or_404(Entry, pk=entry_pk, trip_id=trip_pk)
    if request.method == 'POST':
        entry.delete()
        return redirect('entry_list', trip_pk=trip_pk)
    return render(request, 'entry_confirm_delete.html', {'entry': entry})