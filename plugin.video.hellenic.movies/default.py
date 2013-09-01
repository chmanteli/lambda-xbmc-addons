# -*- coding: utf-8 -*-

'''
    hellenic movies XBMC Addon
    Copyright (C) 2013 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib,urllib2,re,os,xbmc,xbmcplugin,xbmcgui,xbmcaddon
from operator import itemgetter
try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
try:
    import CommonFunctions
except:
    import commonfunctionsdummy as CommonFunctions


language = xbmcaddon.Addon().getLocalizedString
setSetting = xbmcaddon.Addon().setSetting
getSetting = xbmcaddon.Addon().getSetting
addonname = xbmcaddon.Addon().getAddonInfo("name")
addonVersion = xbmcaddon.Addon().getAddonInfo("version")
addonId = xbmcaddon.Addon().getAddonInfo("id")
addonPath = xbmcaddon.Addon().getAddonInfo('path')
addonIcon = xbmc.translatePath(os.path.join(addonPath,'icon.png'))
artPath = xbmc.translatePath(os.path.join(addonPath,'resources/art/'))
fanart = xbmc.translatePath(os.path.join(addonPath,'fanart.jpg'))
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
favData = xbmc.translatePath(os.path.join(dataPath,'favourites.cfg'))
viewData = xbmc.translatePath(os.path.join(dataPath,'views.cfg'))
cacheFull = StorageServer.StorageServer(addonname+addonVersion,720).cacheFunction
cache = StorageServer.StorageServer(addonname+addonVersion,720).cacheFunction
description = language(30450).encode("utf-8")
common = CommonFunctions
sysbase = sys.argv[0]
handle = int(sys.argv[1])
paramString = sys.argv[2]
skin = xbmc.getSkinDir()

movies_list = []
cinegreece_url = 'http://www.cinegreece.com'
greek_movies_url = 'http://greek-movies.com'

def main():
    xbmc_data()
    params = {}
    splitparams = paramString[paramString.find('?') + 1:].split('&')
    for param in splitparams:
        if (len(param) > 0):
            splitparam = param.split('=')
            key = splitparam[0]
            try: 
                value = splitparam[1].encode("utf-8")
            except:
                value = splitparam[1]
            params[key] = value

    try:		action = urllib.unquote_plus(params["action"])
    except:		action = None
    try:		name = urllib.unquote_plus(params["name"])
    except:		name = None
    try:		show = urllib.unquote_plus(params["show"])
    except:		show = None
    try:		url = urllib.unquote_plus(params["url"])
    except:		url = None
    try:		image = urllib.unquote_plus(params["image"])
    except:		image = None
    try:		mode = urllib.unquote_plus(params["mode"])
    except:		mode = None

    if action == None:							get_categories()
    elif action == 'play_item':					play_item()
    elif action == 'random_play_item':			random_play_item()
    elif action == 'queue_item':				queue_item()
    elif action == 'play_from_here_item':		play_from_here_item(url)
    elif action == 'add_favourite_item':		add_favourite_item(name,url)
    elif action == 'delete_favourite_item':		delete_favourite_item(name,url)
    elif action == 'move_favourite_item_up':	move_favourite_item_up(name,url)
    elif action == 'move_favourite_item_down':	move_favourite_item_down(name,url)
    elif action == 'play_queue':				play_queue()
    elif action == 'open_playlist':				open_playlist()
    elif action == 'xbmc_set_view':				xbmc_set_view()
    elif action == 'open_settings':				open_settings()
    elif action == 'get_favourites':			get_favourites()
    elif action == 'get_live_movies':			get_live_movies()
    elif action == 'get_cinegreece_menus':		get_cinegreece_menus()
    elif action == 'get_greek_movies_menus':	get_greek_movies_menus()
    elif action == 'get_recent_movies':			get_recent_movies()
    elif action == 'search_movies':				search_movies()
    elif action == 'get_movies':				get_movies(url)
    elif action == 'play_video':				play_video(url)

    xbmcplugin.setContent(handle, 'Movies')
    xbmcplugin.setPluginFanart(handle, fanart)
    xbmcplugin.endOfDirectory(handle)
    xbmc_view()
    return

def unique_list(list):
    unique_set = set()
    unique_list = []
    for n in list:
        if n not in unique_set:
            unique_set.add(n)
            unique_list.append(n)
    return unique_list

def get_url(url,fetch=True,mobile=False,proxy=None,referer=None,cookie=None):
    if not proxy is None:
        proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
        opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
        opener = urllib2.install_opener(opener)
    request = urllib2.Request(url,None)
    if not cookie is None:
        from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
        import cookielib
        cj = cookielib.CookieJar()
        opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())
        cookiereq = Request(cookie)
        response = opener.open(cookiereq)
        response.close()
        for cookie in cj:
            cookie = '%s=%s' % (cookie.name, cookie.value)
        request.add_header('Cookie', cookie)
    if mobile == True:
        request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
    else:
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0')
    if not referer is None:
        request.add_header('Referer', referer)
    response = urllib2.urlopen(request)
    if fetch == True:
        result = response.read()
    else:
        result = response.geturl()
    response.close()
    return result

def check_addon(id):
    check_addon = xbmcaddon.Addon(id=id).getAddonInfo("name")
    if not check_addon == addonname: return check_addon
    return

def xbmc_notify(mode):
    if mode == 'setview':
        viewName = xbmc.getInfoLabel('Container.Viewmode')
        xbmc.executebuiltin("Notification(%s,%s, 3000)" % (addonname, '%s%s%s') % (language(30301).encode("utf-8"), viewName, language(30302).encode("utf-8")))
    elif mode == 'favadd':
        xbmc.executebuiltin("Notification(%s,%s, 3000)" % (addonname, language(30303).encode("utf-8")))
    elif mode == 'favrem':
        xbmc.executebuiltin("Notification(%s,%s, 3000)" % (addonname, language(30304).encode("utf-8")))
    elif mode == 'favup':
        xbmc.executebuiltin("Notification(%s,%s, 3000)" % (addonname, language(30305).encode("utf-8")))
    elif mode == 'favdown':
        xbmc.executebuiltin("Notification(%s,%s, 3000)" % (addonname, language(30306).encode("utf-8")))

def xbmc_refresh():
    xbmc.executebuiltin('Container.Refresh')

def xbmc_data():
    if not os.path.exists(dataPath):
        os.makedirs(dataPath)
    if not os.path.isfile(favData):
        file = open(favData, 'w')
        file.write('')
        file.close()
    if not os.path.isfile(viewData):
        file = open(viewData, 'w')
        file.write('')
        file.close()

def xbmc_view():
    try:
        file = open(viewData,'r')
        read = file.read().replace('\n','')
        file.close()
        view = re.compile('"%s"[|]"(.+?)"' % (skin)).findall(read)[0]
        xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view))
    except:
        if (skin == 'skin.confluence'):			xbmc.executebuiltin('Container.SetViewMode(500)')
        if (skin == 'skin.ace'):				xbmc.executebuiltin('Container.SetViewMode(62)')
        if (skin == 'skin.aeon.nox'):			xbmc.executebuiltin('Container.SetViewMode(512)')
        if (skin == 'skin.back-row'):			xbmc.executebuiltin('Container.SetViewMode(505)')
        if (skin == 'skin.carmichael'):			xbmc.executebuiltin('Container.SetViewMode(52)')
        if (skin == 'skin.diffuse'):			xbmc.executebuiltin('Container.SetViewMode(55)')
        if (skin == 'skin.metropolis'):			xbmc.executebuiltin('Container.SetViewMode(54)')
        if (skin == 'skin.pm3-hd'):				xbmc.executebuiltin('Container.SetViewMode(53)')
        if (skin == 'skin.transparency'):		xbmc.executebuiltin('Container.SetViewMode(53)')
        if (skin == 'skin.xeebo'):				xbmc.executebuiltin('Container.SetViewMode(52)')
        if (skin == 'skin.xperience-more'):		xbmc.executebuiltin('Container.SetViewMode(55)')
        if (skin == 'skin.fusion.migma.v3'):	xbmc.executebuiltin('Container.SetViewMode(517)')
        if (skin == 'skin.bello'):				xbmc.executebuiltin('Container.SetViewMode(50)')
        if (skin == 'skin.cirrus.extended.v3'):	xbmc.executebuiltin('Container.SetViewMode(55)')
        if (skin == 'skin.neon'):				xbmc.executebuiltin('Container.SetViewMode(503)')
        if (skin == 'skin.quartz'):				xbmc.executebuiltin('Container.SetViewMode(52)')
        if (skin == 'skin.quartz.reloaded'):	xbmc.executebuiltin('Container.SetViewMode(53)')
        if (skin == 'skin.rapier'):				xbmc.executebuiltin('Container.SetViewMode(54)')
        if (skin == 'skin.re-touched'):			xbmc.executebuiltin('Container.SetViewMode(500)')
        if (skin == 'skin.refocus'):			xbmc.executebuiltin('Container.SetViewMode(57)')
        if (skin == 'skin.simplicity.frodo'):	xbmc.executebuiltin('Container.SetViewMode(556)')
        if (skin == 'skin.touched'):			xbmc.executebuiltin('Container.SetViewMode(500)')
        if (skin == 'skin.xperience1080'):		xbmc.executebuiltin('Container.SetViewMode(500)')

def xbmc_set_view():
    try:
        skinInfo = xbmc.translatePath('special://xbmc/addons/%s/addon.xml' % (skin))
        videoNav = 'special://xbmc/addons/%s/%s/MyVideoNav.xml'
        if not os.path.isfile(skinInfo):
            skinInfo = xbmc.translatePath('special://home/addons/%s/addon.xml' % (skin))
            videoNav = 'special://home/addons/%s/%s/MyVideoNav.xml'
        file = open(skinInfo,'r')
        read = file.read().replace('\n','')
        file.close()
        try:
            skinInfo = re.compile('defaultresolution="(.+?)"').findall(read)[0]
        except:
            skinInfo = re.compile('<res.+?folder="(.+?)"').findall(read)[0]
        videoNav = xbmc.translatePath(videoNav % (skin, skinInfo))
        file = open(videoNav,'r')
        read = file.read().replace('\n','')
        file.close()
        views = re.compile('<views>(.+?)</views>').findall(read)[0]
        views = [int(x) for x in views.split(',')]
        for view in views:
            viewLabel = xbmc.getInfoLabel('Control.GetLabel(%s)' % (view))
            if not (viewLabel == '' or viewLabel is None): break
        file = open(viewData, 'r')
        read = file.read()
        file.close()
        file = open(viewData, 'w')
        for line in re.compile('(".+?\n)').findall(read):
            if not line.startswith('"%s"|"' % (skin)): file.write(line)
        file.write('"%s"|"%s"\n' % (skin, str(view)))
        file.close()
        xbmc_notify('setview')
    except:
        return

def play_item():
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    xbmc.executebuiltin('Action(Queue)')
    playlist.unshuffle()
    xbmc.Player().play(playlist)

def random_play_item():
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    xbmc.executebuiltin('Action(Queue)')
    playlist.shuffle()
    xbmc.Player().play(playlist)

def queue_item():
    xbmc.executebuiltin('Action(Queue)')

def play_from_here_item(url):
    try:
        deamon = url
        folderPath = xbmc.getInfoLabel('Container.FolderPath')
        params = folderPath.split("?")[-1]
        params = dict(arg.split("=") for arg in params.split("&"))
        if params["action"] == "get_favourites": movies_list = get_favourites()
        if params["action"] == "get_recent_movies": movies_list = get_recent_movies()
        if params["action"] == "get_live_movies": movies_list = get_live_movies()
        if params["action"] == "get_movies": movies_list = get_movies(urllib.unquote_plus(params["url"]))
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist.unshuffle()
        movies_list.reverse()
        play_from_here_list = []
        for item in movies_list:
            play_from_here_list.append({'name': item['name'], 'url': item['url'], 'image': item['image']})
            if deamon == item['url']: break
        play_from_here_list.reverse()
        for item in play_from_here_list:
            add_movies(0,item['name'],item['url'],item['image'],'playlist')
        xbmc.Player().play(playlist)
    except:
        return

def add_favourite_item(name,url):
    xbmc_refresh()
    file = open(favData, 'a+')
    file.write('"%s"|"%s"\n' % (name, url))
    file.close()
    xbmc_notify('favadd')

def delete_favourite_item(name,url):
    xbmc_refresh()
    file = open(favData, 'r')
    read = file.read().replace('"%s"|"%s"' % (name, url),'')
    file.close()
    file = open(favData, 'w')
    for line in re.compile('(".+?\n)').findall(read):
        file.write(line)
    file.close()
    xbmc_notify('favrem')

def move_favourite_item_up(name,url):
    xbmc_refresh()
    file = open(favData,'r')
    read = file.read()
    file.close()
    favourites_list = []
    for line in re.compile('(".+?)\n').findall(read):
        favourites_list.append(line)
    i = favourites_list.index('"%s"|"%s"' % (name, url))
    if i == 0: return
    favourites_list[i],favourites_list[i-1] = favourites_list[i-1],favourites_list[i]
    file = open(favData, 'w')
    for line in favourites_list:
        file.write('%s\n' % (line))
    file.close()
    xbmc_notify('favup')

def move_favourite_item_down(name,url):
    xbmc_refresh()
    file = open(favData,'r')
    read = file.read()
    file.close()
    favourites_list = []
    for line in re.compile('(".+?)\n').findall(read):
        favourites_list.append(line)
    i = favourites_list.index('"%s"|"%s"' % (name, url))
    if i+1 == len(favourites_list): return
    favourites_list[i],favourites_list[i+1] = favourites_list[i+1],favourites_list[i]
    file = open(favData, 'w')
    for line in favourites_list:
        file.write('%s\n' % (line))
    file.close()
    xbmc_notify('favdown')

def play_queue():
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.unshuffle()
    xbmc.Player().play(playlist)

def open_playlist():
    xbmc.executebuiltin('ActivateWindow(VideoPlaylist)')

def open_settings():
    xbmc.executebuiltin('Addon.OpenSettings(%s)' % (addonId))

def get_favourites():
    global movies_list
    movies_list = []

    file = open(favData, 'r')
    read = file.read()
    file.close()
    list = re.compile('"(.+?)"[|]"(.+?)"').findall(read)
    total = len(list)
    for name,url in list:
        image = cacheFull(get_movies_image,url)
        #image = get_movies_image(url)
        if image == [] or image == "" or image is None: image = artPath+'poster.jpg'
        movies_list.append({'name': name, 'url': url, 'image': image})
        add_favourites(total,name,url,image)

    return movies_list

def add_favourites(total,name,url,image):
    sysname = urllib.quote_plus(name)
    sysurl = urllib.quote_plus(url)
    u = '%s?action=play_video&url=%s' % (sysbase, sysurl)
    cm = []
    cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=queue_item)' % (sysbase)))
    cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=play_from_here_item&url=%s)' % (sysbase, sysurl)))
    cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=play_queue)' % (sysbase)))
    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=open_playlist)' % (sysbase)))
    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=xbmc_set_view)' % (sysbase)))
    #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=open_settings)' % (sysbase)))
    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=move_favourite_item_up&name=%s&url=%s)' % (sysbase, sysname, sysurl)))
    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=move_favourite_item_down&name=%s&url=%s)' % (sysbase, sysname, sysurl)))
    cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=delete_favourite_item&name=%s&url=%s)' % (sysbase, sysname, sysurl)))
    year = ""
    try:	year = re.compile('[[](\d*)[]]').findall(name)[0]
    except:	pass
    try:	year = re.compile('[(](\d*)[)]').findall(name)[0]
    except:	pass
    title = name.replace(year, "").replace(" ()", "").replace(" []", "")
    if url.startswith(cinegreece_url): plot = language(30451).encode("utf-8")
    elif url.startswith(greek_movies_url): plot = language(30452).encode("utf-8")
    else: plot = description
    item = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=image)
    item.setInfo( type="Video", infoLabels={ "Label": title, "Title": title, "Year": year, "Genre": "Greek", "Plot": plot } )
    item.setProperty("IsPlayable", "true")
    item.setProperty( "Video", "true" )
    item.setProperty("Fanart_Image", fanart)
    item.addContextMenuItems(cm, replaceItems=True)
    xbmcplugin.addDirectoryItem(handle=handle,url=u,listitem=item,totalItems=total)
    return

def get_categories():
    total = 6
    add_categories(total,language(30501).encode("utf-8"),artPath+'Favourites.png','get_favourites')
    add_categories(total,language(30502).encode("utf-8"),artPath+'Live.png','get_live_movies')
    add_categories(total,language(30503).encode("utf-8"),artPath+'Cine-Greece.png','get_cinegreece_menus')
    add_categories(total,language(30504).encode("utf-8"),artPath+'Greek-Movies.png','get_greek_movies_menus')
    add_categories(total,language(30505).encode("utf-8"),artPath+'Recent.png','get_recent_movies')
    add_categories(total,language(30506).encode("utf-8"),artPath+'Search.png','search_movies')
    return

def add_categories(total,name,image,action):
    u = '%s?action=%s' % (sysbase, action)
    cm = []
    if action == 'get_favourites' or action == 'get_recent_movies':
        cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=play_item)' % (sysbase)))
        cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=random_play_item)' % (sysbase)))
        cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=queue_item)' % (sysbase)))
    cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=play_queue)' % (sysbase)))
    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=open_playlist)' % (sysbase)))
    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=xbmc_set_view)' % (sysbase)))
    #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=open_settings)' % (sysbase)))
    item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
    item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": description } )
    item.setProperty("Fanart_Image", fanart)
    item.addContextMenuItems(cm, replaceItems=True)
    xbmcplugin.addDirectoryItem(handle=handle,url=u,listitem=item,totalItems=total,isFolder=True)
    return

def get_cinegreece_menus():
    try:
        menus_url = "http://www.cinegreece.com/p/blog-page.html"
        result = common.fetchPage({"link": menus_url})
        menus = common.parseDOM(result["content"], "select", attrs = { "name": "menu1" })[0]
        menus = re.compile('(<option.+?</option>)').findall(menus)
        menus = [x for x in menus if not "/p/blog-page.html" in x]
        total = len(menus)
    except:
        return
    for menu in menus:
        try:
            name = common.parseDOM(menu, "option")[0]
            name = common.replaceHTMLCodes(name)
            name = name.encode('utf-8')
            url = common.parseDOM(menu, "option", ret="value")[0]
            url = common.replaceHTMLCodes(url)
            url = url.replace(url.split("/")[2], cinegreece_url.split("//")[-1])
            url = url.encode('utf-8')
            image = artPath+'Folder.png'
            add_menus(total,name,url,image)
        except:
            total = total - 1
            pass
    return

def get_greek_movies_menus():
    try:
        menus_url = "http://greek-movies.com/movies.php"
        result = common.fetchPage({"link": menus_url})
        menus = common.parseDOM(result["content"], "select", attrs = { "onChange": ".+?" })[0]
        menus = re.compile('(<option.+?</option>)').findall(menus)
        menus = [x for x in menus if not "?y=&g=&p=" in x]
        total = len(menus)
    except:
        return
    for menu in menus:
        try:
            name = common.parseDOM(menu, "p")[0]
            name = common.replaceHTMLCodes(name)
            name = name.encode('utf-8')
            url = common.parseDOM(menu, "option", ret="value")[0]
            url = common.replaceHTMLCodes(url)
            url = '%s/%s' % (greek_movies_url, url)
            url = url.replace('&y=&g=&p=', '')
            url = url.encode('utf-8')
            image = artPath+'Folder.png'
            add_menus(total,name,url,image)
        except:
            total = total - 1
            pass
    return

def add_menus(total,name,url,image):
    sysurl = urllib.quote_plus(url)
    u = '%s?action=get_movies&url=%s' % (sysbase, sysurl)
    cm = []
    cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=play_item)' % (sysbase)))
    cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=random_play_item)' % (sysbase)))
    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=queue_item)' % (sysbase)))
    cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=play_queue)' % (sysbase)))
    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=open_playlist)' % (sysbase)))
    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=xbmc_set_view)' % (sysbase)))
    #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=open_settings)' % (sysbase)))
    item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
    item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": description } )
    item.setProperty("Fanart_Image", fanart)
    item.addContextMenuItems(cm, replaceItems=True)
    xbmcplugin.addDirectoryItem(handle=handle,url=u,listitem=item,totalItems=total,isFolder=True)
    return

def get_movies(url):
    global movies_list
    movies_list = []

    if url.startswith(cinegreece_url):
        movies_list = get_cinegreece_movies(url)
    if url.startswith(greek_movies_url):
        movies_list = get_greek_movies_movies(url)

    total = 0
    movies_list = sorted(movies_list, key=itemgetter('name'))

    for item in movies_list:
        name = item['name']
        url = item['url']
        image = item['image']
        total += 1
        add_movies(total,name,url,image)

    return movies_list

def get_cinegreece_movies(url):
    try:
        result = common.fetchPage({"link": url})
        movies = common.parseDOM(result["content"], "div", attrs = { "itemprop": "articleBody" })[0]
        movies = re.compile('(<a.+?</a>)').findall(movies)
        movies = unique_list(movies)
        total = len(movies)
    except:
        return
    for movie in movies:
        try:
            name = common.parseDOM(movie, "img", ret="title")[0]
            name = common.replaceHTMLCodes(name)
            name = name.encode('utf-8')
            url = common.parseDOM(movie, "a", ret="href")[0]
            url = common.replaceHTMLCodes(url)
            url = url.replace(url.split("/")[2], cinegreece_url.split("//")[-1])
            url = url.encode('utf-8')
            image = common.parseDOM(movie, "img", ret="src")[0]
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
            movies_list.append({'name': name, 'url': url, 'image': image})
        except:
            total = total - 1
            pass

    return movies_list

def get_greek_movies_movies(url):
    try:
        movies = ""
        for i in range(1, 9):
            movies_url = '%s&y=%s' % (url, str(i))
            result = common.fetchPage({"link": movies_url})
            movies += common.parseDOM(result["content"], "DIV", attrs = { "class": "maincontent" })[0]
        movies = common.parseDOM(movies, "td", attrs = { "width": ".+?" })
        movies = unique_list(movies)
        total = len(movies)
    except:
        return
    for movie in movies:
        try:
            name = common.parseDOM(movie, "p")[0]
            name = common.replaceHTMLCodes(name)
            name = name.encode('utf-8')
            url = common.parseDOM(movie, "a", ret="href")[0]
            url = common.replaceHTMLCodes(url)
            url = '%s/%s' % (greek_movies_url, url)
            url = url.encode('utf-8')
            image = common.parseDOM(movie, "IMG", ret="SRC")[0]
            image = common.replaceHTMLCodes(image)
            image = '%s/%s' % (greek_movies_url, image)
            if image.endswith('icon/film.jpg'): image = artPath+'poster.jpg'
            image = image.encode('utf-8')
            movies_list.append({'name': name, 'url': url, 'image': image})
        except:
            total = total - 1
            pass

    return movies_list

def get_live_movies():
    global movies_list
    movies_list = []
    total = 2

    name = 'Hellenic Movies 1'
    url = 'live_1'
    image = artPath+'poster.jpg'
    movies_list.append({'name': name, 'url': url, 'image': image})
    add_movies(total,name,url,image)

    name = 'Hellenic Movies 2'
    url = 'live_2'
    image = artPath+'poster.jpg'
    movies_list.append({'name': name, 'url': url, 'image': image})
    add_movies(total,name,url,image)

    return movies_list

def get_recent_movies():
    global movies_list
    movies_list = []

    try:
        movies_url = "http://www.cinegreece.com/search/label/%CE%95%CE%BB%CE%BB%CE%B7%CE%BD%CE%B9%CE%BA%CE%AD%CF%82%20%CE%A4%CE%B1%CE%B9%CE%BD%CE%AF%CE%B5%CF%82"
        result = common.fetchPage({"link": movies_url})
        movies = common.parseDOM(result["content"], "div", attrs = { "class": "post-outer" })
        movies = unique_list(movies)
        total = len(movies)
    except:
        return
    for movie in movies:
        try:
            name = common.parseDOM(movie, "h3")[0]
            name = common.parseDOM(name, "a")[0]
            name = common.replaceHTMLCodes(name)
            name = name.encode('utf-8')
            url = common.parseDOM(movie, "h3")[0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = common.replaceHTMLCodes(url)
            url = url.replace(url.split("/")[2], cinegreece_url.split("//")[-1])
            url = url.encode('utf-8')
            image = common.parseDOM(movie, "div", attrs = { "class": "separator" })[0]
            image = common.parseDOM(image, "img", ret="src")[0]
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
            movies_list.append({'name': name, 'url': url, 'image': image})
            add_movies(total,name,url,image)
        except:
            total = total - 1
            pass

    return movies_list

def search_movies():
    keyboard = xbmc.Keyboard()
    keyboard.setHeading(language(30506).encode("utf-8"))
    keyboard.doModal()
    if keyboard.isConfirmed() == False:
        get_categories()
        return
    query = keyboard.getText()
    query = urllib.quote_plus(query)

    global movies_list
    movies_list = []
    total = 0

    try:
        movies_url = 'https://encrypted.google.com/search?as_q=%s&as_sitesearch=cinegreece.com' % (query)
        result = common.fetchPage({"link": movies_url})
        movies = re.compile('cinegreece.com/(.+?/.+?[.]html)').findall(result["content"])
        movies = unique_list(movies)
        total = total + len(movies)
        for movie in movies:  
            try:
                url = common.replaceHTMLCodes(movie)
                url = '%s/%s' % (cinegreece_url, url)
                url = url.encode('utf-8')
                name = get_movies_name(url)
                if name is None:
                    total = total - 1
                    continue
                image = get_movies_image(url)
                movies_list.append({'name': name, 'url': url, 'image': image})
                add_movies(total,name,url,image)
            except:
                total = total - 1
                pass
    except:
        pass

    try:
        movies_url = 'https://encrypted.google.com/search?as_q=%s&as_sitesearch=greek-movies.com' % (query)
        result = common.fetchPage({"link": movies_url})
        movies = re.compile('greek-movies.com/(movies.php[?]m=\d*)').findall(result["content"])
        movies = unique_list(movies)
        total = total + len(movies)
        for movie in movies:
            try:
                url = common.replaceHTMLCodes(movie)
                url = '%s/%s' % (greek_movies_url, url)
                url = url.encode('utf-8')
                name = get_movies_name(url)
                image = get_movies_image(url)
                movies_list.append({'name': name, 'url': url, 'image': image})
                add_movies(total,name,url,image)
            except:
                total = total - 1
                pass
    except:
        pass

    return movies_list

def add_movies(total,name,url,image,mode=None):
    sysname = urllib.quote_plus(name)
    sysurl = urllib.quote_plus(url)
    u = '%s?action=play_video&url=%s' % (sysbase, sysurl)
    file = open(favData, 'r')
    read = file.read()
    file.close()
    cm = []
    cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=queue_item)' % (sysbase)))
    cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=play_from_here_item&url=%s)' % (sysbase, sysurl)))
    cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=play_queue)' % (sysbase)))
    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=open_playlist)' % (sysbase)))
    if not url in read:
        cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=add_favourite_item&name=%s&url=%s)' % (sysbase, sysname, sysurl)))
    else:
        cm.append((language(30414).encode("utf-8"), 'RunPlugin(%s?action=delete_favourite_item&name=%s&url=%s)' % (sysbase, sysname, sysurl)))
    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=xbmc_set_view)' % (sysbase)))
    #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=open_settings)' % (sysbase)))
    year = ""
    try:	year = re.compile('[[](\d*)[]]').findall(name)[0]
    except:	pass
    try:	year = re.compile('[(](\d*)[)]').findall(name)[0]
    except:	pass
    title = name.replace(year, "").replace(" ()", "").replace(" []", "")
    if url.startswith(cinegreece_url): plot = language(30451).encode("utf-8")
    elif url.startswith(greek_movies_url): plot = language(30452).encode("utf-8")
    else: plot = description
    item = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=image)
    item.setInfo( type="Video", infoLabels={ "Label": title, "Title": title, "Year": year, "Genre": "Greek", "Plot": plot } )
    item.setProperty("IsPlayable", "true")
    item.setProperty( "Video", "true" )
    item.setProperty("Fanart_Image", fanart)
    if mode == 'playlist':
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.add(u, item)
    else:
        item.addContextMenuItems(cm, replaceItems=True)
        xbmcplugin.addDirectoryItem(handle=handle,url=u,listitem=item,totalItems=total)
    return

def get_movies_name(url):
    if url.startswith(cinegreece_url):
        try:
            result = common.fetchPage({"link": url})
            name = common.parseDOM(result["content"], "div", attrs = { "class": "post-outer" })[0]
            name = common.parseDOM(result["content"], "h3")[0]
            name = common.replaceHTMLCodes(name)
            name = name.encode('utf-8')
            if "/%CE%95%CE%BB%CE%BB%CE%B7%CE%BD%CE%B9%CE%BA%CE%AD%CF%82%20%CE%A4%CE%B1%CE%B9%CE%BD%CE%AF%CE%B5%CF%82" in result["content"]:
                return name
        except:
            return

    if url.startswith(greek_movies_url):
        try:
            result = common.fetchPage({"link": url})
            name = common.parseDOM(result["content"], "DIV", attrs = { "class": "maincontent" })[0]
            title = common.parseDOM(name, "p")[0]
            year = common.parseDOM(name, "p", attrs = { "class": "movieheading3" })[0].split(" ")[-1]
            name = '%s [%s]' % (title, year)
            name = common.replaceHTMLCodes(name)
            name = name.encode('utf-8')
            return name
        except:
            return

def get_movies_image(url):
    if url.startswith(cinegreece_url):
        try:
            result = common.fetchPage({"link": url})
            image = common.parseDOM(result["content"], "div", attrs = { "class": "separator" })[0]
            image = common.parseDOM(image, "img", ret="src")[0]
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
            return image
        except:
            pass

    if url.startswith(greek_movies_url):
        try:
            result = common.fetchPage({"link": url})
            image = common.parseDOM(result["content"], "DIV", attrs = { "class": "maincontent" })[0]
            image = common.parseDOM(image, "img", ret="src")[0]
            image = common.replaceHTMLCodes(image)
            image = '%s/%s' % (greek_movies_url, image)
            if image.endswith('icon/film.jpg'): image = artPath+'poster.jpg'
            image = image.encode('utf-8')
            return image
        except:
            pass

    image = artPath+'poster.jpg'
    return image

def play_video(url):
    if url == 'live_1':
        try:
            url = get_url('http://kanalia.eu/player/player.php?channel=105',referer='http://www.kanalia.eu/')
            streamer = re.compile('streamer:.+?"(.+?)"').findall(url)[0]
            playpath = re.compile('file:.+?"(.+?)"').findall(url)[0]
            url = '%s playpath=%s pageUrl=http://www.kanalia.eu/ live=1 timeout=10' % (streamer, playpath)
        except:
            url = 'rtmp://46.21.146.45:80/cinema/ playpath=cinema.sdp pageUrl=http://www.kanalia.eu/ live=1 timeout=10'
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(handle, True, item)

    if url == 'live_2':
        try:
            streams = []
            try: import json
            except: import simplejson as json
            url = 'http://www.justin.tv/zuganelis'
            name = url.split("/")[-1]
            swf_url = 'http://www.justin.tv/widgets/live_embed_player.swf?channel=%s' % name
            swf_url = get_url(swf_url,fetch=False,referer=url)
            data = 'http://usher.justin.tv/find/%s.json?type=any&group=&channel_subscription=' % name
            data = get_url(data,referer='http://www.justin.tv/')
            data = json.loads(data)
            for i in data:
                token = None
                token = ' jtv='+i['token'].replace('\\','\\5c').replace(' ','\\20').replace('"','\\22')
                if i['needed_info'] == 'private': token = 'private'
                rtmp = i['connect']+'/'+i['play']
                try:
                    if i['type'] == "live": stream_url = rtmp+token
                    else: streams.append((i['type'], rtmp, token))
                except:
                    continue
            if len(streams) < 1: pass
            elif len(streams) == 1: stream_url = streams[0][1]+streams[0][2]
            else:
                for i in range(len(s_type)):
                    quality = s_type[str(i)]
                    for q in streams:
                        if q[0] == quality: stream_url = (q[1]+q[2])
                        else: continue
            url = '%s swfUrl=%s pageUrl=%s swfVfy=1 live=1 timeout=10' % (stream_url, swf_url, url)
            item = xbmcgui.ListItem(path=url)
            xbmcplugin.setResolvedUrl(handle, True, item)
        except:
            return

    if url.startswith(cinegreece_url):
        try:
            result = common.fetchPage({"link": url})
            url = common.parseDOM(result["content"], "div", attrs = { "itemprop": "articleBody" })[0]
            url = common.parseDOM(url, "a", ret="onclick")[0]
            url = re.compile("'(.+?)'").findall(url)[0]
            url = url.split("&amp;")[0].split("/")[-1].split("=")[-1]
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
            if check_addon('plugin.video.youtube') is None:
                xbmcgui.Dialog().ok(addonname, language(30351).encode("utf-8"), language(30352).encode("utf-8"))
            else:
                item = xbmcgui.ListItem(path=url)
                xbmcplugin.setResolvedUrl(handle, True, item)
                return url
        except:
            return

    if url.startswith(greek_movies_url):
        try:
            x_list = []
            result = common.fetchPage({"link": url})
            sources = common.parseDOM(result["content"], "DIV", attrs = { "class": "maincontent" })[0]
            sources = common.parseDOM(sources, "tr",)[-1]
            sources = common.parseDOM(sources, "p")
            sources = unique_list(sources)
            for source in sources:
                source = common.parseDOM(source, "a", ret="href")[0]
                source = '%s/%s' % (greek_movies_url, source)
                result = common.fetchPage({"link": source})
                source = common.parseDOM(result["content"], "button", ret="OnClick")[0]
                source = source.split("'")[1]
                x_list.append(source)
            page_list = []
            page_list += [x for x in x_list if "http://www.youtube.com" in x]
            page_list += [x for x in x_list if "http://www.putlocker.com" in x]
            page_list += [x for x in x_list if "http://www.datemule.com" in x]
            page_list += [x for x in x_list if "http://www.dailymotion.com" in x]
            page_list += [x for x in x_list if "http://www.veoh.com" in x]
            page_list += [x for x in x_list if "http://vimeo.com" in x]
        except:
            return

        for pageUrl in page_list:
            try:
                if pageUrl.startswith('http://www.youtube.com'):
                    result = common.fetchPage({"link": pageUrl})
                    try:
                        error = common.parseDOM(result[u"content"], "h1", attrs = { "id": "unavailable-message" })[0]
                    except:
                        error = None
                    try:
                        alert = common.parseDOM(result[u"content"], "div", attrs = { "id": "watch7-notification-area" })[0]
                    except:
                        alert = None
                    if result["status"] == 200 and error is None and alert is None:
                        url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % pageUrl.split("=")[-1]
                        if check_addon('plugin.video.youtube') is None:
                            xbmcgui.Dialog().ok(addonname, language(30351).encode("utf-8"), language(30352).encode("utf-8"))
                        else:
                            item = xbmcgui.ListItem(path=url)
                            xbmcplugin.setResolvedUrl(handle, True, item)
                        return url
            except:
                pass

            try:
                if pageUrl.startswith('http://www.putlocker.com'):
                    result = common.fetchPage({"link": pageUrl})
                    hash = re.compile('value="(.+?)".+?name="hash"').findall(result[u"content"])[0]
                    post_data = {'hash': hash, 'confirm': 'Continue as Free User'}
                    result = common.fetchPage({"link": pageUrl, "post_data": post_data})
                    url = re.compile('href="(.+?)".+?class="download_file_link"').findall(result[u"content"])[0]
                    url = "http://putlocker.com%s" % url
                    item = xbmcgui.ListItem(path=url)
                    xbmcplugin.setResolvedUrl(handle, True, item)
                    return url
            except:
                pass

            try:
                if pageUrl.startswith('http://www.datemule.com'):
                    result = common.fetchPage({"link": pageUrl})
                    url = common.parseDOM(result[u"content"], "A", ret="onclick")[0]
                    url = re.compile("'(.+?)'").findall(url)[0]
                    url = url.split("title=")[0]
                    result = common.fetchPage({"link": url})
                    url = re.compile('href="(.+?)"').findall(result[u"content"])[0]
                    item = xbmcgui.ListItem(path=url)
                    xbmcplugin.setResolvedUrl(handle, True, item)
                    return url
            except:
                pass

            try:
                if pageUrl.startswith('http://www.dailymotion.com'):
                    result = common.fetchPage({"link": pageUrl})
                    sequence = re.compile('"sequence":"(.+?)"').findall(result[u"content"])[0]
                    sequence = urllib.unquote_plus(sequence).replace('\/', '/')
                    try:
                        url = re.compile('"hqURL":"(.+?)"').findall(sequence)[0]
                    except:
                        url = re.compile('"sdURL":"(.+?)"').findall(sequence)[0]
                    item = xbmcgui.ListItem(path=url)
                    xbmcplugin.setResolvedUrl(handle, True, item)
                    return url
            except:
                pass

            try:
                if pageUrl.startswith('http://www.veoh.com') or pageUrl.startswith('http://vimeo.com'):
                    flashUrl = 'http://www.flashvideodownloader.org/download.php?u=%s' % pageUrl
                    result = common.fetchPage({"link": flashUrl})
                    url = common.parseDOM(result[u"content"], "div", attrs = { "class": "mod_download" })[0]
                    url = common.parseDOM(url, "a", ret="href")[0]
                    item = xbmcgui.ListItem(path=url)
                    xbmcplugin.setResolvedUrl(handle, True, item)
                    return url
            except:
                pass

        url = None
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(handle, True, item)
        return url

main()