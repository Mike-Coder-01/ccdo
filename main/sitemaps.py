
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    protocol = "https"
    changefreq = "monthly"
    priority = 1.0

    def items(self):
        return ["main:home"]

    def location(self, item):
        return reverse(item)
