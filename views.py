from django.shortcuts import render_to_response
from django.conf import settings

def render_about(request, site_url=settings.SITE_URL, shortname=settings.DISQUS_WEBSITE_SHORTNAME):
        return render_to_response('about.html', {'site_url': site_url,
                                                 'shortname': shortname})

