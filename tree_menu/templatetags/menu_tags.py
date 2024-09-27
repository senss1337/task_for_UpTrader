from django import template
from django.urls import resolve
from django.db.models import Prefetch
from django.core.cache import cache
from django.conf import settings
from tree_menu.models import Menu, MenuItem

register = template.Library()

@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path
    cache_key = f'menu_{menu_name}'
    # menu_data = cache.get(cache_key)
    menu_data = None
    if not menu_data:
        menu = Menu.objects.prefetch_related(
            Prefetch('items', queryset=MenuItem.objects.select_related('parent').order_by('order'))
        ).get(name=menu_name)
        menu_items = menu.items.all()
        menu_tree = build_menu_tree(menu_items)
        menu_data = {
            'menu_tree': menu_tree,
        }
        cache.set(cache_key, menu_data, timeout=settings.MENU_CACHE_TIMEOUT)
    active_items = find_active_items(menu_data['menu_tree'], current_path)
    return {
        'menu_items': menu_data['menu_tree'].values(),
        'active_items': active_items,
    }


def build_menu_tree(menu_items):
    items_dict = {item.id: item for item in menu_items}
    menu_tree = {}
    for item in menu_items:
        item.children_list = []
    for item in menu_items:
        if item.parent_id:
            parent = items_dict[item.parent_id]
            parent.children_list.append(item)
        else:
            menu_tree[item.id] = item
    return menu_tree


def find_active_items(menu_tree, current_path):
    active_items = set()

    def search_active(item_menu):
        if item_menu.get_absolute_url() == current_path:
            active_items.add(item_menu.id)
            parent = item_menu.parent
            while parent:
                active_items.add(parent.id)
                parent = parent.parent
            return True
        for child in item_menu.children_list:
            if search_active(child):
                active_items.add(item_menu.id)
                return True
        return False

    for item in menu_tree.values():
        search_active(item)

    return active_items
