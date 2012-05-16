import os
import sys
import urlparse
import urllib2 
import shutil
from urllib import urlretrieve
from time import gmtime, strftime
from contextlib import closing
from BeautifulSoup import BeautifulSoup
from zipfile import ZipFile, ZIP_DEFLATED
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


def index(request):
    error = ''
    if request.method == "POST":
        data = download_image(request)
        if not data['error']:
            return data['response']
        error = data['error']
    else:
        error = 'Please Enter URL'
    return render_to_response('index.html',
        {
            'error': error,            
        }, context_instance=RequestContext(request))

def download_image(request):
    message = "Please request a POST method"
    # TODO change to POST request
    url = request.POST.get('url', '')
    error = ''
    response = None
    if url:
        user_ip_address = get_ip_address(request)
        soup = BeautifulSoup(urllib2.urlopen(url))
        parsed = list(urlparse.urlparse(url))
        time_encode = strftime("%d%m%Y%H%M%S", gmtime())
        out_folder = '/tmp/images-%s/' % time_encode 
        zip_file = '/tmp/images-%s.zip' % time_encode
        image_urls = []
        count = 0
        for image in soup.findAll("img"):
            try:
                if not image['src'] or 'www.googleadservices.com' in image['src']:
                    continue
            except KeyError:
                continue
            parsed[2] = image["src"]
            if image["src"].lower().startswith("http"):
                absolute_image_path = image["src"]
            else:
                absolute_image_path = urlparse.urlunparse(parsed)
            if absolute_image_path not in image_urls:
                if count <= 100:
                    image_urls.append(absolute_image_path)
                    count += 1
        # download images to local
        get_images_to_local(image_urls, out_folder)
        # zip the directory
        zipdir(out_folder, zip_file)
        # Remove temp dir
        remove_dir(out_folder)
        response = HttpResponse(file(zip_file).read(),mimetype='application/zip')
        response['Content-Disposition'] = 'attachment; filename=images.zip'
    else:
        error = 'Please Enter URL'
    return dict(error=error, response=response)

def get_images_to_local(image_urls, dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    count = 1
    for image_url in image_urls:
        filename = "image-%s-" % count + image_url.split("/")[-1]
        outpath = os.path.join(dir_name, filename)
        urlretrieve(image_url, outpath)
        print outpath
        count += 1
    return

def zipdir(basedir, archivename):
    assert os.path.isdir(basedir)
    with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
        for root, dirs, files in os.walk(basedir):
            #NOTE: ignore empty directories
            for fn in files:
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)+len(os.sep)-1:] #XXX: relative path
                z.write(absfn, zfn)
    return

def remove_dir(dir_name):
    shutil.rmtree(dir_name)
    return True

def get_ip_address(request):
    ip_address = request.META['REMOTE_ADDR']
    return ip_address
