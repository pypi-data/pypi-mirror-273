from django import template

from juntagrico_webdav.models import WebdavServer

register = template.Library()


@register.simple_tag
def admin_menu():
    return WebdavServer.objects.filter(active=True, type=WebdavServer.ADMIN_SERVER)


@register.simple_tag
def user_menu():
    return WebdavServer.objects.filter(active=True, type=WebdavServer.USER_SERVER)
