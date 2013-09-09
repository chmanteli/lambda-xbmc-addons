# -*- coding: utf-8 -*-

'''
    mega replay XBMC Addon
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
dataPath			= xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData			= os.path.join(dataPath,'views.cfg')
favData				= os.path.join(dataPath,'favourites4.cfg')
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
        elif action == 'category2':					categories().get2()
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
        elif action == 'megatv_series':				shows().megatv_series()
        elif action == 'megatv_shows':				shows().megatv_shows()
        elif action == 'megatv_info':				shows().megatv_info()
        elif action == 'megatv_cook':				shows().megatv_cook()
        elif action == 'megatv_classics':			shows().megatv_classics()
        elif action == 'cinegreece':				shows().cinegreece()
        elif action == 'episodes':					episodes().get(show, url)
        elif action == 'episodes_news':				episodes().megatv_news()
        elif action == 'episodes_sports':			episodes().megatv_sports()
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
    def __init__(self, url, fetch=True, mobile=False, proxy=None, referer=None, cookie=None):
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
        xbmc.executebuiltin("Notification(%s,%s, 3000)" % (header, str))

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
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "TVShowTitle": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def episodeList(self, episodeList):
        total = len(episodeList)
        for i in episodeList:
            try:
                name, show, url, image = i['name'], i['show'], i['url'], i['image']
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
                item.setProperty("Fanart_Image", addonFanart)
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
            index().infoDialog(language(30303).encode("utf-8"))
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
            index().infoDialog(language(30304).encode("utf-8"))
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
            index().infoDialog(language(30305).encode("utf-8"))
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
            index().infoDialog(language(30306).encode("utf-8"))
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
        catList.append({'name': 30502, 'image': 'MEGA TV.png', 'action': 'category2'})
        catList.append({'name': 30503, 'image': 'YouTube.png', 'action': 'cinegreece'})
        catList.append({'name': 30504, 'image': 'News.png', 'action': 'episodes_news'})
        catList.append({'name': 30505, 'image': 'Sports.png', 'action': 'episodes_sports'})
        index().catList(catList)

    def get2(self):
        catList = []
        catList.append({'name': 30506, 'image': 'Series.png', 'action': 'megatv_series'})
        catList.append({'name': 30507, 'image': 'Shows.png', 'action': 'megatv_shows'})
        catList.append({'name': 30508, 'image': 'Info.png', 'action': 'megatv_info'})
        catList.append({'name': 30509, 'image': 'Cook.png', 'action': 'megatv_cook'})
        catList.append({'name': 30510, 'image': 'Classics.png', 'action': 'megatv_classics'})
        index().catList(catList)

class shows:
    def __init__(self):
        self.list = []
        self.megatvUrl				= 'http://www.megatv.com'
        self.megatv_seriesUrl		= 'http://www.megatv.com/webtv/default.asp?catid=27548'
        self.megatv_showsUrl		= 'http://www.megatv.com/webtv/default.asp?catid=30453'
        self.megatv_infoUrl			= 'http://www.megatv.com/webtv/default.asp?catid=30457'
        self.megatv_cookUrl			= 'http://www.megatv.com/webtv/cook/default.asp?catid=30088'
        self.megatv_classicsUrl		= 'http://www.megatv.com/classics.asp?catid=29991'
        self.cinegreeceUrl			= 'http://www.cinegreece.com'
        self.cinegreece_showsUrl	= 'http://www.cinegreece.com/2012/05/mega.html'

    def megatv_series(self):
        #self.list = self.megatv_list(self.megatv_seriesUrl)
        self.list = cache(self.megatv_list, self.megatv_seriesUrl)
        index().showList(self.list)

    def megatv_shows(self):
        #self.list = self.megatv_list(self.megatv_showsUrl)
        self.list = cache(self.megatv_list, self.megatv_showsUrl)
        index().showList(self.list)

    def megatv_info(self):
        #self.list = self.megatv_list(self.megatv_infoUrl)
        self.list = cache(self.megatv_list, self.megatv_infoUrl)
        index().showList(self.list)

    def megatv_cook(self):
        #self.list = self.megatv_list(self.megatv_cookUrl)
        self.list = cache(self.megatv_list, self.megatv_cookUrl)
        index().showList(self.list)

    def megatv_classics(self):
        #self.list = self.megatv_list(self.megatv_classicsUrl)
        self.list = cache2(self.megatv_list, self.megatv_classicsUrl)
        index().showList(self.list)

    def cinegreece(self):
        #self.list = self.cinegreece_list()
        self.list = cache(self.cinegreece_list)
        index().showList(self.list)

    def megatv_list(self, url):
        try:
            catUrl = url
            result = getUrl(url).result
            result = result.decode('iso-8859-7').encode('utf-8')
            v1 = '/webtv/'
            if re.search('/webtv/',url) is None: v1 = '/'
            match = re.search("addPrototypeElement[(]'.+?','REST','(.+?)','(.+?)'.+?[)]", result)
            v2,v3 = match.groups()
            aspUrl = '%s%s%s?%s' % (self.megatvUrl, v1, v2, v3)
            aspUrl = aspUrl.replace('/../','/')

            result = getUrl(aspUrl).result
            result = result.decode('iso-8859-7').encode('utf-8')
            result = common.parseDOM(result, "ul")[0]

            shows = common.parseDOM(result, "li", attrs = { "class": "lichild" })
            if not shows:
                shows = common.parseDOM(result, "li")
        except:
            return
        for show in shows:
            try:
                name = common.parseDOM(show, "a")[-1]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(show, "a", ret="href")[0]
                url = url.split("catid=")[-1].replace("')",'')
                url = '%s&catidlocal=%s' % (catUrl, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                if url.endswith(self.megatv_classicsUrl.split("catid=")[-1]) : continue
                if re.search('Megalicious Classics',name) is not None: continue
                self.list.append({'name': name, 'url': url})
            except:
                pass

        threads = []
        for i in range(0, len(self.list)):
            threads.append(Thread(self.megatv_list2, self.list[i]['url'], i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        return self.list

    def megatv_list2(self, url, i):
        try:
            image = episodes().megatv_list('', url, 'image')
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
            self.list[i]['image'] = image
        except:
            return

    def cinegreece_list(self):
        try:
            result = getUrl(self.cinegreece_showsUrl).result
            shows = common.parseDOM(result, "div", attrs = { "itemprop": "articleBody" })[0]
            shows = re.compile('(<a.+?</a>)').findall(shows)
        except:
            return
        for show in shows:
            try:
                name = common.parseDOM(show, "img", ret="title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(show, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.replace(url.split("/")[2], self.cinegreeceUrl.split("//")[-1])
                url = url.encode('utf-8')
                image = common.parseDOM(show, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('name'))
        return self.list

class episodes:
    def __init__(self):
        self.list = []
        self.data = []
        self.megatvUrl			= 'http://www.megatv.com'
        self.megatv_newsUrl		= 'http://www.megatv.com/webtv/default.asp?catid=24616&catidlocal=24616'
        self.megatv_sportsUrl	= 'http://www.megatv.com/webtv/default.asp?catid=24616&catidlocal=30200'
        self.cinegreeceUrl		= 'http://www.cinegreece.com'

    def get(self, show, url):
        if url.startswith(self.megatvUrl):
            self.list = self.megatv_list(show, url)
        elif url.startswith(self.cinegreeceUrl):
            self.list = self.cinegreece_list(show, url)
        index().episodeList(self.list)

    def megatv_news(self):
        self.list = self.megatv_list('MEGA TV', self.megatv_newsUrl)
        index().episodeList(self.list)

    def megatv_sports(self):
        self.list = self.megatv_list('MEGA TV', self.megatv_sportsUrl)
        index().episodeList(self.list)

    def megatv_list(self, show, url, mode=None):
        try:
            result = getUrl(url).result
            result = result.decode('iso-8859-7').encode('utf-8')
            v1 = '/webtv/'
            if re.search('/webtv/',url) is None: v1 = '/'
            match = re.search("addPrototypeElement[(]'.+?','REST','(.+?)','(.+?)'.+?[)]", result)
            v2,v3 = match.groups()
            aspUrl = '%s%s%s?%s' % (self.megatvUrl, v1, v2, v3)
            aspUrl = aspUrl.replace('/../','/')

            threads = []
            result, count = "", 11
            if mode is not None: count = 2
            for i in range(1, count):
                self.data.append('')
                aspUrl = '%s&page1=%s&page2=%s' % (url, str(i), str(i))
                threads.append(Thread(self.megatv_list2, aspUrl, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "div", attrs = { "class": "thumbboxna" })
            episodes = uniqueList(episodes).list
        except:
            return
        for episode in episodes:
            try:
                image = common.parseDOM(episode, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                if mode is not None: return image

                try:
                    name = common.parseDOM(episode, "h3")[0]
                    name = common.parseDOM(name, "a")[0]
                except:
                    pass
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="href")[0]
                if url.startswith('JAVASCRIPT') or url.startswith('default.asp'):
                    url = url.split("catid=")[-1].replace("')",'')
                    url = '%s/r.asp?catid=%s' % (self.megatvUrl, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'show': show, 'url': url, 'image': image})
            except:
                pass

        return self.list

    def megatv_list2(self, url, i):
        try:
            result = getUrl(url).result
            result = result.decode('iso-8859-7').encode('utf-8')
            self.data[i-1] = result
        except:
            return

    def cinegreece_list(self, show, url):
        try:
            result = getUrl(url).result
            image = common.parseDOM(result, "div", attrs = { "class": "separator" })[0]
            image = common.parseDOM(image, "img", ret="src")[0]
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
            episodes = re.compile('(<button.+?a="a".+?</button>)').findall(result)
            episodes = uniqueList(episodes).list
        except:
            return
        for episode in episodes:
            try:
                name = common.parseDOM(episode, "button")[0]
                name = name.replace('&nbsp;&nbsp;&nbsp;','-').strip()
                name = 'Επεισόδιο '.decode('iso-8859-7') + name
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "button", ret="onclick")[0]
                url = re.compile("'(.+?)'").findall(url)[0]
                url = url.split("&amp;")[0].split("/")[-1].split("=")[-1]
                url = 'http://www.youtube.com/watch?v=%s' % url
                url = url.encode('utf-8')
                self.list.append({'name': name, 'show': show, 'url': url, 'image': image})
            except:
                pass

        return self.list

class player:
    def __init__(self):
        self.megatvUrl			= 'http://www.megatv.com'
        self.youtubeUrl			= 'http://www.youtube.com'

    def run(self, url):
        if url.startswith(self.megatvUrl):
            url = self.megatv(url)
        elif url.startswith(self.youtubeUrl):
            url = self.youtube(url)

        if url is None: return
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        return url

    def megatv(self, url):
        try:
            url = url.split("catid=")[-1]
            url = 'http://www.megatv.com/XML/jw/videolists.asp?catid=%s&attributes=0&nostore=true' % url
            result = getUrl(url).result

            playpath = common.parseDOM(result, "location")[-1]
            try:
                rtmp = common.parseDOM(result, "meta", attrs = { "rel": "streamer" })[0]
            except:
                rtmp = ""

            if playpath.endswith("/manifest.f4m"):
                rtmp = 'rtmp://cp78455.edgefcs.net/ondemand/vod/'
                try:
                    playpath = re.compile('.+?,.+?,(.+?),.csmil/manifest.f4m').findall(playpath)[0]
                except:
                    playpath = re.compile('.+?,(.+?),.csmil/manifest.f4m').findall(playpath)[0]

            url = '%s%s timeout=10' % (rtmp, playpath)
            if not url.startswith('rtmp://'):
                url = '%s%s' % (rtmp, playpath)

            return url
        except:
            return

    def youtube(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30351).encode("utf-8"), language(30352).encode("utf-8"))
                return
            url = url.split("?v=")[-1]
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
            return url
        except:
            return

main()