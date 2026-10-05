from django import template

register = template.Library()


@register.filter
def img_url(file_field, fallback):
    """
    Usage: {{ program.featured_image|img_url:'https://.../fallback.jpg' }}
    Returns the file's URL if one is uploaded, otherwise the fallback string.
    Prevents a template crash on an empty ImageField/FileField.
    """
    try:
        if file_field:
            return file_field.url
    except (ValueError, AttributeError):
        pass
    return fallback


@register.filter
def get_item(dictionary, key):
    """
    Usage: {{ some_dict|get_item:some_variable_key }}
    Django templates can't index a dict by a variable name directly.
    """
    if dictionary is None:
        return []
    return dictionary.get(key, [])


@register.filter
def get_field(obj, field_name):
    """
    Usage: {{ obj|get_field:"status" }}
    Dynamic attribute lookup for the admin panel's generic list table.
    Uses get_<field>_display() automatically for choice fields.
    """
    display_method = getattr(obj, f"get_{field_name}_display", None)
    if callable(display_method):
        return display_method()
    return getattr(obj, field_name, "")


from django.utils.safestring import mark_safe

SOCIAL_ICONS = {
    "instagram": '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3V9zm7 0h3.8v1.7h.1c.5-1 1.8-2 3.6-2 3.9 0 4.5 2.6 4.5 5.9V21H18v-5.3c0-1.3 0-3-1.8-3s-2.1 1.4-2.1 2.9V21H10V9z"/></svg>',
    "facebook": '<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M13.5 21v-7h2.4l.4-3H13.5V9.2c0-.9.3-1.5 1.6-1.5h1.4V5c-.7-.1-1.6-.2-2.5-.2-2.5 0-4.3 1.5-4.3 4.3V11H7.8v3h2.9v7h2.8z"/></svg>',
    "youtube": '<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><rect x="2" y="5" width="20" height="14" rx="4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10 9.5v5l5-2.5-5-2.5z"/></svg>',
    "whatsapp": '<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.4-.7-1.6-.8-.2-.1-.4-.1-.6.1-.2.2-.6.8-.8 1-.1.2-.3.2-.5.1-1.3-.6-2.1-1.1-2.9-2.5-.2-.3 0-.5.1-.6.2-.2.4-.4.5-.6.1-.2.1-.4 0-.6-.1-.2-.5-1.2-.7-1.6-.2-.4-.4-.3-.6-.3h-.5c-.2 0-.5.1-.7.4-.2.3-.9 1-.9 2.3 0 1.3 1 2.6 1.1 2.8.1.2 1.9 2.9 4.6 4 2.7 1 2.7.7 3.2.6.5-.1 1.4-.6 1.6-1.1.2-.5.2-1 .1-1.1-.1-.1-.2-.2-.4-.3z"/></svg>',
    "twitter": '<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M4 4l7.3 9.3L4.4 20H7l5.6-5.4L17 20h3l-7.7-9.8L19.4 4H17l-5.2 5-4.4-5H4z"/></svg>',
    "x": '<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M4 4l7.3 9.3L4.4 20H7l5.6-5.4L17 20h3l-7.7-9.8L19.4 4H17l-5.2 5-4.4-5H4z"/></svg>',
    "tiktok": '<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M14 3c.3 2 1.8 3.5 3.8 3.7v2.6c-1.3 0-2.6-.4-3.7-1.1v6.1a5 5 0 1 1-4-4.9v2.7a2.3 2.3 0 1 0 1.6 2.2V3H14z"/></svg>',
}

@register.filter
def social_icon(platform):
    """
    Usage: {{ link.platform|social_icon }}
    Returns a proper SVG icon for known platforms (matched by substring,
    case-insensitive) using currentColor so it inherits whatever color
    the surrounding .socials/.topbar styling already sets — hover states
    keep working with zero extra CSS. Falls back to the platform's first
    two letters for anything not in the set, so an unlisted platform
    never breaks instead of showing nothing.
    """
    key = (platform or "").strip().lower()
    for name, svg in SOCIAL_ICONS.items():
        if name in key:
            return mark_safe(svg)
    return (platform or "?")[:2].upper()