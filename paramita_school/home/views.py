from django.shortcuts import render
from .models import (
    SiteSettings, NavMenuItem, BannerSlide, Feature,
    Introduction, AboutSection, PrincipalMessage,
    Testimonial, CTABanner, SocialFeed, FooterInfo,
)


def home(request):
    context = {
        'site'          : SiteSettings.load(),
        'nav_items'     : NavMenuItem.objects.filter(parent__isnull=True).prefetch_related('children'),
        'slides'        : BannerSlide.objects.filter(is_active=True).order_by('order'),
        'features'      : Feature.objects.filter(is_active=True).order_by('order'),
        'introduction'  : Introduction.objects.first(),
        'about'         : AboutSection.objects.first(),
        'principal'     : PrincipalMessage.objects.first(),
        'testimonials'  : Testimonial.objects.filter(is_active=True),
        'cta'           : CTABanner.objects.first(),
        'social_feeds'  : SocialFeed.objects.filter(is_active=True).order_by('order'),
        'footer'        : FooterInfo.objects.first(),
    }
    return render(request, 'home/index.html', context)
