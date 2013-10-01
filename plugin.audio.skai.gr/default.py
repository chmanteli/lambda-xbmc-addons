# -*- coding: utf-8 -*-

'''
    skai podcast XBMC Addon
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
addonGenre			= language(30451).encode("utf-8")
addonIcon			= os.path.join(addonPath,'icon.png')
addonFanart			= os.path.join(addonPath,'resources/fanart/1.jpg')
addonFanart2		= os.path.join(addonPath,'resources/fanart/2.jpg')
addonArt			= os.path.join(addonPath,'resources/art')
addonLogo			= 'special://home/addons/%s/resources/art/logo.png' % (addonId)
dataPath			= xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData			= os.path.join(dataPath,'views.cfg')
favData				= os.path.join(dataPath,'favourites2.cfg')
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
        elif action == 'favourite_add':				contextMenu().favourite_add(name, url, image)
        elif action == 'favourite_delete':			contextMenu().favourite_delete(name, url, image)
        elif action == 'favourite_moveUp':			contextMenu().favourite_moveUp(name, url, image)
        elif action == 'favourite_moveDown':		contextMenu().favourite_moveDown(name, url, image)
        elif action == 'playlist_start':			contextMenu().playlist_start()
        elif action == 'playlist_open':				contextMenu().playlist_open()
        elif action == 'settings_open':				contextMenu().settings_open()
        elif action == 'global_view':				contextMenu().global_view()
        elif action == 'favourites':				favourites().get()
        elif action == 'skai_shows':				shows().skai()
        elif action == 'episodes':					episodes().get(show, url)
        elif action == 'episodes_recent':			episodes().skai_recent()
        elif action == 'episodes_news':				episodes().skai_news()
        elif action == 'episodes_sports':			episodes().skai_sports()
        elif action == 'play':						player().run(url)

        viewDict = {
            'skin.confluence'	: 506,	'skin.aeon.nox'		: 50,	'skin.back-row'			: 50,
            'skin.bello'		: 50,	'skin.carmichael'	: 50,	'skin.diffuse'			: 55,
            'skin.droid'		: 50,	'skin.metropolis'	: 55,	'skin.pm3-hd'			: 51,
            'skin.rapier'		: 52,	'skin.re-touched'	: 50,	'skin.simplicity'		: 50,
            'skin.transparency'	: 51,	'skin.xeebo'		: 50,	'skin.xperience1080'	: 50
            }

        xbmcplugin.setContent(int(sys.argv[1]), 'Albums')
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
        count = 0
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
                item.setInfo( type="Music", infoLabels={ "Title": name, "Label": name, "Album": name, "Genre": addonGenre } )
                item.setProperty("Album_Description", addonDesc)
                count = count + 1
                if count % 2 == 0:
                    item.setProperty("Fanart_Image", addonFanart2)
                else:
                    item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def catList(self, catList):
        total = len(catList)
        count = 0
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
                item.setInfo( type="Music", infoLabels={ "Title": name, "Label": name, "Album": name } )
                item.setProperty("Album_Description", addonDesc)
                count = count + 1
                if count % 2 == 0:
                    item.setProperty("Fanart_Image", addonFanart2)
                else:
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
        count = 0
        for i in showList:
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
                if not url in favRead:
                    cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                else:
                    cm.append((language(30414).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Music", infoLabels={ "Title": name, "Label": name, "Album": name, "Genre": addonGenre } )
                item.setProperty("Album_Description", addonDesc)
                count = count + 1
                if count % 2 == 0:
                    item.setProperty("Fanart_Image", addonFanart2)
                else:
                    item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def episodeList(self, episodeList):
        total = len(episodeList)
        count = 0
        for i in episodeList:
            try:
                name, show, url, image = i['name'], i['show'], i['url'], i['image']
                sysurl = urllib.quote_plus(url)
                u = '%s?action=play&url=%s' % (sys.argv[0], sysurl)

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
                item.setInfo( type="Music", infoLabels={ "Title": name, "Label": name, "Album": name, "Artist": show, "Genre": addonGenre, "Comment": addonDesc } )
                item.setProperty("IsPlayable", "true")
                item.setProperty( "Music", "true" )
                item.setProperty("Album_Label", show)
                item.setProperty("Album_Description", addonDesc)
                count = count + 1
                if count % 2 == 0:
                    item.setProperty("Fanart_Image", addonFanart2)
                else:
                    item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

class contextMenu:
    def item_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.unshuffle()
        xbmc.Player().play(playlist)

    def item_random_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.shuffle()
        xbmc.Player().play(playlist)

    def item_queue(self):
        xbmc.executebuiltin('Action(Queue)')

    def playlist_start(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        playlist.unshuffle()
        xbmc.Player().play(playlist)

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(MusicPlaylist)')

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
            if xbmcgui.getCurrentWindowId() == 10501:
                src +=  'MyMusicSongs.xml'
            else:
                src += 'MyMusicNav.xml'
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
        catList.append({'name': 30502, 'image': 'Shows.png', 'action': 'skai_shows'})
        catList.append({'name': 30503, 'image': 'Recent.png', 'action': 'episodes_recent'})
        catList.append({'name': 30504, 'image': 'News.png', 'action': 'episodes_news'})
        catList.append({'name': 30505, 'image': 'Sports.png', 'action': 'episodes_sports'})
        index().catList(catList)

class shows:
    def __init__(self):
        self.list = []
        self.data = ''
        self.skaiUrl			= 'http://www.skai.gr/player/radio'
        self.skaiUrl2			= 'http://www.skai.gr/ajax.aspx?m=Skai.Player.ItemView&type=Radio'

    def skai(self):
        #self.list = self.skai_list()
        self.list = cache(self.skai_list)
        index().showList(self.list)

    def skai_list(self):
        try:
            result = getUrl(self.skaiUrl).result
            results = common.parseDOM(result, "div", attrs = { "class": "col_.+?" })

            shows = ""
            for result in results: shows += result
            shows = common.parseDOM(shows, "li")
        except:
            return
        for show in shows:
            try:
                name = common.parseDOM(show, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(show, "a", ret="href")[0]
                url = url.split("(")[-1].split(",")[0]
                url = '%s&alid=%s&cid=6' % (self.skaiUrl2, str(url))
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = addonLogo.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('name'))
        return self.list

class episodes:
    def __init__(self):
        self.list = []
        self.data = []
        self.skaiUrl			= 'http://www.skai.gr/player/radio'
        self.skaiUrl2			= 'http://www.skai.gr/ajax.aspx?m=Skai.Player.ItemView&type=Radio'
        self.skairecentUrl		= 'http://www.skai.gr/ajax.aspx?m=Skai.Player.ItemView&type=Radio&cid=0'
        self.skainewsUrl		= 'http://www.skai.gr/ajax.aspx?m=Skai.Player.ItemView&type=Radio&alid=64035&cid=6'
        self.skaisportsUrl		= 'http://www.skai.gr/ajax.aspx?m=Skai.Player.ItemView&type=Radio&alid=63975&cid=6'

    def get(self, show, url):
        self.list = self.skai_list(show, url)
        index().episodeList(self.list)

    def skai_recent(self):
        self.list = self.skai_list('SKAI 1003', self.skairecentUrl)
        index().episodeList(self.list[:100])

    def skai_news(self):
        self.list = self.skai_list('SKAI 1003', self.skainewsUrl)
        index().episodeList(self.list[:100])

    def skai_sports(self):
        self.list = self.skai_list('SKAI 1003', self.skaisportsUrl)
        index().episodeList(self.list[:100])

    def skai_list(self, show, url):
        try:
            threads = []
            result = ""
            for i in range(1, 11):
                self.data.append('')
                episodesUrl = '%s&Page=%s' % (url, str(i))
                threads.append(Thread(self.skai_list2, episodesUrl, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "Item")
            episodes = uniqueList(episodes).list
        except:
            return
        for episode in episodes:
            try:
                title = common.parseDOM(episode, "Title")[0]
                title = title.split('[')[-1].split(']')[0]
                date = common.parseDOM(episode, "Date")[0]
                date = date.split('[')[-1].split(']')[0]
                date = date.split('T')[0].replace('-', '.')
                name = '%s - %s' % (title, date)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "File")[0]
                url = url.split('[')[-1].split(']')[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = addonLogo.encode('utf-8')
                self.list.append({'name': name, 'show': show, 'url': url, 'image': image})
            except:
                pass

        return self.list

    def skai_list2(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i-1] = result
        except:
            return

class player:
    def __init__(self):
        self.skaiUrl			= 'http://www.skai.gr/player/radio'

    def run(self, url):
        url = self.skai(url)
        if url is None: return
        item = xbmcgui.ListItem(path=url, iconImage=addonLogo, thumbnailImage=addonLogo)
        item.setInfo( type="Video", infoLabels={ "Title": "" } )
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        return url

    def skai(self, url):
        swfUrl = 'http://www.skai.gr/files/1/Flash/Shows/SkaiMediaPlayer.swf'
        if url.startswith('rtmp://'):
            url = '%s pageUrl=%s swfUrl=%s swfVfy=1 timeout=10' % (url, self.skaiUrl, swfUrl)
        return url

main()