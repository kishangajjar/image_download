import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'image_download.settings'

ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]

if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')

# also add the parent folder
PARENT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')+1]
if PARENT_FOLDER not in sys.path:
    sys.path.insert(1, PARENT_FOLDER)

def download_image(url):
        
    pass

if __name__ == '__main__':
    url_provided = False
    try:
        url = sys.argv[1]
        url_provided = True
    except IndexError:
        print "Please enter URL into arguments"    
    if url_provided:
        print "INIT",url
        download_image(url)
