from django.shortcuts import render
from django.db.models import Q
from partner.models import Partner

# Create your views here.
def searchposts(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        # submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(name__icontains=query) | Q(address__icontains=query) | Q(image__icontains=query)

            results= Partner.objects.filter(lookups).distinct()

            context={'results': results,
            }

            return render(request, 'search.html', context)

        else:
            return render(request, 'search.html')

    else:
        return render(request, 'search.html')
        
                     # 'submitbutton': submitbutton
