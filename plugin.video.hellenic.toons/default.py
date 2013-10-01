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

import urllib,urllib2,re,os,threading,xbmc,xbmcplugin,xbmcgui,xbmcaddon
from operator import itemgetter
try:	import CommonFunctions
except:	import commonfunctionsdummy as CommonFunctions
try:	import StorageServer
except:	import storageserverdummy as StorageServer


language			= xbmcaddon.Addon().getLocalizedString
setSetting			= xbmcaddon.Addon().setSetting
getSetting			= xbmcaddon.Addon().getSetting
addonName			= xbmcaddon.Addon().getAddonInfo("name")
addonVersion		= xbmcaddon.Addon().getAddonInfo("version")
addonId				= xbmcaddon.Addon().getAddonInfo("id")
addonPath			= xbmcaddon.Addon().getAddonInfo("path")
addonDesc			= language(30450).encode("utf-8")
addonIcon			= os.path.join(addonPath,'icon.png')
addonFanart			= os.path.join(addonPath,'fanart.jpg')
addonArt			= os.path.join(addonPath,'resources/art')
addonVarious		= os.path.join(addonPath,'resources/xml/various.xml')
addonNickelodeon	= os.path.join(addonPath,'resources/xml/nickelodeon.xml')
addonClassics		= os.path.join(addonPath,'resources/xml/classics.xml')
addonSongs			= os.path.join(addonPath,'resources/xml/songs.xml')
dataPath			= xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData			= os.path.join(dataPath,'views.cfg')
favData				= os.path.join(dataPath,'favourites3.cfg')
cache				= StorageServer.StorageServer(addonName+addonVersion,24).cacheFunction
cache2				= StorageServer.StorageServer(addonName+addonVersion,240).cacheFunction
common				= CommonFunctions


class main:
    def __init__(self):
        index().container_data()
        params = {}
        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
        for param in splitparams:
            if (len(param) > 0):
                splitparam = param.split('=')
                key = splitparam[0]
                try:	value = splitparam[1].encode("utf-8")
                except:	value = splitparam[1]
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

        if action == None:							categories().get()
        elif action == 'item_play':					contextMenu().item_play()
        elif action == 'item_random_play':			contextMenu().item_random_play()
        elif action == 'item_queue':				contextMenu().item_queue()
        elif action == 'item_play_from_here':		contextMenu().item_play_from_here(url)
        elif action == 'favourite_add':				contextMenu().favourite_add(name, url, image)
        elif action == 'favourite_delete':			contextMenu().favourite_delete(name, url, image)
        elif action == 'favourite_moveUp':			contextMenu().favourite_moveUp(name, url, image)
        elif action == 'favourite_moveDown':		contextMenu().favourite_moveDown(name, url, image)
        elif action == 'playlist_start':			contextMenu().playlist_start()
        elif action == 'playlist_open':				contextMenu().playlist_open()
        elif action == 'settings_open':				contextMenu().settings_open()
        elif action == 'global_view':				contextMenu().global_view()
        elif action == 'favourites':				favourites().get()
        elif action == 'various_shows':				shows().various()
        elif action == 'nickelodeon_shows':			shows().nickelodeon()
        elif action == 'classics_shows':			shows().classics()
        elif action == 'songs_shows':				shows().songs()
        elif action == 'episodes':					episodes().get(show, url)
        elif action == 'play':						player().run(url)

        viewDict = {
            'skin.confluence'	: 503,	'skin.aeon.nox'		: 518,	'skin.back-row'			: 529,
            'skin.bello'		: 50,	'skin.carmichael'	: 50,	'skin.diffuse'			: 55,
            'skin.droid'		: 50,	'skin.metropolis'	: 55,	'skin.pm3-hd'			: 58,
            'skin.rapier'		: 68,	'skin.re-touched'	: 550,	'skin.simplicity'		: 50,
            'skin.transparency'	: 51,	'skin.xeebo'		: 50,	'skin.xperience1080'	: 50
            }

        xbmcplugin.setContent(int(sys.argv[1]), 'Episodes')
        xbmcplugin.setPluginFanart(int(sys.argv[1]), addonFanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        index().container_view(viewDict)
        return

class getUrl(object):
    def __init__(self, url, fetch=True, mobile=False, proxy=None, post=None, referer=None, cookie=None):
        if not proxy is None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if not post is None:
            request = urllib2.Request(url, post)
        else:
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
        response = urllib2.urlopen(request, timeout=10)
        if fetch == True:
            result = response.read()
        else:
            result = response.geturl()
        response.close()
        self.result = result

class cryptUrl:
    def __init__(self):
        self.key = 'dhflqoxm'

    def encode(self, str):
        enc = []
        import base64
        for i in range(len(str)):
            key_c = self.key[i % len(self.key)]
            enc_c = chr((ord(str[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc))

    def decode(self, str):
        dec = []
        import base64
        str = base64.urlsafe_b64decode(str)
        for i in range(len(str)):
            key_c = self.key[i % len(self.key)]
            dec_c = chr((256 + ord(str[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)

class uniqueList(object):
    def __init__(self, list):
        uniqueSet = set()
        uniqueList = []
        for n in list:
            if n not in uniqueSet:
                uniqueSet.add(n)
                uniqueList.append(n)
        self.list = uniqueList

class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

class index:
    def infoDialog(self, str, header=addonName):
        xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % (header, str, addonIcon))

    def okDialog(self, str1, str2, header=addonName):
        xbmcgui.Dialog().ok(header, str1, str2)

    def selectDialog(self, list, header=addonName):
        select = xbmcgui.Dialog().select(header, list)
        return select

    def yesnoDialog(self, str1, str2, header=addonName):
        answer = xbmcgui.Dialog().yesno(header, str1, str2)
        return answer

    def getProperty(self, str):
        property = xbmcgui.Window(10000).getProperty(str)
        return property

    def setProperty(self, str1, str2):
        xbmcgui.Window(10000).setProperty(str1, str2)

    def clearProperty(self, str):
        xbmcgui.Window(10000).clearProperty(str)

    def addon_status(self, id):
        check = xbmcaddon.Addon(id=id).getAddonInfo("name")
        if not check == addonName: return True

    def container_refresh(self):
        xbmc.executebuiltin("Container.Refresh")

    def container_data(self):
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

    def container_view(self, viewDict):
        try:
            skin = xbmc.getSkinDir()
            file = open(viewData,'r')
            read = file.read().replace('\n','')
            file.close()
            view = re.compile('"%s"[|]"(.+?)"' % (skin)).findall(read)[0]
            xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view))
        except:
            try:
                id = str(viewDict[skin])
                xbmc.executebuiltin('Container.SetViewMode(%s)' % id)
            except:
                pass

    def favList(self, favList):
        total = len(favList)
        for i in favList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)
                u = '%s?action=episodes&show=%s&url=%s' % (sys.argv[0], sysname, sysurl)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "TVShowTitle": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def catList(self, catList):
        total = len(catList)
        for i in catList:
            try:
                name = language(i['name']).encode("utf-8")
                image = '%s/%s' % (addonArt, i['image'])
                action = i['action']
                u = '%s?action=%s' % (sys.argv[0], action)

                cm = []
                if action.startswith('episodes'):
                    cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                    cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "TVShowTitle": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def showList(self, showList):
        file = open(favData,'r')
        favRead = file.read()
        file.close()

        total = len(showList)
        for i in showList:
            try:
                try: name, url, image, fanart = i['name'], i['url'], i['image'], i['fanart']
                except: name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)
                u = '%s?action=episodes&show=%s&url=%s' % (sys.argv[0], sysname, sysurl)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                if not url in favRead:
                    cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                else:
                    cm.append((language(30414).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "TVShowTitle": name, "Plot": addonDesc } )
                try: item.setProperty("Fanart_Image", fanart)
                except: item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def episodeList(self, episodeList):
        total = len(episodeList)
        for i in episodeList:
            try:
                try: name, show, url, image, fanart = i['name'], i['show'], i['url'], i['image'], i['fanart']
                except: name, show, url, image = i['name'], i['show'], i['url'], i['image']
                sysurl = urllib.quote_plus(url)
                u = '%s?action=play&url=%s' % (sys.argv[0], sysurl)

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_play_from_here&url=%s)' % (sys.argv[0], sysurl)))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "TVShowTitle": show, "Plot": addonDesc } )
                item.setProperty("IsPlayable", "true")
                item.setProperty( "Video", "true" )
                try: item.setProperty("Fanart_Image", fanart)
                except: item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

class contextMenu:
    def item_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.unshuffle()
        xbmc.Player().play(playlist)

    def item_random_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.shuffle()
        xbmc.Player().play(playlist)

    def item_queue(self):
        xbmc.executebuiltin('Action(Queue)')

    def item_play_from_here(self, url):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist.unshuffle()
        total = xbmc.getInfoLabel('Container.NumItems')
        for i in range(0, int(total)):
            name = xbmc.getInfoLabel('ListItemNoWrap(%s).Label' % str(i))
            if name == '': break
            show = xbmc.getInfoLabel('ListItemNoWrap(%s).TVShowTitle' % str(i))
            image = xbmc.getInfoLabel('ListItemNoWrap(%s).Icon' % str(i))
            url = xbmc.getInfoLabel('ListItemNoWrap(%s).FileNameAndPath' % str(i))
            url = url.split('?url=')[-1].split('&url=')[-1]
            sysurl = urllib.quote_plus(url)
            u = '%s?action=play&url=%s' % (sys.argv[0], sysurl)
            item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
            item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "TVShowTitle": show, "Plot": addonDesc } )
            item.setProperty("IsPlayable", "true")
            item.setProperty( "Video", "true" )
            item.setProperty("Fanart_Image", addonFanart)
            playlist.add(u, item)
        xbmc.Player().play(playlist)

    def playlist_start(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.unshuffle()
        xbmc.Player().play(playlist)

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(VideoPlaylist)')

    def settings_open(self):
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % (addonId))

    def global_view(self):
        try:
            skin = xbmc.getSkinDir()
            try:
                xml = xbmc.translatePath('special://xbmc/addons/%s/addon.xml' % (skin))
                file = open(xml,'r')
            except:
                xml = xbmc.translatePath('special://home/addons/%s/addon.xml' % (skin))
                file = open(xml,'r')
            read = file.read().replace('\n','')
            file.close()
            src = os.path.dirname(xml) + '/'
            try:
                src += re.compile('defaultresolution="(.+?)"').findall(read)[0] + '/'
            except:
                src += re.compile('<res.+?folder="(.+?)"').findall(read)[0] + '/'
            src += 'MyVideoNav.xml'
            file = open(src,'r')
            read = file.read().replace('\n','')
            file.close()
            views = re.compile('<views>(.+?)</views>').findall(read)[0]
            views = [int(x) for x in views.split(',')]
            for view in views:
                label = xbmc.getInfoLabel('Control.GetLabel(%s)' % (view))
                if not (label == '' or label is None): break
            file = open(viewData, 'r')
            read = file.read()
            file.close()
            file = open(viewData, 'w')
            for line in re.compile('(".+?\n)').findall(read):
                if not line.startswith('"%s"|"' % (skin)): file.write(line)
            file.write('"%s"|"%s"\n' % (skin, str(view)))
            file.close()
            viewName = xbmc.getInfoLabel('Container.Viewmode')
            index().infoDialog('%s%s%s' % (language(30301).encode("utf-8"), viewName, language(30302).encode("utf-8")))
        except:
            return

    def favourite_add(self, name, url, image):
        try:
            index().container_refresh()
            file = open(favData, 'a+')
            file.write('"%s"|"%s"|"%s"\n' % (name, url, image))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_delete(self, name, url, image):
        try:
            index().container_refresh()
            file = open(favData,'r')
            read = file.read()
            file.close()
            read = read.replace('"%s"|"%s"|"%s"' % (name, url, image),'')
            file = open(favData, 'w')
            for line in re.compile('(".+?\n)').findall(read):
                file.write(line)
            file.close()
            index().infoDialog(language(30304).encode("utf-8"), name)
        except:
            return

    def favourite_moveUp(self, name, url, image):
        try:
            index().container_refresh()
            list = []
            file = open(favData,'r')
            read = file.read()
            file.close()
            for line in re.compile('(".+?)\n').findall(read):
                list.append(line)
            i = list.index('"%s"|"%s"|"%s"' % (name, url, image))
            if i == 0 : return
            list[i], list[i-1] = list[i-1], list[i]
            file = open(favData, 'w')
            for line in list:
                file.write('%s\n' % (line))
            file.close()
            index().infoDialog(language(30305).encode("utf-8"), name)
        except:
            return

    def favourite_moveDown(self, name, url, image):
        try:
            index().container_refresh()
            list = []
            file = open(favData,'r')
            read = file.read()
            file.close()
            for line in re.compile('(".+?)\n').findall(read):
                list.append(line)
            i = list.index('"%s"|"%s"|"%s"' % (name, url, image))
            if i+1 == len(list): return
            list[i], list[i+1] = list[i+1], list[i]
            file = open(favData, 'w')
            for line in list:
                file.write('%s\n' % (line))
            file.close()
            index().infoDialog(language(30306).encode("utf-8"), name)
        except:
            return

class favourites:
    def get(self):
        favList = []
        file = open(favData, 'r')
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, url, image in match:
            favList.append({'name': name, 'url': url, 'image': image})
        index().favList(favList)

class categories:
    def get(self):
        catList = []
        catList.append({'name': 30501, 'image': 'Favourites.png', 'action': 'favourites'})
        catList.append({'name': 30502, 'image': 'Various.png', 'action': 'various_shows'})
        catList.append({'name': 30503, 'image': 'Nickelodeon.png', 'action': 'nickelodeon_shows'})
        catList.append({'name': 30504, 'image': 'Classics.png', 'action': 'classics_shows'})
        catList.append({'name': 30505, 'image': 'Songs.png', 'action': 'songs_shows'})
        index().catList(catList)

class shows:
    def __init__(self):
        self.list = []
        self.data = ''
        self.youtubeUrl				= 'http://gdata.youtube.com'
        self.youtube_showsUrl		= 'http://gdata.youtube.com/feeds/api/users/%s/playlists'
        self.youtube_episodeUrl		= 'http://gdata.youtube.com/feeds/api/playlists/%s'
        self.youtube_recentUrl		= 'http://gdata.youtube.com/feeds/api/users/%s/uploads'
        self.youtube_searchUrl		= 'http://gdata.youtube.com/feeds/api/videos?q='

    def various(self):
        self.list = self.various_list()
        self.list = sorted(self.list, key=itemgetter('name'))
        index().showList(self.list)

    def nickelodeon(self):
        self.list = self.nickelodeon_list()
        self.list = sorted(self.list, key=itemgetter('name'))
        index().showList(self.list)

    def classics(self):
        #self.list = self.youtube_list3(addonClassics)
        self.list = cache(self.youtube_list3, addonClassics)
        self.list = sorted(self.list, key=itemgetter('name'))
        index().showList(self.list)

    def songs(self):
        #self.list = self.youtube_list3(addonSongs)
        self.list = cache(self.youtube_list3, addonSongs)
        self.list = sorted(self.list, key=itemgetter('name'))
        index().showList(self.list)

    def various_list(self):
        try:
            file = open(addonVarious,'r')
            result = file.read()
            file.close()
            shows = common.parseDOM(result, "show")
        except:
            return
        for show in shows:
            try:
                name = common.parseDOM(show, "name")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                image = common.parseDOM(show, "image")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': 'various', 'image': image, 'fanart': image})
            except:
                pass

        return self.list

    def nickelodeon_list(self):
        try:
            file = open(addonNickelodeon,'r')
            result = file.read()
            file.close()
            shows = common.parseDOM(result, "show")
        except:
            return
        for show in shows:
            try:
                name = common.parseDOM(show, "name")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(show, "url")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(show, "image")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'fanart': image})
            except:
                pass

        return self.list

    def youtube_list(self, channel):
        try:
            threads = []
            for i in range(1, 250, 25):
                showsUrl = self.youtube_showsUrl % channel + '?max-results=25&start-index=%s' % str(i)
                threads.append(Thread(self.youtube_list2, showsUrl))
            [i.start() for i in threads]
            [i.join() for i in threads]
            result = self.data
            shows = common.parseDOM(result, "entry")
        except:
            return
        for show in shows:
            try:
                name = common.parseDOM(show, "title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(show, "id")[0]
                url = self.youtube_episodeUrl % url.split("/")[-1]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(show, "media:thumbnail", ret="url")[0]
                image = image.replace(image.split("/")[-1], '0.jpg')
                image = image.encode('utf-8')
                if image.endswith("/00000000000/0.jpg"): continue #empty playlist
                self.list.append({'name': name, 'channel': channel, 'url': url, 'image': image})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('name'))
        return self.list

    def youtube_list2(self, url):
        try:
            result = getUrl(url).result
            self.data += result
        except:
            return

    def youtube_list3(self, xmlFile):
        try:
            file = open(xmlFile,'r')
            result = file.read()
            file.close()
            shows = common.parseDOM(result, "channel")
        except:
            return

        for show in shows:
            try:
                url = common.parseDOM(show, "url")[0]
                channel = url.split("/")[-1]
                self.youtube_list(channel)
            except:
                pass

        list = []
        import itertools,operator
        self.list.sort(key=operator.itemgetter('url'))
        for k, i in itertools.groupby(self.list, operator.itemgetter('url')): list.append(i.next())
        self.list[:] = list

        for show in shows:
            try:
                url = common.parseDOM(show, "url")[0]
                channel = url.split("/")[-1]
                includes = common.parseDOM(show, "include")
                if includes == []: raise Exception()
                for i in range(0, len(includes)):
                    includes[i] = self.youtube_episodeUrl % includes[i].split("list=")[-1]
                x = [i for i in self.list if not i['channel'] == channel]
                x += [i for i in self.list if i['channel'] == channel and i['url'] in includes]
                self.list = x
            except:
                pass

        for show in shows:
            try:
                excludes = common.parseDOM(show, "exclude")
                if excludes == []: raise Exception()
                for i in range(0, len(excludes)):
                    excludes[i] = self.youtube_episodeUrl % excludes[i].split("list=")[-1]
                x = [i for i in self.list if not i['url'] in excludes]
                self.list = x
            except:
                pass

        return self.list

class episodes:
    def __init__(self):
        self.list = []
        self.data = []
        self.nickelodeonUrl			= 'http://www.nickelodeon.gr'
        self.youtubeUrl				= 'http://gdata.youtube.com'
        self.youtube_showsUrl		= 'http://gdata.youtube.com/feeds/api/users/%s/playlists'
        self.youtube_episodeUrl		= 'http://gdata.youtube.com/feeds/api/playlists/%s'
        self.youtube_recentUrl		= 'http://gdata.youtube.com/feeds/api/users/%s/uploads'
        self.youtube_searchUrl		= 'http://gdata.youtube.com/feeds/api/videos?q='

    def get(self, show, url):
        if url.startswith(self.nickelodeonUrl):
            self.list = self.nickelodeon_list(show, url)
        elif url.startswith(self.youtubeUrl):
            self.list = self.youtube_list(show, url)
        else:
            self.list = self.various_list(show, url)
        index().episodeList(self.list)

    def various_list(self, show, url):
        try:
            file = open(addonVarious,'r')
            result = file.read()
            file.close()
            quote = urllib.quote_plus(show).replace('%','').replace('+','')
            result = result.replace('name="%s"' % show, 'name="%s"' % quote)
            result = common.parseDOM(result, "show", attrs = { "name": quote })[0]

            episodes = common.parseDOM(result, "episode")
            image = common.parseDOM(result, "image")[0]
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
        except:
            return
        for episode in episodes:
            try:
                name = common.parseDOM(episode, "name")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "url")[0]
                url = cryptUrl().decode(url.encode('utf-8'))
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                self.list.append({'name': name, 'show': show, 'url': url, 'image': image, 'fanart': image})
            except:
                pass

        return self.list

    def nickelodeon_list(self, show, url):
        try:
            file = open(addonNickelodeon,'r')
            result = file.read()
            file.close()
            quote = urllib.quote_plus(show).replace('%','').replace('+','')
            result = result.replace('name="%s"' % show, 'name="%s"' % quote)
            result = common.parseDOM(result, "show", attrs = { "name": quote })[0]

            image = common.parseDOM(result, "image")[0]
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
        except:
            return

        try:
            threads = []
            result = ""
            for i in range(0, 75, 15):
                for x in range(1, 15): self.data.append('')
                episodesUrl = url + '?start=%s' % str(i)
                threads.append(Thread(self.nickelodeon_list2, episodesUrl, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "div", attrs = { "class": "catItemImageBlock" })
        except:
            return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "a", ret="title")[0]
                sort = re.sub("\D", "", name)
                sort = '%0100d' % int(sort)
                sort = sort.encode('utf-8')
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "a", ret="href")[0]
                url = '%s%s' % (self.nickelodeonUrl, url)
                url = url.encode('utf-8')
                for i in self.list:
                    if name == i['name']: raise Exception()

                self.list.append({'name': name, 'show': show, 'sort': sort, 'url': url, 'image': image, 'fanart': image})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        return self.list

    def nickelodeon_list2(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

    def youtube_list(self, show, url):
        try:
            if not url.startswith(self.youtube_searchUrl):
                threads = []
                result = ""
                for i in range(1, 250, 25):
                    for x in range(1, 25): self.data.append('')
                    episodesUrl = url + '?max-results=25&start-index=%s' % str(i)
                    threads.append(Thread(self.youtube_list2, episodesUrl, i))
                [i.start() for i in threads]
                [i.join() for i in threads]
                for i in self.data: result += i
                episodes = common.parseDOM(result, "entry")
            else:
                url = url.decode('iso-8859-7').encode('utf-8')
                params = url.split("?")[-1]
                params = dict(arg.split("=") for arg in params.split("&"))
                query = params["q"]
                match = urllib.quote_plus(query).replace('%','').replace('+','')
                url = url.replace(query, urllib.quote_plus(query))
                threads = []
                result = ""
                for i in range(1, 250, 25):
                    for x in range(1, 25): self.data.append('')
                    episodesUrl = url + '&max-results=25&start-index=%s' % str(i)
                    threads.append(Thread(self.youtube_list2, episodesUrl, i))
                [i.start() for i in threads]
                [i.join() for i in threads]
                for i in self.data: result += i
                episodes = []
                filter = common.parseDOM(result, "entry")
                for episode in filter:
                    name = common.parseDOM(episode, "title")[0]
                    name = urllib.quote_plus(name.encode('utf-8')).replace('%','').replace('+','')
                    if match in name: episodes.append(episode)
        except:
            return
        for episode in episodes:
            try:
                name = common.parseDOM(episode, "title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "media:player", ret="url")[0]
                url = url.split("&amp;")[0].split("=")[-1]
                url = 'http://www.youtube.com/watch?v=%s' % url
                url = url.encode('utf-8')
                image = common.parseDOM(episode, "media:thumbnail", ret="url")[0]
                image = image.replace(image.split("/")[-1], '0.jpg')
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'show': show, 'url': url, 'image': image})
            except:
                pass

        return self.list

    def youtube_list2(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class player:
    def __init__(self):
        self.nickelodeonUrl		= 'http://www.nickelodeon.gr'
        self.flashxUrl			= 'http://flashx.tv'
        self.streamcloudUrl		= 'http://streamcloud.eu'
        self.putlockerUrl		= 'http://www.putlocker.com'
        self.youtubeUrl			= 'http://www.youtube.com'
        self.youtube_infoUrl	= 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'

    def run(self, url):
        if url.startswith(self.flashxUrl):
            url = self.flashx(url)
        elif url.startswith(self.streamcloudUrl):
            url = self.streamcloud(url)
        elif url.startswith(self.putlockerUrl):
            url = self.putlocker(url)
        elif url.startswith(self.nickelodeonUrl):
            url = self.nickelodeon(url)
        elif url.startswith(self.youtubeUrl):
            url = self.youtube(url)

        if url is None: return
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        return url

    def flashx(self, url):
        try:
            result = getUrl(url).result
            embedUrl = re.compile('"(http://play.flashx.tv/player/embed.php.+?)"').findall(result)[0]

            post = ''
            result = getUrl(embedUrl).result
            php = re.compile('action="(.+?.php)"').findall(result)[0]
            phpUrl = 'http://play.flashx.tv/player/%s' % php
            match = common.parseDOM(result, "form", attrs = { "action": php })[0]
            match = re.compile('name="(.+?)".+?value="(.+?)"').findall(match)
            for name, value in match:
                post += '%s=%s&' % (name, urllib.quote_plus(value))

            result = getUrl(phpUrl,post=post).result
            swfUrl = re.compile('(http://play.flashx.tv/nuevo/player/player.swf.+?)"').findall(result)[0]
            cfgUrl = swfUrl.split("?config=")[-1]

            getUrl(swfUrl,referer=phpUrl).result
            result = getUrl(cfgUrl,referer=phpUrl).result
            url = common.parseDOM(result, "file")[0]

            return url
        except:
            return

    def streamcloud(self, url):
        try:
            import time
            result = getUrl(url).result

            post = ''
            match = common.parseDOM(result, "form", attrs = { "class": "proform" })[0]
            match = re.compile('name="(.+?)".+?value="(.+?)"').findall(match)
            for name, value in match:
                post += '%s=%s&' % (name, urllib.quote_plus(value))

            count = re.compile('var count(.+?)\n').findall(result)[0]
            count = int(re.sub("\D", "", count)) + 1

            time.sleep(count)
            result = getUrl(url,post=post).result
            url = re.compile('file: "(.+?)"').findall(result)[0]

            return url
        except:
            return

    def putlocker(self, url):
        try:
            import urlparse
            try: password = urlparse.parse_qs(urlparse.urlparse(url).query)['file_password'][0]
            except: password = ''
            result = getUrl(url).result
            hash = re.compile('value="(.+?)".+?name="hash"').findall(result)[0]
            post = 'hash=%s&confirm=Continue+as+Free+User&file_password=%s' % (hash, password)
            result = getUrl(url,post=post).result
            url = re.compile('href="(.+?)".+?class="download_file_link"').findall(result)[0]
            url = "http://putlocker.com%s" % url
            return url
        except:
            return

    def nickelodeon(self, url):
        try:
            result = getUrl(url).result
            url = common.parseDOM(result, "span", attrs = { "class": "itemVideo" })[0]
            url = re.compile("url: '(.+?manifest.f4m)'").findall(url)[-1]
            url = url.replace("/z/", "/i/").replace("manifest.f4m","master.m3u8")
            return url
        except:
            return

    def youtube(self, url):
        try:
            id = url.split("?v=")[-1]
            state, reason = None, None
            result = getUrl(self.youtube_infoUrl % id).result
            try:
                state = common.parseDOM(result, "yt:state", ret="name")[0]
                reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
            except:
                pass
            if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return
            try:
                result = getUrl(url).result
                alert = common.parseDOM(result, "div", attrs = { "id": "watch7-notification-area" })[0]
                return
            except:
                pass
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30351).encode("utf-8"), language(30352).encode("utf-8"))
                return
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
            return url
        except:
            return

main()