# -*- coding: utf-8 -*-

'''
    alpha podcast XBMC Addon
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
addonLogo			= os.path.join(addonPath,'resources/art/logo.png')
dataPath			= xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData			= os.path.join(dataPath,'views.cfg')
favData				= os.path.join(dataPath,'favourites.cfg')
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

        if action == None:							shows().alpha()
        elif action == 'item_play':					contextMenu().item_play()
        elif action == 'item_random_play':			contextMenu().item_random_play()
        elif action == 'item_queue':				contextMenu().item_queue()
        elif action == 'playlist_start':			contextMenu().playlist_start()
        elif action == 'playlist_open':				contextMenu().playlist_open()
        elif action == 'settings_open':				contextMenu().settings_open()
        elif action == 'global_view':				contextMenu().global_view()
        elif action == 'episodes':					episodes().get(show, url)
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

    def showList(self, showList):
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

class shows:
    def __init__(self):
        self.list = []
        self.alphaUrl			= 'http://www.alpha989.com'

    def alpha(self):
        #self.list = self.alpha_list()
        self.list = cache(self.alpha_list)
        index().showList(self.list)

    def alpha_list(self):
        try:
            result = getUrl(self.alphaUrl).result
            result = common.parseDOM(result, "div", attrs = { "class": "producersHome" })[0]
            shows = common.parseDOM(result, "div", attrs = { "class": "pItem" })
            self.list.append({'name': 'Συνεντεύξεις'.decode('iso-8859-7').encode('utf-8'), 'url': self.alphaUrl, 'image': addonLogo.encode('utf-8')})
        except:
            return
        for show in shows:
            try:
                name = common.parseDOM(show, "h2")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(show, "a", ret="href")[0]
                url = '%s/%s' % (self.alphaUrl, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = addonLogo.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class episodes:
    def __init__(self):
        self.list = []
        self.data = []
        self.alphaUrl			= 'http://www.alpha989.com'

    def get(self, show, url):
        if url == self.alphaUrl:
            self.list = self.alpha_list3(show, url)
        else:
            self.list = self.alpha_list(show, url)
        index().episodeList(self.list)

    def alpha_list(self, show, url):
        try:
            threads = []
            for i in range(1, 6):
                self.data.append('')
                episodesUrl = '%s&p=%s' % (url, str(i))
                threads.append(Thread(self.alpha_list2, episodesUrl, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            result = ""
            for i in self.data:
                result += common.parseDOM(i, "div", attrs = { "class": "playNow" })[0]

            episodes = common.parseDOM(result, "div", attrs = { "id": "cphMainTop.+?" })
        except:
            return
        for episode in episodes:
            try:
                time = episode.split(">")[-1].strip().split(" ")[-1]
                title = common.parseDOM(episode, "b")[0]
                name = '%s - %s' % (time, title)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "a", ret="href")[0]
                url = '%s/%s' % (self.alphaUrl, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = addonLogo.encode('utf-8')
                self.list.append({'name': name, 'show': show, 'url': url, 'image': image})
            except:
                pass

        return self.list

    def alpha_list2(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i-1] = result
        except:
            return

    def alpha_list3(self, show, url):
        try:
            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "class": "interBoxHome" })[0]
            episodes = common.parseDOM(result, "div", attrs = { "class": "iItems.+?" })
        except:
            return
        for episode in episodes:
            try:
                time = common.parseDOM(episode, "div", attrs = { "class": "dateTime" })[0]
                title = common.parseDOM(episode, "div", attrs = { "class": "text" })[0]
                title = common.parseDOM(title, "a")[0]
                name = '%s - %s' % (time, title)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "div", attrs = { "class": "text" })[0]
                url = common.parseDOM(url, "a", ret="href")[0]
                url = '%s/%s' % (self.alphaUrl, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = addonLogo.encode('utf-8')
                self.list.append({'name': name, 'show': show, 'url': url, 'image': image})
            except:
                pass

        return self.list

class player:
    def run(self, url):
        try:
            result = getUrl(url).result
            try:
                result = common.parseDOM(result, "div", attrs = { "class": "playNow" })[0]
            except:
                pass
            try:
                result = common.parseDOM(result, "div", attrs = { "class": "mainContent" })[0]
            except:
                pass
            rtmp = re.compile("streamer:.+?'(.+?)'").findall(result)[0]
            playpath = re.compile("file:.+?'(.+?)'").findall(result)[0]
            if not 'mp3:' in playpath: playpath = 'mp3:' + playpath

            item = xbmcgui.ListItem(path=rtmp, iconImage=addonLogo, thumbnailImage=addonLogo)
            item.setProperty('PlayPath', playpath) 
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        except:
            return

main()