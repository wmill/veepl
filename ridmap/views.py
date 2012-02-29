# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from myforms import VoteValueForm
from django.template import RequestContext, Context, loader
import os
from django.core.servers.basehttp import FileWrapper
from models import Riding

party_keys = ('blq', 'cpc', 'grn', 'lpc', 'ndp')

def index(request):
    if request.method == 'POST':
        form = VoteValueForm(request.POST)
        if form.is_valid():
            b = form.cleaned_data['blq']
            c = form.cleaned_data['cpc']
            g = form.cleaned_data['grn']
            l = form.cleaned_data['lpc']
            n = form.cleaned_data['ndp']
            new_dir = "/maps/%.2f-%.2f-%.2f-%.2f-%.2f/" % (b, c, g, l, n)
            return HttpResponseRedirect(new_dir)
        else: #form is not valid
            return render_to_response('main.html',
                { 'form': form, }, context_instance=RequestContext(request) )
    data =  {
        'blq' : '9.98',
        'cpc' : '37.65',
        'grn' : '6.78',
        'lpc' : '26.26',
        'ndp' : '18.18',
    }
    form = VoteValueForm(data)
    return render_to_response("main.html", { 'form': form, },context_instance=RequestContext(request))


def redirect(request):
    return HttpResponse("Redirect!")

def projection(request, vote_vals):
    try:
        split_vals = vote_vals.split("-")
        if len(split_vals) != 5:
            #bad link
            raise Http404()
        new_vote = {
            'blq': float(split_vals[0]),
            'cpc': float(split_vals[1]),
            'grn': float(split_vals[2]),
            'lpc': float(split_vals[3]),
            'ndp': float(split_vals[4]),
        }
    except ValueError:
        raise Http404()
    seats = {}
    for p in party_keys:
        seats[p] = 0
    changed = []


    for rid in Riding.objects.all():
        rid_results = {}
        for p in party_keys:
            #this object.__dict__ is pretty cool
            rid_results[p] = new_vote[p] * rid.__dict__[p]
        #now rid_results should containt the proper vote totals
        #this next bit isn't my code, I don't usually use lambdas
        #but it basically turns the hashtable inside out, finds the max of the keys, then returns the value
        #which is the key to the max value of the first hashtable
        t1 = rid_results.items()
        f1 = lambda item: (item[1],item[0])
        c = map(f1,t1)
        b = dict(c)
        max_key = b[max(b.keys())]
        #the above was much cleaner before I needed to track down a bug
        if max_key != rid.victor.lower():
            changed.append({'rid': rid, 'new_victor' : max_key.upper(),})
        seats[max_key] += 1
    #and the new values are calculated
    #use the b trick form above to get the seat coutns in order
    b = dict(map(lambda item: (item[1],item[0]),seats.items()))
    seat_counts = b.keys()
    seat_counts.sort( reverse=True )
    sorted_seat_counts = []
    for sc in seat_counts:
        ht = {}
        ht['seats'] = sc
        ht['party'] = b[sc].upper()[0]
        sorted_seat_counts.append(ht)
    map_link = "http://www.veepl.ca/maps/" + vote_vals + "/map.kmz"
    return render_to_response('result.html', {'seat_counts': sorted_seat_counts, 'changed': changed, 'map_link': map_link,})

def getmap(request, vote_vals):
    #this will just return the map, it's not worth handeling seperatly
    filename = "/home/waltermiller/webapps/dynamic_election_map/myproject/templates/map.kmz"
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='application/vnd.google-earth.kmz')
    response['Content-Length'] = os.path.getsize(filename)
    return response

def mapstyle(request, vote_vals):
    #this will calc the style 
    try:
        split_vals = vote_vals.split("-")
        if len(split_vals) != 5:
            #bad link
            raise Http404()
        new_vote = {
            'blq': float(split_vals[0]),
            'cpc': float(split_vals[1]),
            'grn': float(split_vals[2]),
            'lpc': float(split_vals[3]),
            'ndp': float(split_vals[4]),
        }
    except ValueError:
        raise Http404()
    party_color = {
        'blq' : 'b2ffff00',
        'cpc' : 'b2ff0000',
        'grn' : 'b200ff00',
        'lpc' : 'b20000ff',
        'ndp' : 'b20088ff',
    }
    riding_list = []
    #commented in the above code this was copy/pasted from
    for rid in Riding.objects.all():
        rid_results = {}
        for p in party_keys:
            #this object.__dict__ is pretty cool
            rid_results[p] = new_vote[p] * rid.__dict__[p]
        #find the top party
        t1 = rid_results.items()
        f1 = lambda item: (item[1],item[0])
        c = map(f1,t1)
        b = dict(c)
        max_key = b[max(b.keys())]
        color = party_color[max_key]
        riding_list.append({
            'ed_code': rid.ed_code,
            'color': color,
        })
    t = loader.get_template('kml_base.xml')
    con = Context({'ridings': riding_list})
    return HttpResponse(t.render(con), content_type='application/vnd.google-earth.kml+xml')

def robots(request): 
    filename = "/home/waltermiller/webapps/dynamic_election_map/myproject/templates/robots.txt"
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    return response
