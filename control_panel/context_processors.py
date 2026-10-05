from .panel_registry import PANEL_REGISTRY, GROUP_ORDER


def panel_nav(request):
    """Only computed on admin-panel pages, so it never touches the public site."""
    if not request.path.startswith("/panel/"):
        return {}
    groups = {g: [] for g in GROUP_ORDER}
    for slug, entry in PANEL_REGISTRY.items():
        groups.setdefault(entry["group"], []).append({"slug": slug, "label": entry["label"]})
    return {"panel_nav_groups": groups, "panel_group_order": GROUP_ORDER}