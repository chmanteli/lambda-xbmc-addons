# -*- coding: utf-8 -*-

'''
    hellenic toons XBMC Addon
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
favData = xbmc.translatePath(os.path.join(dataPath,'favourites2.cfg'))
viewData = xbmc.translatePath(os.path.join(dataPath,'views.cfg'))
cacheFull = StorageServer.StorageServer(addonname+addonVersion,720).cacheFunction
cache = StorageServer.StorageServer(addonname+addonVersion,240).cacheFunction
description = language(30450).encode("utf-8")
common = CommonFunctions
sysbase = sys.argv[0]
handle = int(sys.argv[1])
paramString = sys.argv[2]
skin = xbmc.getSkinDir()

shows_list = []
episodes_list = []
youtube_url = 'http://gdata.youtube.com'
youtube_search = 'http://gdata.youtube.com/feeds/api/videos?q='
youtube_playlist = 'http://gdata.youtube.com/feeds/api/playlists/'
youtube_user = 'http://gdata.youtube.com/feeds/api/users/'
nickelodeon_url = 'http://www.nickelodeon.gr'

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
    elif action == 'get_nickelodeon_shows':		get_nickelodeon_shows()
    elif action == 'get_youtube_shows':			get_youtube_shows()
    elif action == 'get_youtube_songs':			get_youtube_songs()
    elif action == 'get_episodes':				get_episodes(show,url,image)
    elif action == 'play_video':				play_video(url)

    xbmcplugin.setContent(handle, 'Episodes')
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

def quote_url(url):
    url = urllib.quote_plus(url)
    url = url.replace("%3A", ":")
    url = url.replace("%2F", "/")
    url = url.replace("%3F", "?")
    url = url.replace("%26", "&")
    url = url.replace("%3D", "=")
    url = url.encode('utf-8')
    return url

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
        if (skin == 'skin.confluence'):			xbmc.executebuiltin('Container.SetViewMode(503)')
        if (skin == 'skin.ace'):				xbmc.executebuiltin('Container.SetViewMode(59)')
        if (skin == 'skin.aeon.nox'):			xbmc.executebuiltin('Container.SetViewMode(518)')
        if (skin == 'skin.back-row'):			xbmc.executebuiltin('Container.SetViewMode(529)')
        if (skin == 'skin.carmichael'):			xbmc.executebuiltin('Container.SetViewMode(50)')
        if (skin == 'skin.diffuse'):			xbmc.executebuiltin('Container.SetViewMode(55)')
        if (skin == 'skin.metropolis'):			xbmc.executebuiltin('Container.SetViewMode(55)')
        if (skin == 'skin.pm3-hd'):				xbmc.executebuiltin('Container.SetViewMode(58)')
        if (skin == 'skin.transparency'):		xbmc.executebuiltin('Container.SetViewMode(51)')
        if (skin == 'skin.xeebo'):				xbmc.executebuiltin('Container.SetViewMode(50)')
        if (skin == 'skin.xperience-more'):		xbmc.executebuiltin('Container.SetViewMode(50)')
        if (skin == 'skin.fusion.migma.v3'):	xbmc.executebuiltin('Container.SetViewMode(504)')
        if (skin == 'skin.bello'):				xbmc.executebuiltin('Container.SetViewMode(50)')
        if (skin == 'skin.cirrus.extended.v3'):	xbmc.executebuiltin('Container.SetViewMode(55)')
        if (skin == 'skin.neon'):				xbmc.executebuiltin('Container.SetViewMode(53)')
        if (skin == 'skin.quartz'):				xbmc.executebuiltin('Container.SetViewMode(52)')
        if (skin == 'skin.quartz.reloaded'):	xbmc.executebuiltin('Container.SetViewMode(52)')
        if (skin == 'skin.rapier'):				xbmc.executebuiltin('Container.SetViewMode(68)')
        if (skin == 'skin.re-touched'):			xbmc.executebuiltin('Container.SetViewMode(550)')
        if (skin == 'skin.refocus'):			xbmc.executebuiltin('Container.SetViewMode(50)')
        if (skin == 'skin.simplicity.frodo'):	xbmc.executebuiltin('Container.SetViewMode(50)')
        if (skin == 'skin.touched'):			xbmc.executebuiltin('Container.SetViewMode(50)')
        if (skin == 'skin.xperience1080'):		xbmc.executebuiltin('Container.SetViewMode(50)')

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
        if params["action"] == "get_episodes":
            show = urllib.unquote_plus(params["show"])
            url = urllib.unquote_plus(params["url"])
            image = urllib.unquote_plus(params["image"])
            episodes_list = get_episodes(show,url,image)
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist.unshuffle()
        episodes_list.reverse()
        play_from_here_list = []
        for item in episodes_list:
            play_from_here_list.append({'name': item['name'], 'show': item['show'], 'url': item['url'], 'image': item['image']})
            if deamon == item['url']: break
        play_from_here_list.reverse()
        for item in play_from_here_list:
            add_episodes(0,item['name'],item['show'],item['url'],item['image'],'playlist')
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
    file = open(favData, 'r')
    read = file.read()
    file.close()
    list = re.compile('"(.+?)"[|]"(.+?)"').findall(read)
    total = len(list)
    for name,url in list:
        image = cacheFull(get_episodes,name,url,'','image')
        #image = get_episodes(name,url,'','image')
        if image == [] or image == "" or image is None: image = artPath+'Favourites.png'
        add_favourites(total,name,url,image)
    return

def add_favourites(total,name,url,image):
    sysname = urllib.quote_plus(name)
    sysurl = urllib.quote_plus(url)
    sysimage = urllib.quote_plus(image)
    u = '%s?action=get_episodes&show=%s&url=%s&image=%s' % (sysbase, sysname, sysurl, sysimage)
    cm = []
    cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=play_item)' % (sysbase)))
    cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=random_play_item)' % (sysbase)))
    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=queue_item)' % (sysbase)))
    cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=play_queue)' % (sysbase)))
    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=open_playlist)' % (sysbase)))
    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=xbmc_set_view)' % (sysbase)))
    #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=open_settings)' % (sysbase)))
    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=move_favourite_item_up&name=%s&url=%s)' % (sysbase, sysname, sysurl)))
    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=move_favourite_item_down&name=%s&url=%s)' % (sysbase, sysname, sysurl)))
    cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=delete_favourite_item&name=%s&url=%s)' % (sysbase, sysname, sysurl)))
    item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
    item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "TVShowTitle": name, "Plot": description } )
    item.setProperty("Fanart_Image", fanart)
    item.addContextMenuItems(cm, replaceItems=True)
    xbmcplugin.addDirectoryItem(handle=handle,url=u,listitem=item,totalItems=total,isFolder=True)
    return

def get_categories():
    total = 4
    add_categories(total,language(30501).encode("utf-8"),artPath+'Favourites.png','get_favourites')
    add_categories(total,language(30502).encode("utf-8"),artPath+'Nickelodeon.png','get_nickelodeon_shows')
    add_categories(total,language(30503).encode("utf-8"),artPath+'YouTube.png','get_youtube_shows')
    add_categories(total,language(30504).encode("utf-8"),artPath+'Songs.png','get_youtube_songs')
    return

def add_categories(total,name,image,action):
    u = '%s?action=%s' % (sysbase, action)
    cm = []
    cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=play_queue)' % (sysbase)))
    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=open_playlist)' % (sysbase)))
    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=xbmc_set_view)' % (sysbase)))
    #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=open_settings)' % (sysbase)))
    item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
    item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "TVShowTitle": name, "Plot": description } )
    item.setProperty("Fanart_Image", fanart)
    item.addContextMenuItems(cm, replaceItems=True)
    xbmcplugin.addDirectoryItem(handle=handle,url=u,listitem=item,totalItems=total,isFolder=True)
    return

def get_nickelodeon_shows():
    global shows_list
    shows_list = []

    name = 'Avatar - Season 2'
    url = 'http://www.nickelodeon.gr/seires/item/375.html'
    image = 'http://www.nickelodeon.gr/media/k2/items/cache/b48f2c03bbd159814922841bfb3fe7d7_XL.jpg'
    shows_list.append({'name': name, 'url': url, 'image': image})

    name = 'Avatar - Season 3'
    url = 'http://www.nickelodeon.gr/seires/item/396.html'
    image = 'http://www.nickelodeon.gr/media/k2/items/cache/18bdd04e288fc232234be2fb5ea8bf38_XL.jpg'
    shows_list.append({'name': name, 'url': url, 'image': image})

    name = 'Big Time Rush - Season 2'
    url = 'http://www.nickelodeon.gr/seires/videos/big-time-rush-videos/item/567.html'
    image = 'http://www.nickelodeon.gr/media/k2/items/cache/6e6b736f77dd07b0a373e582bb4b1e3c_XL.jpg'
    shows_list.append({'name': name, 'url': url, 'image': image})

    name = 'Dinofroz - Season 1'
    url = 'http://www.nickelodeon.gr/seires/item/435.html'
    image = 'http://www.nickelodeon.gr/media/k2/items/cache/57df6a0f34180006582f429068c6ac21_XL.jpg'
    shows_list.append({'name': name, 'url': url, 'image': image})

    name = 'iCarly - Season 2'
    url = 'http://www.nickelodeon.gr/seires/item/509.html'
    image = 'http://www.nickelodeon.gr/media/k2/items/cache/cfee1df0aef1bf88281266898fc4ff19_XL.jpg'
    shows_list.append({'name': name, 'url': url, 'image': image})

    name = 'The Legend Of Korra - Season 1'
    url = 'http://www.nickelodeon.gr/seires/item/443.html'
    image = 'http://www.nickelodeon.gr/media/k2/items/cache/9c2fe6cb8c357cf6d57c8926869c1003_XL.jpg'
    shows_list.append({'name': name, 'url': url, 'image': image})

    name = 'Monsuno - Season 1'
    url = 'http://www.nickelodeon.gr/seires/item/349.html'
    image = 'http://www.nickelodeon.gr/media/k2/items/cache/3bd6583af5a14653b7b54db2c9fe7f3e_XL.jpg'
    shows_list.append({'name': name, 'url': url, 'image': image})

    name = 'TMNT - Season 1'
    url = 'http://www.nickelodeon.gr/seires/item/335.html'
    image = 'http://www.nickelodeon.gr/media/k2/items/cache/e9432fccf28a953514f077b86e5e657a_XL.jpg'
    shows_list.append({'name': name, 'url': url, 'image': image})

    total = 0
    for item in shows_list:
        name = item['name']
        url = item['url']
        image = item['image']
        total += 1
        add_shows(total,name,url,image)

    return shows_list

def get_youtube_shows():
    global shows_list
    shows_list = []

    #GreekTvCartoon
    #http://www.youtube.com/user/GreekTvCartoon/videos?view=1
    shows_list = cache(get_youtube_shows_list,'GreekTvCartoon')
    #shows_list = get_youtube_shows_list('GreekTvCartoon')

    #oldMegaCartoons
    #http://www.youtube.com/user/oldMegaCartoons/videos?view=1
    shows_list = cache(get_youtube_shows_list,'oldMegaCartoons')
    #shows_list = get_youtube_shows_list('oldMegaCartoons')

    #GreekTvCartoons
    #http://www.youtube.com/user/GreekTvCartoons/videos?view=1
    shows_list = cache(get_youtube_shows_list,'GreekTvCartoons')
    #shows_list = get_youtube_shows_list('GreekTvCartoons')

    #MrOldcartoon*
    #http://www.youtube.com/user/MrOldcartoon/videos?view=1
    shows_list = cache(get_youtube_shows_list,'MrOldcartoon')
    #shows_list = get_youtube_shows_list('MrOldcartoon')

    #KinoumenaSxedia
    #http://www.youtube.com/user/KinoumenaSxedia/videos?view=1
    shows_list = cache(get_youtube_shows_list,'KinoumenaSxedia')
    #shows_list = get_youtube_shows_list('KinoumenaSxedia')

    #ToonsFromThePast
    #http://www.youtube.com/user/ToonsFromThePast/videos?view=1
    shows_list = cache(get_youtube_shows_list,'ToonsFromThePast')
    #shows_list = get_youtube_shows_list('ToonsFromThePast')

    #SuperGreekCartoon
    #http://www.youtube.com/user/SuperGreekCartoon/videos?view=1
    shows_list = cache(get_youtube_shows_list,'SuperGreekCartoon')
    #shows_list = get_youtube_shows_list('SuperGreekCartoon')

    #SuperGreekCartoon2
    #http://www.youtube.com/user/supergreekcartoon2/videos?view=1
    shows_list = cache(get_youtube_shows_list,'supergreekcartoon2')
    #shows_list = get_youtube_shows_list('supergreekcartoon2')

    #Greek Disney Corner
    #http://www.youtube.com/user/Michaletosjr/videos?view=1
    shows_list = cache(get_youtube_shows_list,'Michaletosjr')
    #shows_list = get_youtube_shows_list('Michaletosjr')

    #GreekCartoonClassics
    #http://www.youtube.com/user/GreekCartoonClassics/videos?view=1
    shows_list = cache(get_youtube_shows_list,'GreekCartoonClassics')
    #shows_list = get_youtube_shows_list('GreekCartoonClassics')

    #CartoonGR
    #http://www.youtube.com/user/CartoonGR/videos?view=1
    shows_list = cache(get_youtube_shows_list,'CartoonGR')
    #shows_list = get_youtube_shows_list('CartoonGR')

    #GPITRAL5
    #http://www.youtube.com/user/GPITRAL5/videos?view=1
    shows_list = cache(get_youtube_shows_list,'GPITRAL5')
    #shows_list = get_youtube_shows_list('GPITRAL5')

    #trianta99*
    #http://www.youtube.com/user/trianta99/videos?view=1
    shows_list = cache(get_youtube_shows_list,'trianta99')
    #shows_list = get_youtube_shows_list('trianta99')

    #lilithvii**
    #http://www.youtube.com/user/lilithvii/videos?view=1
    shows_list = cache(get_youtube_shows_list,'lilithvii')
    #shows_list = get_youtube_shows_list('lilithvii')

    #stswandersoul**
    #http://www.youtube.com/user/stswandersoul/videos?view=1
    shows_list = cache(get_youtube_shows_list,'stswandersoul')
    #shows_list = get_youtube_shows_list('stswandersoul')

    #acrobat106
    name = 'Mickey Mouse Clubhouse'.encode("utf-8")#Mickey Mouse Clubhouse
    url = youtube_search + 'MICKEY MOUSE CLUBHOUSE&author=acrobat106'
    image = 'http://i.ytimg.com/vi/mayex_QrnQo/0.jpg'
    channel = 'acrobat106'
    shows_list.append({'name': name, 'url': url, 'image': image, 'channel': channel})

    total = 0
    shows_list = sorted(shows_list, key=itemgetter('name'))

    for item in shows_list:
        name = item['name']
        url = item['url']
        image = item['image']
        channel = item['channel']

        #MrOldcartoon fix
        if url.endswith("PLB4A43356634E7F15"): continue #PROMO VIDEOS
        if url.endswith("PL22A077ED4B2360C1"): continue #jjjjjjjjjjjj

        #trianta99 fix
        if url.endswith("FLYxtDTeDWEduVbOQztWfaBg"): continue #Αγαπημένα βίντεο

        #lilithvii fix
        if channel == "lilithvii" and not (
        url.endswith("PL3420AA02720B05E5") or #Ulysses 31 - Οδύσσεια του Διαστήματος
        url.endswith("PL147140D5904AFBE4") or #Κάντυ Κάντυ (1976) 1-40
        url.endswith("PLF191388E07E9E127") or #Κάντυ Κάντυ (1976) 41-80
        url.endswith("PL8F5C47492E11C109") or #Κάντυ Κάντυ (1976) 81-115
        url.endswith("PLAD759EE008F12C43") or #Φρουτοπία (1985) - 1ος Κύκλος
        url.endswith("PLC3C3861A770162F5") or #Φρουτοπία (1985) - 2ος Κύκλος
        url.endswith("PL0C994DFD3BCDAEDB") or #Φρουτοπία - 3ος Κύκλος
        url.endswith("PLE3470893493CF5A8") or #Lazer Tag Academy (Τα Αστροπίστολα) - 1986
        url.endswith("PLD2C2707D06DA58DC") or #Του κουτιού τα παραμύθια (1987)
        url.endswith("PL724AA3356D663CED") or #Karate Kat (1987) - Greek
        url.endswith("PLC34BCF01941BAC02") #Happy Tree Friends
        ): continue

        #stswandersoul fix
        if channel == "stswandersoul" and not (
        url.endswith("SP1FDC7DF9E8F8ED46") #igano kabamaru greek episodes (greek audio)
        ): continue

        total += 1
        add_shows(total,name,url,image)

    return shows_list

def get_youtube_songs():
    global shows_list
    shows_list = []

    #Κανάλι ... λέμε τώρα*
    #http://www.youtube.com/user/sapiensgr2/videos?view=1
    shows_list = cache(get_youtube_shows_list,'sapiensgr2')
    #shows_list = get_youtube_shows_list('sapiensgr2')

    #Η ΧΑΡΑ ΤΟΥ ΠΑΙΔΙΟΥ**
    #http://www.youtube.com/user/Aviosys/videos?view=1
    shows_list = cache(get_youtube_shows_list,'Aviosys')
    #shows_list = get_youtube_shows_list('Aviosys')

    #SuperKidschannel**
    #http://www.youtube.com/user/SuperKidscorner/videos?view=1
    shows_list = cache(get_youtube_shows_list,'SuperKidscorner')
    #shows_list = get_youtube_shows_list('SuperKidscorner')

    total = 0
    shows_list = sorted(shows_list, key=itemgetter('name'))

    for item in shows_list:
        name = item['name']
        url = item['url']
        image = item['image']
        channel = item['channel']

        #sapiensgr2 fix
        if url.endswith("PLB3126415BC8BCDE3"): continue #ΑΓΑΠΗΜΕΝΑ

        #Aviosys fix
        if channel == "Aviosys" and not url.endswith("PL9E9CD72ED3715FEA"): continue #ΠΑΙΔΙΚΑ - ΤΑ ΖΟΥΖΟΥΝΙΑ
        if channel == "Aviosys" and url.endswith("PL9E9CD72ED3715FEA"):
            name = u'\u0396'u'\u039F'u'\u03A5'u'\u0396'u'\u039F'u'\u03A5'u'\u039D'u'\u0399'u'\u0391'.encode("utf-8")#ΖΟΥΖΟΥΝΙΑ

        #SuperKidscorner fix
        if channel == "SuperKidscorner" and not (
        url.endswith("PL06ECA50FF627CBA7") #Mazoo and the Zoo - Μαζού Ζου
        ): continue

        total += 1
        add_shows(total,name,url,image)

    return shows_list

def get_youtube_shows_list(channel):
    try:
        shows = ""
        for i in range(1, 10000, 25):
            shows_url = '%s%s/playlists?max-results=25&start-index=%s' % (youtube_user, channel, str(i))
            result = common.fetchPage({"link": shows_url})
            shows += result["content"]
            next = 'start-index=%s' % str(i+25)
            if not next in result["content"]: break
        shows = common.parseDOM(shows, "entry")
        total = len(shows)
    except:
        return
    for show in shows:
        try:
            name = common.parseDOM(show, "title")[0]
            name = common.replaceHTMLCodes(name)
            name = name.encode('utf-8')
            image = common.parseDOM(show, "media:thumbnail", ret="url")[0]
            image = image.replace(image.split("/")[-1], '0.jpg')
            image = image.encode('utf-8')
            url = common.parseDOM(show, "id")[0]
            url = youtube_playlist + url.split("/")[-1]
            url = url.encode('utf-8')
            if image.endswith("/00000000000/0.jpg"): continue #empty playlist
            shows_list.append({'name': name, 'url': url, 'image': image, 'channel': channel})
        except:
            total = total - 1
            pass

    return shows_list

def add_shows(total,name,url,image):
    sysname = urllib.quote_plus(name)
    sysurl = urllib.quote_plus(url)
    sysimage = urllib.quote_plus(image)
    u = '%s?action=get_episodes&show=%s&url=%s&image=%s' % (sysbase, sysname, sysurl, sysimage)
    file = open(favData, 'r')
    read = file.read()
    file.close()
    cm = []
    cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=play_item)' % (sysbase)))
    cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=random_play_item)' % (sysbase)))
    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=queue_item)' % (sysbase)))
    cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=play_queue)' % (sysbase)))
    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=open_playlist)' % (sysbase)))
    if not url in read:
        cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=add_favourite_item&name=%s&url=%s)' % (sysbase, sysname, sysurl)))
    else:
        cm.append((language(30414).encode("utf-8"), 'RunPlugin(%s?action=delete_favourite_item&name=%s&url=%s)' % (sysbase, sysname, sysurl)))
    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=xbmc_set_view)' % (sysbase)))
    #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=open_settings)' % (sysbase)))
    item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
    item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "TVShowTitle": name, "Plot": description } )
    item.setProperty("Fanart_Image", fanart)
    item.addContextMenuItems(cm, replaceItems=True)
    xbmcplugin.addDirectoryItem(handle=handle,url=u,listitem=item,totalItems=total,isFolder=True)
    return

def get_episodes(show,url,image,mode=None):
    global episodes_list
    episodes_list = []

    if url.startswith(nickelodeon_url):
        if mode is None:
            episodes_list = get_nickelodeon_episodes(show,url)
        else:
            image = get_nickelodeon_episodes(show,url,mode)
            return image

    if url.startswith(youtube_url):
        if mode is None:
            episodes_list = get_youtube_episodes(show,url)
        else:
            image = get_youtube_episodes(show,url,mode)
            return image

    return episodes_list

def get_nickelodeon_episodes(show,url,mode=None):
    try:
        result = common.fetchPage({"link": url})
        episodes = result["content"]
    except:
        return
    try:
        episodes = common.parseDOM(episodes, "div", attrs = { "class": "row itemVideosList" })[0]
        episodes = common.parseDOM(episodes, "div", attrs = { "class": "w25" })
        total = len(episodes)
    except:
        pass
    for episode in episodes:
        try:
            name = common.parseDOM(episode, "a", ret="title")[0]
            name = common.replaceHTMLCodes(name)
            name = name.encode('utf-8')
            url = common.parseDOM(episode, "a", ret="href")[0]
            url = '%s%s' % (nickelodeon_url, url)
            url = url.encode('utf-8')
            image = common.parseDOM(episode, "img", ret="src")[0]
            image = image.encode('utf-8')
            if mode == 'image': return image
            episodes_list.append({'name': name, 'show': show, 'url': url, 'image': image})
            add_episodes(total,name,show,url,image)
        except:
            total = total - 1
            pass

    return episodes_list

def get_youtube_episodes(show,url,mode=None):
    try:
        episodes = ""
        if not "?" in url: url += "?"
        if url.startswith(youtube_playlist):
            for i in range(1, 10000, 25):
                episodes_url = '%s&max-results=25&start-index=%s' % (url, str(i))
                result = common.fetchPage({"link": episodes_url})
                episodes += result["content"]
                next = 'start-index=%s' % str(i+25)
                if not next in result["content"]: break
            episodes = common.parseDOM(episodes, "entry")
            total = len(episodes)

        if url.startswith(youtube_user):
            for i in range(1, 100, 25):
                episodes_url = '%s&max-results=25&start-index=%s' % (url, str(i))
                result = common.fetchPage({"link": episodes_url})
                episodes += result["content"]
            episodes = common.parseDOM(episodes, "entry")
            total = len(episodes)

        if url.startswith(youtube_search):
            params = url.split("?")[-1]
            params = dict(arg.split("=") for arg in params.split("&"))
            query = params["q"]
            query2 = urllib.quote_plus(query).encode('utf-8').replace('%','').replace('+','')
            url = url.replace(query, urllib.quote_plus(query))
            for i in range(1, 10000, 25):
                episodes_url = '%s&max-results=25&start-index=%s' % (url, str(i))
                result = common.fetchPage({"link": episodes_url})
                episodes += result["content"]
                try:
                    match = common.parseDOM(result["content"], "entry")[-1]
                    match = common.parseDOM(match, "title")[0]
                    match = urllib.quote_plus(match.encode('utf-8')).replace('%','').replace('+','')
                    if not query2 in match: break
                except:
                    break
            filter_list = common.parseDOM(episodes, "entry")
            episodes = []
            for filter in filter_list:
                match = common.parseDOM(filter, "title")[0]
                match = urllib.quote_plus(match.encode('utf-8')).replace('%','').replace('+','')
                if query2 in match:
                    episodes.append(filter)
            total = len(episodes)
    except:
        return

    for episode in episodes:
        try:
            name = common.parseDOM(episode, "title")[0]
            name = common.replaceHTMLCodes(name)
            name = name.encode('utf-8')
            image = common.parseDOM(episode, "media:thumbnail", ret="url")[0]
            image = image.replace(image.split("/")[-1], '0.jpg')
            image = image.encode('utf-8')
            if mode == 'image': return image
            url = common.parseDOM(episode, "media:player", ret="url")[0]
            url = re.compile('v=(.+?)&amp').findall(url)[0]
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
            url = url.encode('utf-8')
            episodes_list.append({'name': name, 'show': show, 'url': url, 'image': image})
            add_episodes(total,name,show,url,image)
        except:
            total = total - 1
            pass

    return episodes_list

def add_episodes(total,name,show,url,image,mode=None):
    sysurl = urllib.quote_plus(url)
    u = '%s?action=play_video&url=%s' % (sysbase, sysurl)
    cm = []
    cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=queue_item)' % (sysbase)))
    cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=play_from_here_item&url=%s)' % (sysbase, sysurl)))
    cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=play_queue)' % (sysbase)))
    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=open_playlist)' % (sysbase)))
    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=xbmc_set_view)' % (sysbase)))
    #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=open_settings)' % (sysbase)))
    item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
    item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "TVShowTitle": show, "Plot": description } )
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

def play_video(url):
    try:
        if url.startswith('plugin://plugin.video.youtube/'):
            if check_addon('plugin.video.youtube') is None:
                xbmcgui.Dialog().ok(addonname, language(30351).encode("utf-8"), language(30352).encode("utf-8"))
            else:
                item = xbmcgui.ListItem(path=url)
                xbmcplugin.setResolvedUrl(handle, True, item)
            return

        if url.startswith(nickelodeon_url):
            url = quote_url(url)
            result = common.fetchPage({"link": url})
            url = common.parseDOM(result["content"], "span", attrs = { "class": "itemVideo" })[0]
            url = re.compile("url: '(.+?manifest.f4m)'").findall(url)[-1]
            url = url.replace("/z/", "/i/").replace("manifest.f4m","master.m3u8")
            item = xbmcgui.ListItem(path=url)
            xbmcplugin.setResolvedUrl(handle, True, item)
            return
    except:
        return

main()