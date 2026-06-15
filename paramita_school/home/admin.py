from django.contrib import admin
from django.utils.html import mark_safe
from .models import (
    SiteSettings, NavMenuItem, BannerSlide, Feature,
    Introduction, AboutSection, PrincipalMessage,
    Testimonial, CTABanner, SocialFeed, FooterInfo,
)

admin.site.site_header  = 'Paramita Heritage School — Admin'
admin.site.site_title   = 'Paramita Admin'
admin.site.index_title  = 'Dashboard'


# ─── SITE SETTINGS ───────────────────────────────────────────────────────────

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    readonly_fields = ['logo_preview']
    fieldsets = [
        ('Logo', {'fields': ['logo', 'logo_preview', 'footer_logo']}),
        ('Other', {'fields': ['parent_login_url', 'tagline']}),
    ]

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


# ─── NAVBAR ──────────────────────────────────────────────────────────────────

class ChildMenuInline(admin.TabularInline):
    model   = NavMenuItem
    fk_name = 'parent'
    extra   = 1
    fields  = ['label', 'url', 'order', 'open_new_tab']


@admin.register(NavMenuItem)
class NavMenuItemAdmin(admin.ModelAdmin):
    list_display  = ['label', 'url', 'parent', 'order']
    list_filter   = ['parent']
    ordering      = ['order']
    inlines       = [ChildMenuInline]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=True)


# ─── BANNER SLIDES ───────────────────────────────────────────────────────────

@admin.register(BannerSlide)
class BannerSlideAdmin(admin.ModelAdmin):
    list_display  = ['image_preview', 'title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_display_links = ['image_preview', 'title']
    readonly_fields    = ['image_preview']
    fieldsets = [
        ('Slide Image', {'fields': ['image', 'image_preview']}),
        ('Content',     {'fields': ['title', 'subtitle']}),
        ('Buttons',     {'fields': [('btn1_text', 'btn1_link'), ('btn2_text', 'btn2_link')]}),
        ('Settings',    {'fields': ['order', 'is_active']}),
    ]


# ─── FEATURES ────────────────────────────────────────────────────────────────

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display  = ['icon_preview', 'title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_display_links = ['icon_preview', 'title']
    readonly_fields    = ['icon_preview']


# ─── INTRODUCTION ────────────────────────────────────────────────────────────

@admin.register(Introduction)
class IntroductionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['section_label', 'heading', 'content', 'image']}),
    ]

    def has_add_permission(self, request):
        return not Introduction.objects.exists()


# ─── ABOUT ───────────────────────────────────────────────────────────────────

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['section_label', 'heading', 'content', 'image', ('btn_text', 'btn_link')]}),
    ]

    def has_add_permission(self, request):
        return not AboutSection.objects.exists()


# ─── PRINCIPAL MESSAGE ───────────────────────────────────────────────────────

@admin.register(PrincipalMessage)
class PrincipalMessageAdmin(admin.ModelAdmin):
    readonly_fields = ['image_style_preview']
    fieldsets = [
        ('Principal Details', {'fields': ['name', 'designation', 'image']}),
        ('Photo Frame Style', {
            'fields': ['image_style', 'image_style_preview'],
            'description': 'Choose how the principal photo is displayed on the homepage.',
        }),
        ('Message',  {'fields': ['salutation', 'message']}),
        ('Button',   {'fields': [('btn_text', 'btn_link')]}),
    ]

    def image_style_preview(self, obj):
        styles = {
            'circle':  ('50%',   'Circle',         '#8B0000'),
            'square':  ('0px',   'Square',         '#1a2035'),
            'rounded': ('20px',  'Rounded Square', '#1a2a0d'),
            'hexagon': ('0px',   'Hexagon',        '#2a1a0d'),
        }
        boxes = []
        for key, (radius, label, color) in styles.items():
            selected = '3px solid #C9A227' if key == obj.image_style else '2px solid #ccc'
            clip = "polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%)" if key == 'hexagon' else 'none'
            boxes.append(
                f'<div style="display:inline-flex;flex-direction:column;align-items:center;gap:6px;margin:8px;">'
                f'<div style="width:64px;height:64px;background:{color};border-radius:{radius};'
                f'clip-path:{clip};border:{selected};"></div>'
                f'<span style="font-size:11px;font-weight:600;color:#333">{label}</span>'
                f'<span style="font-size:10px;color:#888">{"✅ Active" if key == obj.image_style else ""}</span>'
                f'</div>'
            )
        return mark_safe(
            '<div style="display:flex;flex-wrap:wrap;gap:4px;padding:10px 0;">'
            + ''.join(boxes) +
            '</div><p style="color:#666;font-size:12px;margin-top:4px;">'
            '👆 Select a style above then save to apply it.</p>'
        )
    image_style_preview.short_description = 'Style Preview'

    def has_add_permission(self, request):
        return not PrincipalMessage.objects.exists()


# ─── TESTIMONIALS ────────────────────────────────────────────────────────────

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display  = ['name', 'stars_html', 'date', 'is_active']
    list_editable = ['is_active']
    list_filter   = ['rating', 'is_active']
    ordering      = ['-date']


# ─── CTA BANNER ──────────────────────────────────────────────────────────────

@admin.register(CTABanner)
class CTABannerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['heading', 'subheading', 'btn_text', 'btn_link', 'bg_image']}),
    ]

    def has_add_permission(self, request):
        return not CTABanner.objects.exists()


# ─── SOCIAL FEED ─────────────────────────────────────────────────────────────

@admin.register(SocialFeed)
class SocialFeedAdmin(admin.ModelAdmin):
    list_display  = ['image_preview', 'platform', 'caption', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_display_links = ['image_preview', 'caption']
    readonly_fields    = ['image_preview']


# ─── FOOTER ──────────────────────────────────────────────────────────────────

@admin.register(FooterInfo)
class FooterInfoAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Contact',       {'fields': ['address', ('phone1', 'phone2'), 'email']}),
        ('Google Map',    {'fields': ['map_embed_url']}),
        ('Social Links',  {'fields': ['facebook_url', 'instagram_url', 'youtube_url', 'linkedin_url']}),
        ('Copyright',     {'fields': ['copyright_text']}),
    ]

    def has_add_permission(self, request):
        return not FooterInfo.objects.exists()