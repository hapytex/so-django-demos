from django.shortcuts import render

# Create your views here.

def search_view(request):
    q = request.GET.get("q", "")  # Get query parameter
    return render(request, "search.html", {"q": q})