# -*- coding: utf-8 -*-

'''
    ant1 player XBMC Addon
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


language            = xbmcaddon.Addon().getLocalizedString
setSetting          = xbmcaddon.Addon().setSetting
getSetting          = xbmcaddon.Addon().getSetting
addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonDesc           = language(30450).encode("utf-8")
addonIcon           = os.path.join(addonPath,'icon.png')
addonFanart         = os.path.join(addonPath,'fanart.jpg')
addonArt            = os.path.join(addonPath,'resources/art')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData            = os.path.join(dataPath,'views.cfg')
favData             = os.path.join(dataPath,'favourites2.cfg')
cache               = StorageServer.StorageServer(addonName+addonVersion,24).cacheFunction
cache2              = StorageServer.StorageServer(addonName+addonVersion,240).cacheFunction
common              = CommonFunctions
action              = None


class main:
    def __init__(self):
        global action
        index().container_data()
        params = {}
        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
        for param in splitparams:
            if (len(param) > 0):
                splitparam = param.split('=')
                key = splitparam[0]
                try:    value = splitparam[1].encode("utf-8")
                except: value = splitparam[1]
                params[key] = value

        try:        action = urllib.unquote_plus(params["action"])
        except:     action = None
        try:        name = urllib.unquote_plus(params["name"])
        except:     name = None
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None
        try:        image = urllib.unquote_plus(params["image"])
        except:     image = None
        try:        show = urllib.unquote_plus(params["show"])
        except:     show = None

        if action == None:                          categories().get()
        elif action == 'item_play':                 contextMenu().item_play()
        elif action == 'item_random_play':          contextMenu().item_random_play()
        elif action == 'item_queue':                contextMenu().item_queue()
        elif action == 'item_play_from_here':       contextMenu().item_play_from_here(url)
        elif action == 'favourite_add':             contextMenu().favourite_add(name, url, image)
        elif action == 'favourite_delete':          contextMenu().favourite_delete(name, url, image)
        elif action == 'favourite_moveUp':          contextMenu().favourite_moveUp(name, url, image)
        elif action == 'favourite_moveDown':        contextMenu().favourite_moveDown(name, url, image)
        elif action == 'playlist_start':            contextMenu().playlist_start()
        elif action == 'playlist_open':             contextMenu().playlist_open()
        elif action == 'settings_open':             contextMenu().settings_open()
        elif action == 'global_view':               contextMenu().global_view()
        elif action == 'favourites':                favourites().get()
        elif action == 'antenna_shows':             shows().antenna()
        elif action == 'episodes':                  episodes().get(show, url)
        elif action == 'episodes_recent':           episodes().antenna_recent()
        elif action == 'episodes_news':             episodes().antenna_news()
        elif action == 'episodes_sports':           episodes().antenna_sports()
        elif action == 'play':                      player().run(url)

        xbmcplugin.setContent(int(sys.argv[1]), 'Episodes')
        index().container_view({'skin.confluence' : 503})
        xbmcplugin.setPluginFanart(int(sys.argv[1]), addonFanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return

class getUrl(object):
    def __init__(self, url, fetch=True, close=True, cookie=False, mobile=False, proxy=None, post=None, referer=None):
        if not proxy is None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if cookie == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post is None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
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
        if close == True:
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
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
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
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

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
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

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
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

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
        catList.append({'name': 30502, 'image': 'Shows.png', 'action': 'antenna_shows'})
        catList.append({'name': 30503, 'image': 'Recent.png', 'action': 'episodes_recent'})
        catList.append({'name': 30504, 'image': 'News.png', 'action': 'episodes_news'})
        catList.append({'name': 30505, 'image': 'Sports.png', 'action': 'episodes_sports'})
        index().catList(catList)

class link:
    def __init__(self):
        self.antenna_base = 'http://www.antenna.gr'
        self.antenna_shows = 'http://www.antenna.gr/templates/data/az?letter='
        self.antenna_episodes = 'http://www.antenna.gr/templates/data/categories?cid='
        self.antenna_news = 'http://www.antenna.gr/webtv/categories?cid=3067'
        self.antenna_sports = 'http://www.antenna.gr/webtv/categories?cid=3062'
        self.antenna_recent = 'http://www.antenna.gr/templates/data/webtvLatest?xsl=t'

class shows:
    def __init__(self):
        self.list = []
        self.data = ''

    def antenna(self):
        #self.list = self.antenna_list()
        self.list = cache(self.antenna_list)
        index().showList(self.list)

    def antenna_list(self):
        try:
            threads = []
            letters = ['%u0391', '%u0392', '%u0393', '%u0394', '%u0395', '%u0396', '%u0397', '%u0398', '%u0399', '%u039A', '%u039B', '%u039C', '%u039D', '%u039E', '%u039F', '%u03A0', '%u03A1', '%u03A3', '%u03A4', '%u03A5', '%u03A6', '%u03A7', '%u03A8', '%u03A9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1-9']
            for letter in letters:
                url = '%s%s' % (link().antenna_shows, letter)
                threads.append(Thread(self.antenna_list2, url))
            [i.start() for i in threads]
            [i.join() for i in threads]
            result = self.data
            shows = common.parseDOM(result, "dl")
        except:
            return
        for show in shows:
            try:
                name = re.compile('</div>(.+?)<div').findall(show)[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(show, "a", ret="href")[0]
                url = '%s%s' % (link().antenna_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(show, "img", ret="src")[0]
                image = '%s%s' % (link().antenna_base, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('name'))
        return self.list

    def antenna_list2(self, url):
        try:
            result = getUrl(url).result
            self.data += result
        except:
            return

class episodes:
    def __init__(self):
        self.list = []
        self.data = []

    def get(self, show, url):
        self.list = self.antenna_list(show, url)
        index().episodeList(self.list)

    def antenna_recent(self):
        self.list = self.antenna_list3('ANT1 TV', link().antenna_recent)
        index().episodeList(self.list)

    def antenna_news(self):
        self.list = self.antenna_list('ANT1 TV', link().antenna_news)
        index().episodeList(self.list)

    def antenna_sports(self):
        self.list = self.antenna_list('ANT1 TV', link().antenna_sports)
        index().episodeList(self.list)

    def antenna_list(self, show, url):
        try:
            episodesUrl = url.split("=")[-1]
            episodesUrl = '%s%s' % (link().antenna_episodes, episodesUrl)
            result = getUrl(episodesUrl).result
            count = common.parseDOM(result, "a", attrs = { "class": "paging" })[-1]
            count = int(count)+1
            if count > 20: count = 20
            threads = []
            for i in range(1, count):
                self.data.append('')
                url = '%s&p=%s' % (episodesUrl, str(i))
                threads.append(Thread(self.antenna_list2, url, i-1))
            [i.start() for i in threads]
            [i.join() for i in threads]
            result = ''
            for i in self.data: result += i

            episodes = re.compile('(<div class=.+?)<div class="teasertext"').findall(result)
            episodes = uniqueList(episodes).list
        except:
            return
        for episode in episodes:
            try:
                name = common.parseDOM(episode, "div", attrs = { "class": "title" })[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "a", ret="href")[0]
                url = '%s%s' % (link().antenna_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(episode, "img", ret="src")[0]
                image = '%s%s' % (link().antenna_base, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'show': show, 'url': url, 'image': image})
            except:
                pass

        return self.list

    def antenna_list2(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

    def antenna_list3(self, show, url):
        try:
            threads = []
            episodesUrl = url
            for i in range(1, 8):
                self.data.append('')
                url = '%s&p=%s' % (episodesUrl, str(i))
                threads.append(Thread(self.antenna_list2, url, i-1))
            [i.start() for i in threads]
            [i.join() for i in threads]
            result = ''
            for i in self.data: result += i

            episodes = re.compile('(<div class=.+?)<div class="teasertext"').findall(result)
            episodes = uniqueList(episodes).list
        except:
            return
        for episode in episodes:
            try:
                name = common.parseDOM(episode, "div", attrs = { "class": "title" })[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "a", ret="href")[0]
                url = '%s%s' % (link().antenna_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(episode, "img", ret="src")[0]
                image = '%s%s' % (link().antenna_base, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'show': show, 'url': url, 'image': image})
            except:
                pass

        return self.list

class player:
    def __init__(self):
        self.data = ''

    def run(self, url):
        url = self.antenna(url)
        if url is None: return
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        return url

    def antenna(self, url):
        dataUrl = url.replace('watch','templates/data/player')
        swfUrl = 'http://www.antenna.gr/webtv/images/fbplayer.swf'
        pageUrl = url
        proxy = '%s:%s' % (getSetting("proxyip"), getSetting("proxyport"))

        try:
            result = getUrl(dataUrl).result
            rtmp = common.parseDOM(result, "FMS")[0]
            playpath = common.parseDOM(result, "appStream")[0]
            if not playpath.endswith('/GR.flv'):
                url = '%s playpath=%s pageUrl=%s swfUrl=%s swfVfy=true timeout=10' % (rtmp, playpath, pageUrl, swfUrl)
                if playpath.startswith('http://'): url = playpath
                return url
        except:
            pass

        try:
            threads = []
            proxies = self.proxynova()
            proxies.insert(0, proxy)
            for proxy in proxies: threads.append(Thread(self.antenna2, dataUrl, proxy))
            [i.start() for i in threads]
            [i.join() for i in threads]
            result = self.data
            rtmp = common.parseDOM(result, "FMS")[0]
            playpath = common.parseDOM(result, "appStream")[0]
            if not playpath.endswith('/GR.flv'):
                url = '%s playpath=%s pageUrl=%s swfUrl=%s swfVfy=true timeout=10' % (rtmp, playpath, pageUrl, swfUrl)
                if playpath.startswith('http://'): url = playpath
                return url
            else:
                raise Exception()
        except:
            index().okDialog(language(30353).encode("utf-8"), '')
            contextMenu().settings_open()
            return

    def antenna2(self, url, proxy):
        try:
            result = getUrl(url,proxy=proxy).result
            self.data += result
        except:
            return

    def proxynova(self):
        try:
            hostList = []
            url = 'http://www.proxynova.com/proxy-server-list/country-gr/'
            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            hosts = common.parseDOM(result, "tr")
        except:
            return []
        for host in hosts:
            try:
                time = common.parseDOM(host, "time", attrs = { "class": "time-ago recent" })[0]
                name = common.parseDOM(host, "span", attrs = { "class": "row_proxy_ip" })[0]
                hostList.append(name)
            except:
                pass

        proxyList = []
        hostList = uniqueList(hostList[:4]).list
        portList = [':80', ':8080', ':3128', ':8000']
        for port in portList:
            for host in hostList: proxyList.append(host+port)

        return proxyList

main()