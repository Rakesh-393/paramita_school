from django.db import models
from django.utils.html import mark_safe


# ─── NAVBAR ─────────────────────────────────────────────────────────────────

class SiteSettings(models.Model):
    """Singleton – stores logo and top-level site info."""
    logo            = models.ImageField(upload_to='site/', help_text='Main navbar logo')
    footer_logo     = models.ImageField(upload_to='site/', blank=True, null=True)
    parent_login_url = models.URLField(default='#', blank=True)
    tagline         = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name        = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def logo_preview(self):
        if self.logo:
            return mark_safe(f'<img src="{self.logo.url}" height="60" />')
        return '—'
    logo_preview.short_description = 'Preview'


class NavMenuItem(models.Model):
    """Top-level or child nav items (supports one level of dropdown)."""
    label   = models.CharField(max_length=100)
    url     = models.CharField(max_length=300, default='#')
    parent  = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    order   = models.PositiveIntegerField(default=0)
    open_new_tab = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']
        verbose_name        = 'Nav Menu Item'
        verbose_name_plural = 'Nav Menu Items'

    def __str__(self):
        return f'{"— " if self.parent else ""}{self.label}'


# ─── HERO BANNER ─────────────────────────────────────────────────────────────

class BannerSlide(models.Model):
    image       = models.ImageField(upload_to='banner/')
    title       = models.CharField(max_length=200)
    subtitle    = models.CharField(max_length=400, blank=True)
    btn1_text   = models.CharField(max_length=100, blank=True, verbose_name='Button 1 Text')
    btn1_link   = models.URLField(blank=True, verbose_name='Button 1 Link')
    btn2_text   = models.CharField(max_length=100, blank=True, verbose_name='Button 2 Text')
    btn2_link   = models.URLField(blank=True, verbose_name='Button 2 Link')
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name        = 'Banner Slide'
        verbose_name_plural = 'Banner Slides'

    def __str__(self):
        return self.title

    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" height="80" style="border-radius:6px;" />')
        return '—'
    image_preview.short_description = 'Preview'


# ─── FEATURES STRIP ──────────────────────────────────────────────────────────

class Feature(models.Model):
    icon        = models.ImageField(upload_to='features/')
    title       = models.CharField(max_length=200)
    description = models.TextField()
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def icon_preview(self):
        if self.icon:
            return mark_safe(f'<img src="{self.icon.url}" height="60" />')
        return '—'
    icon_preview.short_description = 'Icon'


# ─── INTRODUCTION ────────────────────────────────────────────────────────────

class Introduction(models.Model):
    section_label = models.CharField(max_length=100, default='INTRODUCTION')
    heading       = models.CharField(max_length=300)
    content       = models.TextField()
    image         = models.ImageField(upload_to='intro/')

    class Meta:
        verbose_name        = 'Introduction Section'
        verbose_name_plural = 'Introduction Section'

    def __str__(self):
        return self.heading

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


# ─── ABOUT SECTION ───────────────────────────────────────────────────────────

class AboutSection(models.Model):
    section_label = models.CharField(max_length=100, default='About Us')
    heading       = models.CharField(max_length=300)
    content       = models.TextField()
    image         = models.ImageField(upload_to='about/')
    btn_text      = models.CharField(max_length=100, blank=True)
    btn_link      = models.URLField(blank=True)

    class Meta:
        verbose_name        = 'About Section'
        verbose_name_plural = 'About Section'

    def __str__(self):
        return self.heading

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


# ─── PRINCIPAL MESSAGE ───────────────────────────────────────────────────────

class PrincipalMessage(models.Model):

    IMAGE_STYLE_CHOICES = [
        ('circle',  'Circle — Classic round portrait'),
        ('square',  'Square — Sharp professional look'),
        ('rounded', 'Rounded Square — Modern soft edges'),
        ('hexagon', 'Hexagon — Unique geometric frame'),
    ]

    salutation  = models.CharField(max_length=200, default='Dear Parents, Students, and Esteemed Staff Members,')
    message     = models.TextField()
    name        = models.CharField(max_length=200)
    designation = models.CharField(max_length=200, default='Principal')
    image       = models.ImageField(upload_to='principal/')
    image_style = models.CharField(
                      max_length=20,
                      choices=IMAGE_STYLE_CHOICES,
                      default='circle',
                      verbose_name='Image Frame Style',
                      help_text='Choose the shape of the principal photo frame'
                  )
    btn_text    = models.CharField(max_length=100, default='Know More')
    btn_link    = models.CharField(max_length=300, blank=True, default='#', help_text='e.g. / or https://example.com')

    class Meta:
        verbose_name        = 'Principal Message'
        verbose_name_plural = 'Principal Message'

    def __str__(self):
        return f'Message from {self.name}'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


# ─── TESTIMONIALS ────────────────────────────────────────────────────────────

class Testimonial(models.Model):
    RATING_CHOICES = [(i, '★' * i) for i in range(1, 6)]

    name      = models.CharField(max_length=200)
    avatar    = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    review    = models.TextField()
    rating    = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    date      = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.name} — {"★" * self.rating}'

    def stars_html(self):
        filled = '★' * self.rating
        empty  = '☆' * (5 - self.rating)
        return mark_safe(f'<span style="color:#C9A227;">{filled}</span>{empty}')
    


# ─── CTA BANNER ──────────────────────────────────────────────────────────────

class CTABanner(models.Model):
    heading     = models.CharField(max_length=300)
    subheading  = models.CharField(max_length=400, blank=True)
    btn_text    = models.CharField(max_length=100)
    btn_link    = models.URLField()
    bg_image    = models.ImageField(upload_to='cta/', blank=True, null=True)

    class Meta:
        verbose_name        = 'CTA Banner'
        verbose_name_plural = 'CTA Banner'

    def __str__(self):
        return self.heading

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


# ─── SOCIAL FEED ─────────────────────────────────────────────────────────────

class SocialFeed(models.Model):
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook',  'Facebook'),
        ('youtube',   'YouTube'),
        ('other',     'Other'),
    ]
    platform         = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='instagram')
    custom_platform  = models.CharField(max_length=50, blank=True, help_text='Specify platform name if "Other" is selected')
    image     = models.ImageField(upload_to='social/')
    link      = models.URLField()
    caption   = models.CharField(max_length=300, blank=True)
    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name        = 'Social Feed Post'
        verbose_name_plural = 'Social Feed Posts'

    def __str__(self):
        return f'{self.platform.title()} — {self.caption[:50] if self.caption else self.link}'

    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" height="80" style="border-radius:6px;"/>')
        return '—'
    image_preview.short_description = 'Preview'


# ─── FOOTER ──────────────────────────────────────────────────────────────────

class FooterInfo(models.Model):
    address       = models.TextField()
    phone1        = models.CharField(max_length=20)
    phone2        = models.CharField(max_length=20, blank=True)
    email         = models.EmailField()
    map_embed_url = models.TextField(help_text='Google Maps embed src URL')
    facebook_url  = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url   = models.URLField(blank=True)
    linkedin_url  = models.URLField(blank=True)
    copyright_text = models.CharField(max_length=300, default='© 2025 Paramita Schools. All Rights Reserved.')

    class Meta:
        verbose_name        = 'Footer Information'
        verbose_name_plural = 'Footer Information'

    def __str__(self):
        return 'Footer Information'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
