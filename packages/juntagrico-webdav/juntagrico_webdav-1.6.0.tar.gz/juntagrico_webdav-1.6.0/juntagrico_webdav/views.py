import os
import requests
import dateparser
from xml.etree import ElementTree as ET
from urllib.parse import unquote, urlsplit

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from juntagrico_webdav.models import WebdavServer


@login_required
def list(request, id):
    server = get_object_or_404(WebdavServer, pk=id)
    if server.type == WebdavServer.ADMIN_SERVER and not request.user.is_staff:
        return redirect('home')
    url = server.url + '/' + server.path
    username = server.username
    password = server.password
    session = requests.Session()
    session.auth = (username, password)
    session.get(url)
    headers = {'Accept': '*/*', 'Depth': '1'}
    response = session.request('PROPFIND', url, headers=headers)
    files = []
    last_mod_datetime = None
    tree = ET.fromstring(response.content)
    for prop in tree.findall('./{DAV:}response'):
        collection_element = prop.find(".//{DAV:}resourcetype/{DAV:}collection")
        if collection_element is not None:
            # skip folders
            continue
        href = prop.find("./{DAV:}href").text
        href = urlsplit(href).path
        href = os.path.basename(href)
        name = unquote(href)
        last_mod_date = prop.find('.//{DAV:}getlastmodified').text
        last_mod_datetime = dateparser.parse(last_mod_date, languages=['en'])
        if last_mod_datetime is not None:
            last_mod_date = last_mod_datetime.strftime("%d.%m.%Y %H:%M:%S")
        if name != '':
            element = {'url': href,
                       'name': name,
                       'date': last_mod_date,
                       'datetime': last_mod_datetime}
            files.append(element)
    if server.sorted_by_name or last_mod_datetime is None:
        files.sort(key=lambda x: x['name'])
    else:
        files.sort(key=lambda x: x['datetime'])
    if server.sorted_desc:
        files.reverse()
    renderdict = {
        'webdav_server': server,
        'files': files,
        'menu': {'wd': 'active'},
    }
    return render(request, "wd/list.html", renderdict)


@login_required
def get_item(request, id, file):
    server = get_object_or_404(WebdavServer, pk=id)
    if server.type == WebdavServer.ADMIN_SERVER and not request.user.is_staff:
        return redirect('home')
    url = server.url + '/' + server.path + '/' + file
    username = server.username
    password = server.password
    session = requests.Session()
    session.auth = (username, password)
    session.get(url)
    file_response = session.request('GET', url)
    content_type = file_response.headers['Content-Type']
    if file_response.status_code != 200 or 'application/xml' in content_type:
        raise Http404('File not found')
    response = HttpResponse(file_response.content, content_type=content_type)
    return response
