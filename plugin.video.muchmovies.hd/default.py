# -*- coding: utf-8 -*-

'''
    Much Movies HD XBMC Addon
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
try:    import CommonFunctions
except: import commonfunctionsdummy as CommonFunctions
from metahandler import metahandlers
from metahandler import metacontainers


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
addonDownloads      = os.path.join(addonPath,'resources/art/Downloads.png')
addonPages          = os.path.join(addonPath,'resources/art/Pages.png')
addonNext           = os.path.join(addonPath,'resources/art/Next.png')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData            = os.path.join(dataPath,'views.cfg')
favData             = os.path.join(dataPath,'favourites.cfg')
metaget             = metahandlers.MetaData(preparezip=False)
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

        if action == None:                          root().get()
        elif action == 'item_play':                 contextMenu().item_play()
        elif action == 'item_random_play':          contextMenu().item_random_play()
        elif action == 'item_queue':                contextMenu().item_queue()
        elif action == 'favourite_add':             contextMenu().favourite_add(favData, name, url, image, imdb)
        elif action == 'favourite_from_search':     contextMenu().favourite_from_search(favData, name, url, image, imdb)
        elif action == 'favourite_delete':          contextMenu().favourite_delete(favData, name, url)
        elif action == 'favourite_moveUp':          contextMenu().favourite_moveUp(favData, name, url)
        elif action == 'favourite_moveDown':        contextMenu().favourite_moveDown(favData, name, url)
        elif action == 'playlist_open':             contextMenu().playlist_open()
        elif action == 'settings_open':             contextMenu().settings_open()
        elif action == 'addon_home':                contextMenu().addon_home()
        elif action == 'view_movies':               contextMenu().view('movies')
        elif action == 'trailer':                   contextMenu().trailer(url)
        elif action == 'download':                  contextMenu().download(name, url)
        elif action == 'library':                   contextMenu().library(name, url)
        elif action == 'movies':                    movies().muchmovies(url)
        elif action == 'movies_search':             movies().muchmovies_search(query)
        elif action == 'movies_favourites':         favourites().movies()
        elif action == 'pages_movies':              pages().muchmovies()
        elif action == 'genres_movies':             genres().muchmovies()
        elif action == 'play':                      player().run(url, name)

        if action is None: pass
        elif action.startswith('movies'):
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            index().container_view('movies', {'skin.confluence' : 500})
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

    def resolve_simple(self, url):
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

    def resolve(self, name, url):
        if not xbmc.getInfoLabel('ListItem.label') == '' :
            meta = {'label' : xbmc.getInfoLabel('ListItem.label'), 'title' : xbmc.getInfoLabel('ListItem.title'), 'year' : xbmc.getInfoLabel('ListItem.year'), 'imdb_id' : xbmc.getInfoLabel('ListItem.imdb_id'), 'tmdb_id' : xbmc.getInfoLabel('ListItem.tmdb_id'), 'writer' : xbmc.getInfoLabel('ListItem.writer'), 'director' : xbmc.getInfoLabel('ListItem.director'), 'tagline' : xbmc.getInfoLabel('ListItem.tagline'), 'cast' : xbmc.getInfoLabel('ListItem.cast'), 'rating' : xbmc.getInfoLabel('ListItem.rating'), 'votes' : xbmc.getInfoLabel('ListItem.votes'), 'duration' : xbmc.getInfoLabel('ListItem.duration'), 'plot' : xbmc.getInfoLabel('ListItem.plot'), 'mpaa' : xbmc.getInfoLabel('ListItem.mpaa'), 'premiered' : xbmc.getInfoLabel('ListItem.premiered'), 'trailer' : xbmc.getInfoLabel('ListItem.trailer_url'), 'genre' : xbmc.getInfoLabel('ListItem.genre'), 'studio' : xbmc.getInfoLabel('ListItem.studio')}
            if not xbmc.getInfoLabel('ListItem.tvshowtitle') == '' :
                meta.update({'tvshowtitle' : xbmc.getInfoLabel('ListItem.tvshowtitle'), 'season' : xbmc.getInfoLabel('ListItem.season'), 'episode' : xbmc.getInfoLabel('ListItem.episode')})
            poster = xbmc.getInfoLabel('ListItem.thumb')
        else:
            season, episode, year = None, None, None
            try: season = re.compile('S(\d{3})E\d*').findall(name)[-1]
            except: pass
            try: season = re.compile('S(\d{2})E\d*').findall(name)[-1]
            except: pass
            try: episode = re.compile('S%sE(\d*)' % (season)).findall(name)[-1]
            except: pass
            try: year = re.compile('[(](\d{4})[)]').findall(name)[-1]
            except: pass
            if not (season is None and episode is None):
            	show = name.replace('S%sE%s' % (season, episode), '').strip()
            	season, episode = '%01d' % int(season), '%01d' % int(episode)
            	imdb = metaget.get_meta('tvshow', show)['imdb_id']
            	imdb = re.sub("[^0-9]", "", imdb)
            	i = metaget.get_episode_meta('', imdb, season, episode)
            	meta = {'label' : i['title'], 'title' : i['title'], 'tvshowtitle': show, 'imdb_id' : i['imdb_id'], 'season' : i['season'], 'episode' : i['episode'], 'writer' : i['writer'], 'director' : i['director'], 'rating' : i['rating'], 'duration' : i['duration'], 'plot' : i['plot'], 'premiered' : i['premiered'], 'genre' : i['genre']}
            	poster = i['cover_url']
            elif not year is None:
            	title = name.replace('(%s)' % year, '').strip()
            	i = metaget.get_meta('movie', title ,year=year ,overlay=6)
            	meta = {'label' : i['title'], 'title' : i['title'], 'year' : i['year'], 'imdb_id' : i['imdb_id'], 'tmdb_id' : i['tmdb_id'], 'writer' : i['writer'], 'director' : i['director'], 'tagline' : i['tagline'], 'cast' : i['cast'], 'rating' : i['rating'], 'votes' : i['votes'], 'duration' : i['duration'], 'plot' : i['plot'], 'mpaa' : i['mpaa'], 'premiered' : i['premiered'], 'trailer' : i['trailer_url'], 'genre' : i['genre'], 'studio' : i['studio']}
            	poster = i['cover_url']
            else:
            	meta = {'label' : name, 'title' : name}
            	poster = ''

        item = xbmcgui.ListItem(path=url, iconImage="DefaultVideo.png", thumbnailImage=poster)
        item.setInfo( type="Video", infoLabels= meta )
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

    def rootList(self, rootList):
        total = len(rootList)
        for i in rootList:
            try:
                name = language(i['name']).encode("utf-8")
                image = '%s/%s' % (addonArt, i['image'])
                action = i['action']
                u = '%s?action=%s' % (sys.argv[0], action)

                cm = []
                if action == 'movies_favourites':
                    cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                    cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def pageList(self, pageList):
        total = len(pageList)
        for i in pageList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)

                if action.endswith('movies'):
                    u = '%s?action=movies&url=%s' % (sys.argv[0], sysurl)
                elif action.endswith('shows'):
                    u = '%s?action=shows&url=%s' % (sys.argv[0], sysurl)

                cm = []
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def nextList(self, next):
        if next == '': return
        name, url, image = language(30361).encode("utf-8"), next, addonNext
        sysurl = urllib.quote_plus(url)

        if action.startswith('movies'):
            u = '%s?action=movies&url=%s' % (sys.argv[0], sysurl)
        elif action.startswith('shows'):
            u = '%s?action=shows&url=%s' % (sys.argv[0], sysurl)

        cm = []
        cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
        cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
        cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

        item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems(cm, replaceItems=True)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def downloadList(self):
        u = getSetting("downloads")
        if u == '': return
        name, image = language(30363).encode("utf-8"), addonDownloads

        cm = []
        cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
        cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
        cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

        item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems(cm, replaceItems=True)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def movieList(self, movieList):
        file = open(favData,'r')
        favRead = file.read()
        file.close()

        total = len(movieList)
        for i in movieList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                try: imdb = i['imdb']
                except: imdb = ''
                try: genre = i['genre']
                except: genre = ''
                try: plot = i['plot']
                except: plot = addonDesc
                try: year = re.compile('[(](\d{4})[)]').findall(name)[-1]
                except: year = ""
                title = name.replace('(%s)' % year, '').strip()

                sysname, sysimdb, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(imdb), urllib.quote_plus(url), urllib.quote_plus(image)
                u = '%s?action=play&name=%s&url=%s' % (sys.argv[0], sysname, sysurl)

                if getSetting("meta") == 'true':
                    #i = metaget.get_meta('movie', title ,imdb_id=imdb ,year=year ,overlay=6)
                    i = metaget.get_meta('movie', title ,year=year ,overlay=6)
                    meta = {'label' : i['title'], 'title' : i['title'], 'year' : i['year'], 'imdb_id' : i['imdb_id'], 'tmdb_id' : i['tmdb_id'], 'writer' : i['writer'], 'director' : i['director'], 'tagline' : i['tagline'], 'cast' : i['cast'], 'rating' : i['rating'], 'votes' : i['votes'], 'duration' : i['duration'], 'plot' : i['plot'], 'mpaa' : i['mpaa'], 'premiered' : i['premiered'], 'trailer' : i['trailer_url'], 'genre' : i['genre'], 'studio' : i['studio']}
                    trailer, poster = urllib.quote_plus(i['trailer_url']), i['cover_url']
                    if trailer == '': trailer = sysurl
                    if poster == '': poster = image
                else:
                    meta = {'label': title, 'title': title, 'year': year, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                    trailer, poster = sysurl, image
                if getSetting("meta") == 'true' and getSetting("fanart") == 'true':
                    fanart = i['backdrop_url']
                    if fanart == '': fanart = addonFanart
                else:
                    fanart = addonFanart

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=download&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                if getSetting("meta") == 'true': cm.append((language(30409).encode("utf-8"), 'Action(Info)'))
                if action == 'movies_favourites':
                    cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=library&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                elif action == 'movies_search':
                    cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=trailer&url=%s)' % (sys.argv[0], trailer)))
                    cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=library&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=favourite_from_search&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                else:
                    cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=trailer&url=%s)' % (sys.argv[0], trailer)))
                    cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=library&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if not '"%s"' % url in favRead: cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    else: cm.append((language(30414).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels= meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("art(poster)", poster)
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
            if imdb == '': imdb = '0'
            index().container_refresh()
            file = open(data, 'a+')
            #file.write('"%s"|"%s"|"%s"|"%s"\n' % (name, imdb, url, image))
            file.write('"%s"|"%s"|"%s"\n' % (name, url, image))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_from_search(self, data, name, url, image, imdb):
        try:
            if imdb == '': imdb = '0'
            file = open(data,'r')
            read = file.read()
            file.close()
            if url in read:
                index().infoDialog(language(30307).encode("utf-8"), name)
                return
            file = open(data, 'a+')
            #file.write('"%s"|"%s"|"%s"|"%s"\n' % (name, imdb, url, image))
            file.write('"%s"|"%s"|"%s"\n' % (name, url, image))
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

    def trailer(self, url):
        url = player().trailer(url)
        if url is None: return
        item = xbmcgui.ListItem(path=url)
        item.setProperty("IsPlayable", "true")
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist.add(url,item)
        xbmc.Player().play(playlist)

    def download(self, name, url):
        try:
            download = getSetting("downloads")
            download = xbmc.translatePath(download)
            if download == '':
            	yes = index().yesnoDialog(language(30341).encode("utf-8"), language(30342).encode("utf-8"))
            	if yes: contextMenu().settings_open()
            	return
            try: os.makedirs(dataPath)
            except: pass
            try: os.makedirs(download)
            except: pass

            property = (addonName+name).replace(' ','').lower()
            url = player().muchmovies(url)
            if url is None: return
            ext = os.path.splitext(url)[1][1:].strip().lower()
            enc_name = name.translate(None, '\/:*?"<>|')
            stream = os.path.join(download, enc_name + '.' + ext)
            temp = stream + '.tmp'

            if os.path.isfile(stream) == True:
            	yes = index().yesnoDialog(language(30343).encode("utf-8"), language(30344).encode("utf-8"), name)
            	if yes:
            	    try: os.remove(stream)
            	    except: pass
            	    try: os.remove(temp)
            	    except: pass
            	else:
            	    return
            if os.path.isfile(temp) == True:
            	if index().getProperty(property) == 'open':
            	    yes = index().yesnoDialog(language(30345).encode("utf-8"), language(30346).encode("utf-8"), name)
            	    if yes: index().setProperty(property, 'cancel')
            	    return
            	else:
            	    try: os.remove(temp)
            	    except: pass

            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
            response = urllib2.urlopen(request, timeout=10)
            with open(temp, 'wb') as data:
            	count = 0
            	CHUNK = 16 * 1024
            	size = response.info()["Content-Length"]
            	index().setProperty(property, 'open')
            	index().infoDialog(language(30308).encode("utf-8"), name)
            	while True:
            		chunk = response.read(CHUNK)
            		if not chunk: break
            		if index().getProperty(property) == 'cancel': raise Exception()
            		if xbmc.abortRequested == True: raise Exception()
            		quota = int(100 * float(os.path.getsize(temp))/float(size))
            		if not count == quota and count in [0,10,20,30,40,50,60,70,80,90]:
            		    index().infoDialog(language(30309).encode("utf-8") + str(count) + '%', name)
            		data.write(chunk)
            		count = quota

            response.close()
            data.close()
            os.rename(temp, stream)
            index().infoDialog(language(30310).encode("utf-8"), name)
            index().clearProperty(property)
        except:
            data.close()
            index().clearProperty(property)
            try: os.remove(temp)
            except: pass
            sys.exit()
            return

    def library(self, name, url, silent=False):
        try:
            library = getSetting("movie_library")
            library = xbmc.translatePath(library)
            sysname, sysurl = urllib.quote_plus(name), urllib.quote_plus(url)
            content = '%s?action=play&name=%s&url=%s' % (sys.argv[0], sysname, sysurl)
            enc_name = name.translate(None, '\/:*?"<>|')
            folder = os.path.join(library, enc_name)
            stream = os.path.join(folder, enc_name + '.strm')
            try: os.makedirs(dataPath)
            except: pass
            try: os.makedirs(library)
            except: pass
            try: os.makedirs(folder)
            except: pass
            file = open(stream, 'w')
            file.write(content)
            file.close()
            if silent == False:
                index().infoDialog(language(30311).encode("utf-8"), name)
        except:
            return

class subtitles:
    def get(self, name):
        subs = getSetting("subs")
        if subs == '1': self.greek(name)

    def greek(self, name):
        try:
            import shutil, zipfile, time
            sub_tmp = os.path.join(dataPath,'sub_tmp')
            sub_tmp2 = os.path.join(sub_tmp, "subs")
            sub_stream = os.path.join(dataPath,'sub_stream')
            sub_file = os.path.join(sub_tmp, 'sub_tmp.zip')
            try: os.makedirs(dataPath)
            except: pass
            try: shutil.rmtree(sub_tmp)
            except: pass
            try: os.makedirs(sub_tmp)
            except: pass
            try: shutil.rmtree(sub_stream)
            except: pass
            try: os.makedirs(sub_stream)
            except: pass

            subtitles = []
            query = ''.join(e for e in name if e.isalnum() or e == ' ')
            query = urllib.quote_plus(query)
            url = 'http://www.greeksubtitles.info/search.php?name=' + query
            result = getUrl(url).result
            result = result.decode('iso-8859-7').encode('utf-8')
            result = result.lower().replace('"',"'")
            match = "get_greek_subtitles[.]php[?]id=(.+?)'.+?%s.+?<"
            quality = ['bluray', 'brrip', 'bdrip', 'dvdrip', 'hdtv']
            for q in quality:
                subtitles += re.compile(match % q).findall(result)
            if subtitles == []: raise Exception()
            for subtitle in subtitles:
                url = 'http://www.findsubtitles.eu/getp.php?id=' + subtitle
                response = urllib.urlopen(url)
                content = response.read()
                response.close()
                if content[:4] == 'PK': break

            file = open(sub_file, 'wb')
            file.write(content)
            file.close()
            file = zipfile.ZipFile(sub_file, 'r')
            file.extractall(sub_tmp)
            file.close()
            files = os.listdir(sub_tmp2)
            if files == []: raise Exception()
            file = [i for i in files if i.endswith('.srt') or i.endswith('.sub')]
            if file == []:
                pack = [i for i in files if i.endswith('.zip') or i.endswith('.rar')]
                pack = os.path.join(sub_tmp2, pack[0])
                xbmc.executebuiltin('Extract("%s","%s")' % (pack, sub_tmp2))
                time.sleep(1)
            files = os.listdir(sub_tmp2)
            file = [i for i in files if i.endswith('.srt') or i.endswith('.sub')][0]
            copy = os.path.join(sub_tmp2, file)
            shutil.copy(copy, sub_stream)
            try: shutil.rmtree(sub_tmp)
            except: pass
            file = os.path.join(sub_stream, file)
            if not os.path.isfile(file): raise Exception()

            xbmc.Player().setSubtitles(file)
        except:
            try: shutil.rmtree(sub_tmp)
            except: pass
            try: shutil.rmtree(sub_stream)
            except: pass
            index().infoDialog(language(30316).encode("utf-8"), name)
            return

class favourites:
    def __init__(self):
        self.list = []

    def movies(self):
        file = open(favData, 'r')
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, url, image in match:
            self.list.append({'name': name, 'url': url, 'image': image})
        index().movieList(self.list)

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'Favourites.png', 'action': 'movies_favourites'})
        rootList.append({'name': 30502, 'image': 'Listings.png', 'action': 'movies'})
        rootList.append({'name': 30503, 'image': 'Genres.png', 'action': 'genres_movies'})
        rootList.append({'name': 30504, 'image': 'Pages.png', 'action': 'pages_movies'})
        rootList.append({'name': 30505, 'image': 'Search.png', 'action': 'movies_search'})
        index().rootList(rootList)
        index().downloadList()

class link:
    def __init__(self):
        self.muchmovies_base = 'http://www.muchmovies.org'
        self.muchmovies_sort = 'http://www.muchmovies.org/session/sort'
        self.muchmovies_root = 'http://www.muchmovies.org/movies'
        self.muchmovies_search = 'http://www.muchmovies.org/search'
        self.muchmovies_genre = 'http://www.muchmovies.org/genres'
        self.youtube_base = 'http://www.youtube.com'
        self.youtube_info = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'

class pages:
    def __init__(self):
        self.list = []

    def muchmovies(self):
        self.list = self.muchmovies_list()
        index().pageList(self.list)

    def muchmovies_list(self):
        try:
            result = getUrl(link().muchmovies_root, mobile=True).result
            pages = common.parseDOM(result, "div", attrs = { "class": "pagenav" })[0]
            pages = re.compile('(<option.+?</option>)').findall(pages)
        except:
            return
        for page in pages:
            try:
                name = common.parseDOM(page, "option")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(page, "option", ret="value")[0]
                url = '%s%s' % (link().muchmovies_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = addonPages.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class genres:
    def __init__(self):
        self.list = []

    def muchmovies(self):
        self.list = self.muchmovies_list()
        index().pageList(self.list)

    def muchmovies_list(self):
        try:
            result = getUrl(link().muchmovies_genre, mobile=True).result
            genres = common.parseDOM(result, "ul", attrs = { "id": "genres" })
            genres = common.parseDOM(genres, "li")
        except:
            return
        for genre in genres:
            try:
                name = common.parseDOM(genre, "h2")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(genre, "a", ret="href")[0]
                url = '%s%s' % (link().muchmovies_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(genre, "img", ret="src")[0]
                image = '%s%s' % (link().muchmovies_base, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class movies:
    def __init__(self):
        self.list = []
        self.next = ''

    def muchmovies_search(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query is None or self.query == ''):
            self.query = link().muchmovies_search + '/' + urllib.quote_plus(self.query.replace(' ', '-'))
            self.list = self.muchmovies_list(self.query, '')
            index().movieList(self.list)
            index().nextList(self.next)

    def muchmovies(self, url=None):
        self.sort = getSetting("sortby")
        if self.sort == '1':
            post = 'sort_by=release'
        elif self.sort == '2':
            post = 'sort_by=title'
        elif self.sort == '3':
            post = 'sort_by=rating'
        else:
            post = 'sort_by=date_added'
        self.list = self.muchmovies_list(url, post)
        index().movieList(self.list)
        index().nextList(self.next)

    def muchmovies_list(self, url, post):
        try:
            if url is None: url = link().muchmovies_root
            result = getUrl(link().muchmovies_sort, post=post, mobile=True, close=False, cookie=True).result
            result = getUrl(url, mobile=True).result
            movies = common.parseDOM(result, "li", attrs = { "data-icon": "false" })
        except:
            return
        try:
            try:
                self.next = common.parseDOM(result, "a", ret="href", attrs = { "data-icon": "arrow-r", "class": "ui-disabled" })[0]
                self.next = ''
            except:
                self.next = common.parseDOM(result, "a", ret="href", attrs = { "data-icon": "arrow-r" })[0]
                self.next = '%s%s' % (link().muchmovies_base, self.next)
        except:
            pass
        for movie in movies:
            try:
                name = common.parseDOM(movie, "h2")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(movie, "a", ret="href")[0]
                url = '%s%s' % (link().muchmovies_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(movie, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class player:
    def run(self, url, name=None):
        url = self.muchmovies(url)
        if url is None: return
        index().resolve(name, url)
        subtitles().get(name)
        return url

    def trailer(self, url):
        try:
            if url.startswith(link().youtube_base):
                url = self.youtube(url)
            else:
                result = getUrl(url).result
                url = re.compile('"http://www.youtube.com/embed/(.+?)"').findall(result)[0]
                url = url.split("?")[0]
                url = 'http://www.youtube.com/watch?v=%s' % url
                url = self.youtube(url)
            if url is None: return
            return url
        except:
            return

    def muchmovies(self, url):
        try:
            result = getUrl(url, mobile=True).result
            url = common.parseDOM(result, "a", ret="href")
            url = [i for i in url if "?action=stream" in i][0]
            url = url.split("?")[0]
            return url
        except:
            return

    def youtube(self, url):
        try:
            id = url.split("?v=")[-1]
            state, reason = None, None
            result = getUrl(link().youtube_info % id).result
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
                index().okDialog(language(30321).encode("utf-8"), language(30322).encode("utf-8"))
                return
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
            return url
        except:
            return

main()