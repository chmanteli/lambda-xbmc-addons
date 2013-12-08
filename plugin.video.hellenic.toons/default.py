# -*- coding: utf-8 -*-

'''
    Hellenic Toons XBMC Addon
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

import urllib,urllib2,re,os,threading,datetime,time,xbmc,xbmcplugin,xbmcgui,xbmcaddon
from operator import itemgetter
import urlresolver
try:    import CommonFunctions
except: import commonfunctionsdummy as CommonFunctions
try:    import StorageServer
except: import storageserverdummy as StorageServer


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
addonSlideshow      = os.path.join(addonPath,'resources/slideshow')
addonVarious        = os.path.join(addonPath,'resources/data/various.xml')
addonNickelodeon    = os.path.join(addonPath,'resources/data/nickelodeon.xml')
addonClassics       = os.path.join(addonPath,'resources/data/classics.xml')
addonSongs        = os.path.join(addonPath,'resources/data/songs.xml')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData            = os.path.join(dataPath,'views.cfg')
favData             = os.path.join(dataPath,'favourites4.cfg')
cache               = StorageServer.StorageServer(addonName+addonVersion,1).cacheFunction
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
        try:        query = urllib.unquote_plus(params["query"])
        except:     query = None
        try:        imdb = urllib.unquote_plus(params["imdb"])
        except:     imdb = None
        try:        genre = urllib.unquote_plus(params["genre"])
        except:     genre = None
        try:        plot = urllib.unquote_plus(params["plot"])
        except:     plot = None
        try:        show = urllib.unquote_plus(params["show"])
        except:     show = None
        try:        season = urllib.unquote_plus(params["season"])
        except:     season = None
        try:        episode = urllib.unquote_plus(params["episode"])
        except:     episode = None
        try:        size = urllib.unquote_plus(params["size"])
        except:     size = None

        if action == None:                          root().get()
        elif action == 'item_play':                 contextMenu().item_play()
        elif action == 'item_random_play':          contextMenu().item_random_play()
        elif action == 'item_queue':                contextMenu().item_queue()
        elif action == 'item_play_from_here':       contextMenu().item_play_from_here(url)
        elif action == 'favourite_add':             contextMenu().favourite_add(favData, name, url, image, imdb)
        elif action == 'favourite_delete':          contextMenu().favourite_delete(favData, name, url)
        elif action == 'favourite_moveUp':          contextMenu().favourite_moveUp(favData, name, url)
        elif action == 'favourite_moveDown':        contextMenu().favourite_moveDown(favData, name, url)
        elif action == 'playlist_open':             contextMenu().playlist_open()
        elif action == 'settings_open':             contextMenu().settings_open()
        elif action == 'addon_home':                contextMenu().addon_home()
        elif action == 'view_root':                 contextMenu().view('root')
        elif action == 'view_tvshows':              contextMenu().view('tvshows')
        elif action == 'view_episodes':             contextMenu().view('videos')
        elif action == 'shows_various':             shows().various()
        elif action == 'shows_nickelodeon':         shows().nickelodeon()
        elif action == 'shows_classics':            shows().classics()
        elif action == 'shows_songs':               shows().songs()
        elif action == 'shows_favourites':          favourites().shows()
        elif action == 'episodes':                  episodeList().get(name, url, image, imdb, genre, plot, show)
        elif action == 'play':                      resolver().run(url, size, name)


        if action is None or action.startswith('root'):
            pass
        elif action.startswith('shows'):
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            index().container_view('tvshows', {'skin.confluence' : 500})
        elif action.startswith('episodes'):
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            index().container_view('videos', {'skin.confluence' : 504})

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

class player(xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)

    def status(self):
        return

    def run(self, name, url):
        try:
            import urlparse
            query = urlparse.urlparse(xbmc.getInfoLabel('Container.FolderPath')).query
            base = urlparse.parse_qs(query)['url'][0]
            if base.startswith(link().youtube_api): raise Exception()
            poster = urlparse.parse_qs(query)['image'][0]
        except:
            poster = ''

        item = xbmcgui.ListItem(path=url, iconImage=poster, thumbnailImage=poster)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        xbmc.sleep(3000)
        if not xbmc.getCondVisibility('Player.Paused') == 0:
            xbmc.executebuiltin('Action(Play)')

    def onPlayBackEnded(self):
        index().container_refresh()

    def onPlayBackStopped(self):
        index().container_refresh()

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
        xbmc.executebuiltin('Container.Refresh')

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

    def container_view(self, content, viewDict):
        try:
            skin = xbmc.getSkinDir()
            file = open(viewData,'r')
            read = file.read().replace('\n','')
            file.close()
            view = re.compile('"%s"[|]"%s"[|]"(.+?)"' % (skin, content)).findall(read)[0]
            xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view))
        except:
            try:
                id = str(viewDict[skin])
                xbmc.executebuiltin('Container.SetViewMode(%s)' % id)
            except:
                pass

    def rootList(self, rootList):
        count = 0
        total = len(rootList)
        for i in rootList:
            try:
                name = language(i['name']).encode("utf-8")
                image = '%s/%s' % (addonArt, i['image'])
                action = i['action']
                u = '%s?action=%s' % (sys.argv[0], action)
                fanart = '%s/%s.jpg' % (addonSlideshow, str(count)[-1])
                count = count + 1

                cm = []
                if action.startswith('episodes'): cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                if action.startswith('episodes'): cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                #cm.append((language(30427).encode("utf-8"), 'RunPlugin(%s?action=view_root)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels = {'label': name, 'title': name, 'plot': addonDesc} )
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def showList(self, showList):
        file = open(favData,'r')
        favRead = file.read()
        file.close()

        count = 0
        total = len(showList)
        for i in showList:
            try:
                name, url, image, imdb, genre, plot = i['name'], i['url'], i['image'], i['imdb'], i['genre'], i['plot']
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '
                title = name

                sysname, sysurl, sysimage, sysimdb, sysgenre, sysplot, systitle = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(imdb), urllib.quote_plus(genre), urllib.quote_plus(plot), urllib.quote_plus(title)
                u = '%s?action=episodes&url=%s&image=%s&imdb=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysurl, sysimage, sysimdb, sysgenre, sysplot, sysname)
                fanart = '%s/%s.jpg' % (addonSlideshow, str(count)[-1])
                count = count + 1
                try: fanart = i['fanart']
                except: pass

                meta = {'label': title, 'title': title, 'tvshowtitle': title, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                poster, banner = image, image
                meta.update({'art(banner)': banner, 'art(poster)': poster})

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                if action == 'shows_favourites':
                    cm.append((language(30429).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30419).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30420).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30421).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                else:
                    if not '"%s"' % url in favRead: cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    else: cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30429).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def episodeList(self, episodeList):
        count = 0
        total = len(episodeList)
        for i in episodeList:
            try:
                name, url, image, imdb, genre, plot = i['name'], i['url'], i['image'], i['imdb'], i['genre'], i['plot']
                title, show, season, episode = i['title'], i['show'], i['season'], i['episode']
                if plot == '': plot = addonDesc
                try: size = i['size']
                except: size = '0'

                sysname, sysurl, syssize = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(size)
                u = '%s?action=play&name=%s&url=%s&size=%s' % (sys.argv[0], sysname, sysurl, syssize)
                if url.startswith(link().youtube_base) or url.startswith(link().youtube_search):
                    u = '%s?action=play&name=%s&url=%s&size=%s&t=%s' % (sys.argv[0], sysname, sysurl, syssize, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
                meta = {'label': title, 'title': title, 'studio': show, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                try: meta.update({'premiered': i['date']})
                except: pass
                fanart = '%s/%s.jpg' % (addonSlideshow, str(count)[-1])
                count = count + 1
                try: fanart = i['fanart']
                except: pass
                poster = image

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_play_from_here&url=%s)' % (sys.argv[0], sysurl)))
                cm.append((language(30431).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
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
        import urlparse
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist.unshuffle()
        total = xbmc.getInfoLabel('Container.NumItems')
        for i in range(0, int(total)):
            i = str(i)
            label = xbmc.getInfoLabel('ListItemNoWrap(%s).Label' % i)
            if label == '': break

            path = xbmc.getInfoLabel('ListItemNoWrap(%s).FileNameAndPath' % i)
            query = urlparse.urlparse(path.replace(sys.argv[0],'')).query
            name, url = urlparse.parse_qs(query)['name'][0], urlparse.parse_qs(query)['url'][0]
            sysname, sysurl = urllib.quote_plus(name), urllib.quote_plus(url)
            u = '%s?action=play&name=%s&url=%s' % (sys.argv[0], sysname, sysurl)

            meta = {'label' : xbmc.getInfoLabel('ListItemNoWrap(%s).title' % i), 'title' : xbmc.getInfoLabel('ListItemNoWrap(%s).title' % i), 'tvshowtitle': xbmc.getInfoLabel('ListItemNoWrap(%s).tvshowtitle' % i), 'imdb_id' : xbmc.getInfoLabel('ListItemNoWrap(%s).imdb_id' % i), 'season' : xbmc.getInfoLabel('ListItemNoWrap(%s).season' % i), 'episode' : xbmc.getInfoLabel('ListItemNoWrap(%s).episode' % i), 'writer' : xbmc.getInfoLabel('ListItemNoWrap(%s).writer' % i), 'director' : xbmc.getInfoLabel('ListItemNoWrap(%s).director' % i), 'rating' : xbmc.getInfoLabel('ListItemNoWrap(%s).rating' % i), 'duration' : xbmc.getInfoLabel('ListItemNoWrap(%s).duration' % i), 'plot' : xbmc.getInfoLabel('ListItemNoWrap(%s).plot' % i), 'premiered' : xbmc.getInfoLabel('ListItemNoWrap(%s).premiered' % i), 'genre' : xbmc.getInfoLabel('ListItemNoWrap(%s).genre' % i)}
            poster, fanart = xbmc.getInfoLabel('ListItemNoWrap(%s).icon' % i), xbmc.getInfoLabel('ListItemNoWrap(%s).Property(Fanart_Image)' % i)

            item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=poster)
            item.setInfo( type="Video", infoLabels= meta )
            item.setProperty("IsPlayable", "true")
            item.setProperty("Video", "true")
            item.setProperty("Fanart_Image", fanart)
            playlist.add(u, item)
        xbmc.Player().play(playlist)

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(VideoPlaylist)')

    def settings_open(self):
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % (addonId))

    def addon_home(self):
        xbmc.executebuiltin('Container.Update(plugin://%s/,replace)' % (addonId))

    def view(self, content):
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
                if not line.startswith('"%s"|"%s"|"' % (skin, content)): file.write(line)
            file.write('"%s"|"%s"|"%s"\n' % (skin, content, str(view)))
            file.close()
            viewName = xbmc.getInfoLabel('Container.Viewmode')
            index().infoDialog('%s%s%s' % (language(30301).encode("utf-8"), viewName, language(30302).encode("utf-8")))
        except:
            return

    def favourite_add(self, data, name, url, image, imdb):
        try:
            index().container_refresh()
            file = open(data, 'a+')
            file.write('"%s"|"%s"|"%s"|"%s"\n' % (name, imdb, url, image))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_delete(self, data, name, url):
        try:
            index().container_refresh()
            file = open(data,'r')
            read = file.read()
            file.close()
            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"' % url in x][0]
            list = re.compile('(".+?\n)').findall(read.replace(line, ''))
            file = open(data, 'w')
            for line in list: file.write(line)
            file.close()
            index().infoDialog(language(30304).encode("utf-8"), name)
        except:
            return

    def favourite_moveUp(self, data, name, url):
        try:
            index().container_refresh()
            file = open(data,'r')
            read = file.read()
            file.close()
            list = re.compile('(".+?)\n').findall(read)
            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"' % url in x][0]
            i = list.index(line)
            if i == 0 : return
            list[i], list[i-1] = list[i-1], list[i]
            file = open(data, 'w')
            for line in list: file.write('%s\n' % (line))
            file.close()
            index().infoDialog(language(30305).encode("utf-8"), name)
        except:
            return

    def favourite_moveDown(self, data, name, url):
        try:
            index().container_refresh()
            file = open(data,'r')
            read = file.read()
            file.close()
            list = re.compile('(".+?)\n').findall(read)
            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"' % url in x][0]
            i = list.index(line)
            if i+1 == len(list): return
            list[i], list[i+1] = list[i+1], list[i]
            file = open(data, 'w')
            for line in list: file.write('%s\n' % (line))
            file.close()
            index().infoDialog(language(30306).encode("utf-8"), name)
        except:
            return

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'Favourites.png', 'action': 'shows_favourites'})
        rootList.append({'name': 30502, 'image': 'Various.png', 'action': 'shows_various'})
        rootList.append({'name': 30503, 'image': 'Nickelodeon.png', 'action': 'shows_nickelodeon'})
        rootList.append({'name': 30504, 'image': 'Classics.png', 'action': 'shows_classics'})
        rootList.append({'name': 30505, 'image': 'Songs.png', 'action': 'shows_songs'})
        index().rootList(rootList)

class favourites:
    def __init__(self):
        self.list = []

    def shows(self):
        try:
            file = open(addonNickelodeon,'r')
            result = file.read()
            file.close()
            nickelodeon_result = common.parseDOM(result, "show")
        except:
            pass
        try:
            file = open(addonVarious,'r')
            result = file.read()
            file.close()
            various_result = common.parseDOM(result, "show")
        except:
            pass
        try:
            file = open(favData, 'r')
            read = file.read()
            file.close()
        except:
            return
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, imdb, url, image in match:
            try:
                if url.startswith(link().youtube_api):
                    fanart = None
                elif url.startswith(link().nickelodeon_base):
                    filter = [i for i in nickelodeon_result if url in common.replaceHTMLCodes(i)][0]
                    fanart = common.parseDOM(filter, "fanart")[0]
                    fanart = common.replaceHTMLCodes(fanart)
                else:
                    filter = [i for i in various_result if url in common.replaceHTMLCodes(i)][0]
                    fanart = common.parseDOM(filter, "fanart")[0]
                    fanart = common.replaceHTMLCodes(fanart)
            except:
                fanart = None
            meta = {'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': 'Greek', 'plot': ''}
            if not fanart == None: meta.update({'fanart': fanart})
            self.list.append(meta)

        index().showList(self.list)

class link:
    def __init__(self):
        self.nickelodeon_base = 'http://www.nickelodeon.gr'

        self.youtube_base = 'http://www.youtube.com'
        self.youtube_api = 'http://gdata.youtube.com'
        self.youtube_playlists = 'http://gdata.youtube.com/feeds/api/users/%s/playlists'
        self.youtube_playlist = 'http://gdata.youtube.com/feeds/api/playlists/%s'
        self.youtube_search = 'http://gdata.youtube.com/feeds/api/videos?q='
        self.youtube_watch = 'http://www.youtube.com/watch?v=%s'
        self.youtube_info = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'

class shows:
    def __init__(self):
        self.list = []

    def nickelodeon(self):
        self.list = showList().data_list(addonNickelodeon)
        index().showList(self.list)

    def various(self):
        self.list = showList().data_list(addonVarious)
        index().showList(self.list)

    def classics(self):
        #self.list = showList().youtubedata_list(addonClassics)
        self.list = cache(showList().youtubedata_list, addonClassics)
        index().showList(self.list)

    def songs(self):
        #self.list = showList().youtubedata_list(addonSongs)
        self.list = cache(showList().youtubedata_list, addonSongs)
        index().showList(self.list)

class showList:
    def __init__(self):
        self.list = []
        self.data = []

    def data_list(self, file):
        try:
            file = open(file,'r')
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
                image = common.parseDOM(show, "poster")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                fanart = common.parseDOM(show, "fanart")[0]
                fanart = common.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'fanart': fanart, 'imdb': '0', 'genre': 'Greek', 'plot': ''})
            except:
                pass

        return self.list

    def youtubedata_list(self, file):
        try:
            file = open(file,'r')
            result = file.read()
            file.close()
            shows = common.parseDOM(result, "channel")
        except:
            return

        for show in shows:
            try:
                url = common.parseDOM(show, "url")[0]
                channel = url.split("/")[-1]
                self.youtube_list(channel, [])
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
                    includes[i] = link().youtube_playlist % includes[i].split("list=")[-1]
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
                    excludes[i] = link().youtube_playlist % excludes[i].split("list=")[-1]
                x = [i for i in self.list if not i['url'] in excludes]
                self.list = x
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('name'))
        return self.list

    def youtube_list(self, channel, filter):
        try:
            count = 0
            threads = []
            result = ''
            for i in range(1, 250, 25):
                self.data.append('')
                showsUrl = link().youtube_playlists % channel + '?max-results=25&start-index=%s' % str(i)
                threads.append(Thread(self.thread, showsUrl, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            shows = common.parseDOM(result, "entry")
        except:
            return
        for show in shows:
            try:
                name = common.parseDOM(show, "title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(show, "id")[0]
                url = link().youtube_playlist % url.split("/")[-1]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(show, "media:thumbnail", ret="url")[0]
                image = image.replace(image.split("/")[-1], '0.jpg')
                image = image.encode('utf-8')
                if image.endswith("/00000000000/0.jpg"): raise Exception() #empty playlist
                if any(url.endswith(i) for i in filter): raise Exception()
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': '0', 'genre': 'Greek', 'plot': '', 'channel': channel})
            except:
                pass

        return self.list

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class episodeList:
    def __init__(self):
        self.list = []
        self.data = []

    def get(self, name, url, image, imdb, genre, plot, show):
        if url.startswith(link().youtube_api):
            self.list = self.youtube_list(name, url, image, imdb, genre, plot, show)
        elif url.startswith(link().nickelodeon_base):
            self.list = self.nickelodeon_list(name, url, image, imdb, genre, plot, show)
        else:
            self.list = self.various_list(name, url, image, imdb, genre, plot, show)
        index().episodeList(self.list)


    def various_list(self, name, url, image, imdb, genre, plot, show):
        try:
            file = open(addonVarious,'r')
            result = file.read()
            file.close()
            result = common.parseDOM(result, "show")
            filter = [i for i in result if url in common.replaceHTMLCodes(i)][0]
            episodes = common.parseDOM(filter, "episode")
            image = common.parseDOM(filter, "fanart")[0]
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
                size = common.parseDOM(episode, "size")[0]
                size = common.replaceHTMLCodes(size)
                size = size.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'fanart': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'season': '1', 'episode': '1', 'size': size})
            except:
                pass

        return self.list

    def nickelodeon_list(self, name, url, image, imdb, genre, plot, show):
        try:
            file = open(addonNickelodeon,'r')
            result = file.read()
            file.close()
            result = common.parseDOM(result, "show")
            filter = [i for i in result if url in common.replaceHTMLCodes(i)][0]
            image = common.parseDOM(filter, "fanart")[0]
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
        except:
            pass
        try:
            count = 0
            threads = []
            result = ''
            for i in range(0, 75, 15):
                self.data.append('')
                episodesUrl = url + '?start=%s' % str(i)
                threads.append(Thread(self.thread, episodesUrl, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "div", attrs = { "class": "catItemImageBlock" })
            if episodes == []:
                result = getUrl(url).result
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
                url = '%s%s' % (link().nickelodeon_base, url)
                url = url.encode('utf-8')
                for i in self.list:
                    if name == i['name']: raise Exception()
                self.list.append({'name': name, 'url': url, 'image': image, 'fanart': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'season': '1', 'episode': '1', 'sort': sort})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        return self.list

    def youtube_list(self, name, url, image, imdb, genre, plot, show):
        try:
            count = 0
            threads = []
            result = ''
            for i in range(1, 250, 25):
                self.data.append('')
                episodesUrl = url + '?max-results=25&start-index=%s' % str(i)
                threads.append(Thread(self.thread, episodesUrl, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "entry")
        except:
        	return
        for episode in episodes:
            try:
                name = common.parseDOM(episode, "title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "media:player", ret="url")[0]
                url = url.split("&amp;")[0].split("=")[-1]
                url = link().youtube_watch % url
                url = url.encode('utf-8')
                image = common.parseDOM(episode, "media:thumbnail", ret="url")[0]
                image = image.replace(image.split("/")[-1], '0.jpg')
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'season': '1', 'episode': '1'})
            except:
                pass

        return self.list


    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class resolver:
    def run(self, url, size, name=None, play=True):
        try:
            if player().status() is True: return

            if url.startswith(link().nickelodeon_base): url = self.nickelodeon(url)
            elif url.startswith(link().youtube_base): url = self.youtube(url)
            else: url = self.urlresolver(url)
            if url is None: raise Exception()

            if not size == '0':
                size_new = self.size(url)
                if not size == size_new: raise Exception()

            if play == False: return url
            player().run(name, url)
            return url
        except:
            index().infoDialog(language(30317).encode("utf-8"))
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

    def size(self, url):
        try:
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0')
            response = urllib2.urlopen(request, timeout=30)
            size = response.info()["Content-Length"]
            return size
        except:
            return

    def youtube(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30321).encode("utf-8"), language(30322).encode("utf-8"))
                return
            id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            state, reason = None, None
            result = getUrl(link().youtube_info % id).result
            try:
                state = common.parseDOM(result, "yt:state", ret="name")[0]
                reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
            except:
                pass
            if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return
            try:
                result = getUrl(link().youtube_watch % id).result
                alert = common.parseDOM(result, "div", attrs = { "id": "watch7-notification-area" })[0]
                return
            except:
                pass
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
            return url
        except:
            return

    def urlresolver(self, url):
        try:
            host = urlresolver.HostedMediaFile(url)
            if host: resolver = urlresolver.resolve(url)
            if not resolver == url: return resolver
        except:
            return


main()