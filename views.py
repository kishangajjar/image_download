from BeautifulSoup import BeautifulSoup
import urlparse
import urllib2 
#from urllib import urlretrieve
import os
import sys
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


def index(request):
    return render_to_response('index.html', None, context_instance=RequestContext(request))

def download_image(request):
    message = "Please request a POST method"
    # TODO change to POST request
    if request.method == 'POST':
        url = request.POST.get('url', '')
        if url:
            user_ip_address = get_ip_address(request)
            print user_ip_address
            soup = BeautifulSoup(urllib2.urlopen(url))
            print "SOUP -- %s" % soup
            parsed = list(urlparse.urlparse(url))

            for image in soup.findAll("img"):
                print "Image: %(src)s" % image
                filename = image["src"].split("/")[-1]
                parsed[2] = image["src"]
                outpath = os.path.join(out_folder, filename)
                if image["src"].lower().startswith("http"):
                    urlretrieve(image["src"], outpath)
                else:
                    urlretrieve(urlparse.urlunparse(parsed), outpath)
            message = "Download completed.."
        else:
            message = "Please provide URL into arguments"
    else:
        return HttpResponsePermanentRedirect("/")
    return HttpResponse(message)

def get_ip_address(request):
    ip_address = request.META['REMOTE_ADDR']
    return ip_address
