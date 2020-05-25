import os

def root_url(request):
    """
    Pass your root_url from the settings.py
    """
    return {'SITE_URL': os.path.dirname(os.path.abspath(__file__))}