# -*- coding: utf-8 -*-

'''
    Hellenic Player XBMC Addon
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
try:    import json
except: import simplejson as json
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
addonNickelodeon    = os.path.join(addonPath,'resources/data/nickelodeon.xml')
addonSkaiDoc        = os.path.join(addonPath,'resources/data/skaidoc.xml')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData            = os.path.join(dataPath,'views.cfg')
favData             = os.path.join(dataPath,'favourites.cfg')
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

        if action == None:                          root().get()
        elif action == 'item_live':                 item().live()
        elif action == 'root_shows':                root().shows()
        elif action == 'root_archive':              root().archives()
        elif action == 'root_news':                 root().news()
        elif action == 'root_sports':               root().sports()
        elif action == 'root_music':                root().music()
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
        elif action == 'view_archives':             contextMenu().view('archives')
        elif action == 'view_tvshows':              contextMenu().view('tvshows')
        elif action == 'view_episodes':             contextMenu().view('videos')
        elif action == 'shows_mega':                shows().megatv()
        elif action == 'shows_ant1':                shows().antenna()
        elif action == 'shows_alpha':               shows().alphatv()
        elif action == 'shows_star':                shows().star()
        elif action == 'shows_skai':                shows().skai()
        elif action == 'shows_madtv':               shows().madtv()
        elif action == 'shows_nickelodeon':         shows().nickelodeon()
        elif action == 'shows_skaidoc':             shows().skaidoc()
        elif action == 'archives_mega':             archives().megatv()
        elif action == 'archives_ant1':             archives().antenna()
        elif action == 'archives_alpha':            archives().alphatv()
        elif action == 'archives_star':             archives().star()
        elif action == 'archives_ert':              archives().ert()
        elif action == 'archives_rik':              archives().rik()
        elif action == 'archives_favourites':       favourites().archives()
        elif action == 'episodes_meganews':         news().megatv()
        elif action == 'episodes_ant1news':         news().antenna()
        elif action == 'episodes_alphanews':        news().alphatv()
        elif action == 'episodes_starnews':         news().star()
        elif action == 'episodes_skainews':         news().skai()
        elif action == 'episodes_enikosnews':       news().enikos()
        elif action == 'episodes_megasports':       sports().megatv()
        elif action == 'episodes_ant1sports':       sports().antenna()
        elif action == 'episodes_greeksuperleague': sports().greeksuperleague()
        elif action == 'episodes_novasports':       sports().novasports()
        elif action == 'episodes_novasportsnews':   sports().novasportsnews()
        elif action == 'episodes_madgreekzmusic':   music().madgreekz()
        elif action == 'episodes_madtop50':         music().madtop50()
        elif action == 'episodes_itunesgr':         music().itunesgr()
        elif action == 'episodes_uschart':          music().uschart()
        elif action == 'episodes_itunesus':         music().itunesus()
        elif action == 'episodes_ukchart':          music().ukchart()
        elif action == 'episodes_itunesuk':         music().itunesuk()
        elif action == 'episodes':                  episodeList().get(name, url, image, imdb, genre, plot, show)
        elif action == 'play':                      resolver().run(url, name)

        if action is None or action.startswith('root'):
            index().container_view('root', {'skin.confluence' : 500})
        elif action.startswith('archives'):
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            index().container_view('archives', {'skin.confluence' : 500})
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
        item = xbmcgui.ListItem(path=url)
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
                cm.append((language(30427).encode("utf-8"), 'RunPlugin(%s?action=view_root)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels = {'label': name, 'title': name, 'plot': addonDesc} )
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def itemList(self, itemList):
        total = len(itemList)
        for i in itemList:
            try:
                name = language(i['name']).encode("utf-8")
                image = '%s/%s' % (addonArt, i['image'])
                action = i['action']
                u = '%s?action=%s' % (sys.argv[0], action)

                cm = []
                cm.append((language(30427).encode("utf-8"), 'RunPlugin(%s?action=view_root)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels = {'label': name, 'title': name, 'plot': addonDesc} )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
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
                if action == 'archives_favourites':
                    cm.append((language(30432).encode("utf-8"), 'RunPlugin(%s?action=view_archives)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30419).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30420).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30421).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                elif action.startswith('archives'):
                    if not '"%s"' % url in favRead: cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    else: cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30432).encode("utf-8"), 'RunPlugin(%s?action=view_archives)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
                else:
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

                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)
                u = '%s?action=play&name=%s&url=%s' % (sys.argv[0], sysname, sysurl)
                if url.startswith(link().youtube_base) or url.startswith(link().youtube_search):
                    u = '%s?action=play&name=%s&url=%s&t=%s' % (sys.argv[0], sysname, sysurl, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
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
                cm.append((language(30433).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))
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
            #file.write('"%s"|"%s"|"%s"\n' % (name, url, image))
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
        index().itemList([{'name': 30501, 'image': 'Live.png', 'action': 'item_live'}])
        rootList.append({'name': 30502, 'image': 'Networks.png', 'action': 'root_shows'})
        rootList.append({'name': 30503, 'image': 'Archives.png', 'action': 'root_archive'})
        rootList.append({'name': 30504, 'image': 'Favourites.png', 'action': 'archives_favourites'})
        rootList.append({'name': 30505, 'image': 'News.png', 'action': 'root_news'})
        rootList.append({'name': 30506, 'image': 'Sports.png', 'action': 'root_sports'})
        rootList.append({'name': 30507, 'image': 'Music.png', 'action': 'root_music'})
        rootList.append({'name': 30508, 'image': 'Children.png', 'action': 'shows_nickelodeon'})
        rootList.append({'name': 30509, 'image': 'Documentaries.png', 'action': 'shows_skaidoc'})
        index().rootList(rootList)

    def shows(self):
        rootList = []
        rootList.append({'name': 30521, 'image': 'MEGA.png', 'action': 'shows_mega'})
        rootList.append({'name': 30522, 'image': 'ANT1.png', 'action': 'shows_ant1'})
        rootList.append({'name': 30523, 'image': 'ALPHA.png', 'action': 'shows_alpha'})
        rootList.append({'name': 30524, 'image': 'STAR.png', 'action': 'shows_star'})
        rootList.append({'name': 30525, 'image': 'SKAI.png', 'action': 'shows_skai'})
        rootList.append({'name': 30526, 'image': 'MAD TV.png', 'action': 'shows_madtv'})
        rootList.append({'name': 30527, 'image': 'NICKELODEON.png', 'action': 'shows_nickelodeon'})
        index().rootList(rootList)

    def archives(self):
        rootList = []
        rootList.append({'name': 30541, 'image': 'MEGA.png', 'action': 'archives_mega'})
        rootList.append({'name': 30542, 'image': 'ANT1.png', 'action': 'archives_ant1'})
        rootList.append({'name': 30543, 'image': 'ALPHA.png', 'action': 'archives_alpha'})
        rootList.append({'name': 30544, 'image': 'STAR.png', 'action': 'archives_star'})
        rootList.append({'name': 30545, 'image': 'ERT.png', 'action': 'archives_ert'})
        rootList.append({'name': 30546, 'image': 'RIK.png', 'action': 'archives_rik'})
        index().rootList(rootList)

    def news(self):
        rootList = []
        rootList.append({'name': 30561, 'image': 'MEGA.png', 'action': 'episodes_meganews'})
        rootList.append({'name': 30562, 'image': 'ANT1.png', 'action': 'episodes_ant1news'})
        rootList.append({'name': 30563, 'image': 'ALPHA.png', 'action': 'episodes_alphanews'})
        rootList.append({'name': 30564, 'image': 'STAR.png', 'action': 'episodes_starnews'})
        rootList.append({'name': 30565, 'image': 'SKAI.png', 'action': 'episodes_skainews'})
        rootList.append({'name': 30566, 'image': 'ENIKOS.png', 'action': 'episodes_enikosnews'})
        index().rootList(rootList)

    def sports(self):
        rootList = []
        rootList.append({'name': 30581, 'image': 'MEGA.png', 'action': 'episodes_megasports'})
        rootList.append({'name': 30582, 'image': 'ANT1.png', 'action': 'episodes_ant1sports'})
        rootList.append({'name': 30583, 'image': 'Super League.png', 'action': 'episodes_greeksuperleague'})
        rootList.append({'name': 30584, 'image': 'Novasports.png', 'action': 'episodes_novasports'})
        rootList.append({'name': 30585, 'image': 'Novasports.png', 'action': 'episodes_novasportsnews'})
        index().rootList(rootList)

    def music(self):
        rootList = []
        rootList.append({'name': 30601, 'image': 'MAD Greekz.png', 'action': 'episodes_madgreekzmusic'})
        rootList.append({'name': 30602, 'image': 'MAD Top 50.png', 'action': 'episodes_madtop50'})
        rootList.append({'name': 30603, 'image': 'iTunes GR Chart.png', 'action': 'episodes_itunesgr'})
        rootList.append({'name': 30604, 'image': 'US Chart.png', 'action': 'episodes_uschart'})
        rootList.append({'name': 30605, 'image': 'iTunes US Chart.png', 'action': 'episodes_itunesus'})
        rootList.append({'name': 30606, 'image': 'UK Chart.png', 'action': 'episodes_ukchart'})
        rootList.append({'name': 30607, 'image': 'iTunes UK Chart.png', 'action': 'episodes_itunesuk'})
        index().rootList(rootList)

class item:
    def live(self):
        if index().addon_status('plugin.video.hellenic.tv') is None:
            index().okDialog(language(30323).encode("utf-8"), language(30324).encode("utf-8"))
            return
        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.hellenic.tv/?action=dialog)')

class favourites:
    def __init__(self):
        self.list = []

    def archives(self):
        file = open(favData, 'r')
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, imdb, url, image in match:
            self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': 'Greek', 'plot': ''})
        index().showList(self.list)

class link:
    def __init__(self):
        self.megatv_base = 'http://www.megatv.com'
        self.megatv_feed = 'http://megatv.feed.gr'
        self.megatv_shows = 'http://megatv.feed.gr/mobile/mobile.asp?pageid=816&catidlocal=32623&subidlocal=20933'
        self.megatv_episodes = 'http://megatv.feed.gr/mobile/mobile/ekpompiindex_29954.asp?pageid=816&catidlocal=%s'
        self.megatv_news = 'http://www.megatv.com/webtv/default.asp?catid=27377&catidlocal=27377'
        self.megatv_sports = 'http://www.megatv.com/webtv/default.asp?catid=27377&catidlocal=27387'
        self.megatv_hls = 'http://hdflashmegatv-f.akamaihd.net'
        self.megatv_info = 'http://www.megatv.com/XML/jw/videolists.asp?catid=%s&attributes=0&nostore=true'

        self.antenna_base = 'http://www.antenna.gr'
        self.antenna_img = 'http://www.antenna.gr/imgHandler/326'
        self.antenna_shows = 'http://www.antenna.gr/tv/doubleip/shows?version=3.0'
        self.antenna_episodes = 'http://www.antenna.gr/tv/doubleip/show?version=3.0&sid='
        self.antenna_episodes2 = 'http://www.antenna.gr/tv/doubleip/categories?version=3.0&howmany=100&cid='
        self.antenna_news = 'http://www.antenna.gr/tv/doubleip/show?version=3.0&sid=222903'
        self.antenna_sports = 'http://www.antenna.gr/tv/doubleip/categories?version=3.0&howmany=100&cid=3062'
        self.antenna_watch = 'http://www.antenna.gr/webtv/watch?cid=%s'
        self.antenna_info = 'http://www.antenna.gr/webtv/templates/data/player?cid=%s'

        self.alphatv_base = 'http://www.alphatv.gr'
        self.alphatv_shows = 'http://www.alphatv.gr/shows'
        self.alphatv_shows2 = 'http://www.alphatv.gr/views/ajax?view_name=alpha_shows_category_view&view_display_id=page_3&view_path=shows&view_base_path=shows&page=%s'
        self.alphatv_news = 'http://www.alphatv.gr/shows/informative/news'

        self.star_base = 'http://www.star.gr'
        self.star_shows = 'http://www.star.gr/_layouts/handlers/tv/feeds.program.ashx?catTitle=hosts'
        self.star_episodes = 'http://www.star.gr/_layouts/handlers/tv/feeds.program.ashx?catTitle=%s&artId=%s'
        self.star_news = 'http://www.star.gr/_layouts/handlers/tv/feeds.program.ashx?catTitle=News&artId=9'
        self.star_watch = 'http://cdnapi.kaltura.com/p/21154092/sp/2115409200/playManifest/entryId/%s/flavorId/%s/format/url/protocol/http/a.mp4'

        self.skai_base = 'http://www.skai.gr'
        self.skai_shows = 'http://www.skai.gr/Ajax.aspx?m=Skai.TV.ProgramListView&la=0&Type=TV&Day=%s'
        self.skai_episodes = 'http://www.skai.gr/Ajax.aspx?m=Skai.Player.ItemView&type=TV&cid=6&alid=%s'
        self.skai_news = 'http://www.skai.gr/player/TV/?mmid=243980'

        self.nickelodeon_base = 'http://www.nickelodeon.gr'

        self.enikos_news = 'http://gdata.youtube.com/feeds/api/users/enikosgr/uploads'
        self.enikos_show = 'http://gdata.youtube.com/feeds/api/users/enikoslive/uploads'

        self.novasports_base = 'http://www.novasports.gr'
        self.novasports_episodes = 'http://www.novasports.gr/LiveWebTV.aspx%s'
        self.novasports_series = 'http://www.novasports.gr/handlers/LiveWebTv/LiveWebTvMediaGallery.ashx?containerid=-1&mediafiletypeid=0&latest=true&isBroadcast=true&tabid=shows'
        self.novasports_news = 'http://www.novasports.gr/handlers/LiveWebTv/LiveWebTvMediaGallery.ashx?containerid=-1&mediafiletypeid=2&latest=true&tabid=categories'

        self.madtv_base = 'http://www.mad.tv'
        self.madtv_charts = 'http://www.mad.tv/data/chart.php?service=chart&chid=NaN'
        self.madtv_chart = 'http://www.mad.tv/data/chart.php?service=chart&chid=%s'
        self.madtv_oldchart = 'http://www.mad.tv/data/chart.php?service=oldchart&chdt=%s'

        self.youtube_base = 'http://www.youtube.com'
        self.youtube_api = 'http://gdata.youtube.com'
        self.youtube_playlists = 'http://gdata.youtube.com/feeds/api/users/%s/playlists'
        self.youtube_playlist = 'http://gdata.youtube.com/feeds/api/playlists/%s'
        self.youtube_search = 'http://gdata.youtube.com/feeds/api/videos?q='
        self.youtube_watch = 'http://www.youtube.com/watch?v=%s'
        self.youtube_info = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'

        self.dailymotion_base = 'http://www.dailymotion.com'
        self.dailymotion_api = 'https://api.dailymotion.com'
        self.dailymotion_playlist = 'https://api.dailymotion.com/user/%s/videos?fields=description,duration,id,owner.username,taken_time,thumbnail_large_url,title,views_total&sort=recent&family_filter=1'
        self.dailymotion_watch = 'http://www.dailymotion.com/video/%s'
        self.dailymotion_info = 'http://www.dailymotion.com/embed/video/%s'

        self.cinegreece_base = 'http://www.cinegreece.com'
        self.cinegreece_mega = 'http://www.cinegreece.com/2012/05/mega.html'
        self.cinegreece_ant1 = 'http://www.cinegreece.com/2012/05/ant1.html'
        self.cinegreece_alpha = 'http://www.cinegreece.com/2012/05/alpha.html'
        self.cinegreece_star = 'http://www.cinegreece.com/2012/05/star.html'
        self.cinegreece_ert = 'http://www.cinegreece.com/2012/05/ert.html'
        self.cinegreece_rik = 'http://www.cinegreece.com/2012/05/rik.html'

class shows:
    def __init__(self):
        self.list = []

    def megatv(self):
        self.list = showList().megatv_list()
        #self.list = cache(showList().megatv_list)
        index().showList(self.list)

    def antenna(self):
        self.list = showList().antenna_list()
        #self.list = cache(showList().antenna_list)
        index().showList(self.list)

    def alphatv(self):
        self.list = showList().alphatv_list()
        #self.list = cache(showList().alphatv_list)
        index().showList(self.list)

    def star(self):
        self.list = showList().star_list()
        #self.list = cache(showList().star_list)
        index().showList(self.list)

    def skai(self):
        self.list = showList().skai_list()
        #self.list = cache(showList().skai_list)
        index().showList(self.list)

    def madtv(self):
        channel = 'MADTVGREECE'
        filter = ["PL1RY_6CEqdtnxJYgudDydiG4fKVoQouHf", "PL1RY_6CEqdtlu30q6SyuNe6Tk5IYjAiks", "PLE4B3F6B7F753D97C", "PL85C952EA930B9E90", "PL04B2C2D8B304BA48", "PL46B9D152167BA727"]
        self.list = showList().youtube_list(channel, filter)
        #self.list = cache(showList().youtube_list, channel, filter)
        index().showList(self.list)

    def nickelodeon(self):
        self.list = showList().data_list(addonNickelodeon)
        index().showList(self.list)

    def skaidoc(self):
        self.list = showList().data_list(addonSkaiDoc)
        index().showList(self.list)

class archives:
    def __init__(self):
        self.list = []

    def megatv(self):
        self.list = showList().cinegreece_list(link().cinegreece_mega)
        #self.list = cache(showList().cinegreece_list, link().cinegreece_mega)
        index().showList(self.list)

    def antenna(self):
        self.list = showList().cinegreece_list(link().cinegreece_ant1)
        #self.list = cache(showList().cinegreece_list, link().cinegreece_ant1)
        index().showList(self.list)

    def alphatv(self):
        self.list = showList().cinegreece_list(link().cinegreece_alpha)
        #self.list = cache(showList().cinegreece_list, link().cinegreece_alpha)
        index().showList(self.list)

    def star(self):
        self.list = showList().cinegreece_list(link().cinegreece_star)
        #self.list = cache(showList().cinegreece_list, link().cinegreece_star)
        index().showList(self.list)

    def ert(self):
        self.list = showList().cinegreece_list(link().cinegreece_ert)
        #self.list = cache(showList().cinegreece_list, link().cinegreece_ert)
        index().showList(self.list)

    def rik(self):
        self.list = showList().cinegreece_list(link().cinegreece_rik)
        #self.list = cache(showList().cinegreece_list, link().cinegreece_rik)
        index().showList(self.list)

class news:
    def __init__(self):
        self.list = []

    def megatv(self):
        name = 'MEGA GEGONOTA'
        url = link().megatv_news
        self.list = episodeList().megatv_list2(name, url, ' ', '0', 'Greek', '', name)
        index().episodeList(self.list)

    def antenna(self):
        name = 'ANT1 NEWS'
        url = link().antenna_news
        self.list = episodeList().antenna_list(name, url, ' ', '0', 'Greek', '', name)
        index().episodeList(self.list)

    def alphatv(self):
        name = 'ALPHA NEWS'
        url = link().alphatv_news
        self.list = episodeList().alphatv_list(name, url, ' ', '0', 'Greek', '', name)
        index().episodeList(self.list)

    def star(self):
        name = 'STAR NEWS'
        url = link().star_news
        image = 'http://www.star.gr/tv/PublishingImages/160913114342_2118.jpg'
        self.list = episodeList().star_list(name, url, image, '0', 'Greek', ' ', name)
        index().episodeList(self.list)

    def skai(self):
        name = 'SKAI NEWS'
        url = link().skai_news
        self.list = episodeList().skai_list(name, url, ' ', '0', 'Greek', '', name)
        index().episodeList(self.list)

    def enikos(self):
        name = 'ENIKOS'
        url = link().enikos_news
        self.list = episodeList().youtube_list(name, url, ' ', '0', 'Greek', '', name)
        index().episodeList(self.list[:100])

class sports:
    def __init__(self):
        self.list = []

    def megatv(self):
        name = 'MEGA SPORTS'
        url = link().megatv_sports
        self.list = episodeList().megatv_list2(name, url, ' ', '0', 'Greek', '', name)
        index().episodeList(self.list)

    def antenna(self):
        name = 'ANT1 SPORTS'
        url = link().antenna_sports
        self.list = episodeList().antenna_list(name, url, ' ', '0', 'Greek', '', name)
        index().episodeList(self.list)

    def greeksuperleague(self):
        name = 'Super League'
        channel = 'greeksuperleague'
        url = link().dailymotion_playlist % channel
        self.list = episodeList().dailymotion_list(name, url, ' ', '0', 'Greek', '', name)
        index().episodeList(self.list)

    def novasports(self):
        name = 'Novasports'
        url = link().novasports_series
        self.list = episodeList().novasports_list(name, url, ' ', '0', 'Greek', '', name)
        index().episodeList(self.list)

    def novasportsnews(self):
        name = 'Novasports News'
        url = link().novasports_news
        self.list = episodeList().novasports_list(name, url, ' ', '0', 'Greek', '', name)
        index().episodeList(self.list)

class music:
    def __init__(self):
        self.list = []

    def madgreekz(self):
        channel = 'madtvgreekz'
        filter = ["PL20iPi-qHKiz1wJCqvbvy5ffrtWT1VcVF", "PL20iPi-qHKiyWnRbBdnSF7RlDdAePiKzj", "PL20iPi-qHKiyZGlOs5DTElzAK_YNCDJn0", "PL20iPi-qHKiwyRhqqmOnbDvPSUgRzzxgq"]
        self.list = showList().youtube_list(channel, filter)
        #self.list = cache(showList().youtube_list, channel, filter)
        self.list = sorted(self.list, key=itemgetter('name'))
        index().showList(self.list)

    def madtop50(self):
        name = 'MAD Top 50'
        self.list = episodeList().madchart_list(name, ' ', ' ', '0', 'Greek', '', name)
        index().episodeList(self.list)

    def itunesgr(self):
        name = 'iTunes GR Chart'
        self.list = episodeList().madchart_list(name, ' ', ' ', '0', 'Greek', '', name)
        index().episodeList(self.list)

    def uschart(self):
        name = 'US Chart'
        self.list = episodeList().madchart_list(name, ' ', ' ', '0', 'Greek', '', name)
        index().episodeList(self.list)

    def itunesus(self):
        name = 'iTunes US Chart'
        self.list = episodeList().madchart_list(name, ' ', ' ', '0', 'Greek', '', name)
        index().episodeList(self.list)

    def ukchart(self):
        name = 'UK Chart'
        self.list = episodeList().madchart_list(name, ' ', ' ', '0', 'Greek', '', name)
        index().episodeList(self.list)

    def itunesuk(self):
        name = 'iTunes UK Chart'
        self.list = episodeList().madchart_list(name, ' ', ' ', '0', 'Greek', '', name)
        index().episodeList(self.list)

class showList:
    def __init__(self):
        self.list = []
        self.data = []

    def megatv_list(self):
        try:
            result = getUrl(link().megatv_shows, mobile=True).result
            shows = common.parseDOM(result, "li")
        except:
            return
        for show in shows:
            try:
                name = common.parseDOM(show, "h5")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(show, "a", ret="data-params")[0]
                tpl = common.parseDOM(show, "a", ret="data-tpl")[0]
                if tpl == 'ekpompiindex': url = link().megatv_episodes % url.split("catid=")[-1]
                elif tpl == 'gegonota_home': url = link().megatv_news
                else: raise Exception()
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(show, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': '0', 'genre': 'Greek', 'plot': ''})
            except:
                pass

        return self.list

    def antenna_list(self):
        try:
            result = getUrl(link().antenna_shows, mobile=True).result
            shows = re.compile('({.+?})').findall(result)
            self.list.append({'name': 'ANT1 NEWS', 'url': link().antenna_news, 'image': 'http://www.antenna.gr/imgHandler/326/5a7c9f1a-79b6-47e0-b8ac-304d4e84c591.jpg', 'imdb': '0', 'genre': 'Greek', 'plot': ''})
        except:
            return
        for show in shows:
            try:
                i = json.loads(show)
                name = i['teasertitle'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                image = i['webpath'].strip()
                image = '%s/%s' % (link().antenna_img, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                url = i['id'].strip()
                url = link().antenna_episodes + url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                try: plot = i['teasertext'].strip()
                except: plot = ' '
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': '0', 'genre': 'Greek', 'plot': plot})
            except:
                pass

        return self.list

    def alphatv_list(self):
        try:
            result = getUrl(link().alphatv_shows).result
            filter = common.parseDOM(result, "span", attrs = { "class": "field-content" })
            filter = common.parseDOM(filter, "a", ret="href")
            filter = uniqueList(filter).list

            threads = []
            result = ''
            for i in range(0, 5):
                self.data.append('')
                showsUrl = link().alphatv_shows2 % str(i)
                threads.append(Thread(self.thread, showsUrl, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += json.loads(i)[1]['data']

            shows = common.parseDOM(result, "li")
        except:
            return
        for show in shows:
            try:
                name = common.parseDOM(show, "span")[0]
                name = common.parseDOM(name, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(show, "a", ret="href")[0]
                if not any(url == i for i in filter): raise Exception()
                url = '%s%s' % (link().alphatv_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(show, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': '0', 'genre': 'Greek', 'plot': ''})
            except:
                pass

        return self.list

    def star_list(self):
        try:
            result = getUrl(link().star_shows, mobile=True).result
            result = json.loads(result)
            shows = result['hosts']
        except:
            return
        for show in shows:
            try:
                i = show
                name = i['Title'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                image = i['Image'].strip()
                image = '%s%s' % (link().star_base, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                id = i['ProgramId']
                cat = i['ProgramCat'].strip()
                url = link().star_episodes % (cat, id)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': '0', 'genre': 'Greek', 'plot': ' '})
            except:
                pass

        self.list.append({'name': 'STON ENIKO', 'url': link().enikos_show, 'image': '%s/STON ENIKO.jpg' % addonArt, 'imdb': '0', 'genre': 'Greek', 'plot': 'STON ENIKO'})

        return self.list

    def skai_list(self):
        try:
            url = []
            d = datetime.datetime.utcnow()
            for i in range(0, 7):
                url.append(link().skai_shows % d.strftime("%d.%m.%Y"))
                d = d - datetime.timedelta(hours=24)
            url = url[::-1]

            threads = []
            result = ''
            for i in range(0, 7):
                self.data.append('')
                showsUrl = url[i]
                threads.append(Thread(self.thread, showsUrl, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            shows = common.parseDOM(result, "Show", attrs = { "TVonly": "0" })
        except:
            return
        for show in shows:
            try:
                name = common.parseDOM(show, "Show")[0]
                name = name.split('[')[-1].split(']')[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(show, "Link")[0]
                url = url.split('[')[-1].split(']')[0]
                url = '%s%s' % (link().skai_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(show, "ShowImage")[0]
                image = image.split('[')[-1].split(']')[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                plot = common.parseDOM(show, "Description")[0]
                plot = plot.split('[')[-1].split(']')[0]
                plot = plot.replace('<br>','').replace('</br>','').replace('\n','').split('<')[0].strip()
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                if image in str(self.list): raise Exception()
                if not 'mmid=' in url: raise Exception()
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': '0', 'genre': 'Greek', 'plot': plot})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('name'))
        return self.list

    def cinegreece_list(self, url):
        try:
            showsUrl = [url]
            for i in range(2, 5): showsUrl.append(url.replace('.html', 'p%s.html' % str(i)))

            threads = []
            result = ''
            for i in range(0, 4):
                self.data.append('')
                threads.append(Thread(self.thread, showsUrl[i], i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for data in self.data:
                try: result += common.parseDOM(data, "div", attrs = { "itemprop": "articleBody" })[0]
                except: pass

            shows = re.compile('(<a.+?</a>)').findall(result)
        except:
            return
        for show in shows:
            try:
                name = common.parseDOM(show, "img", ret="title")[0]
                if name.endswith('(Ο)'.decode('iso-8859-7')): name = 'Ο '.decode('iso-8859-7') + name.replace('(Ο)'.decode('iso-8859-7'), '').strip()
                elif name.endswith('(Η)'.decode('iso-8859-7')): name = 'Η '.decode('iso-8859-7') + name.replace('(Η)'.decode('iso-8859-7'), '').strip()
                elif name.endswith('(Το)'.decode('iso-8859-7')): name = 'Το '.decode('iso-8859-7') + name.replace('(Το)'.decode('iso-8859-7'), '').strip()
                elif name.endswith('(Οι)'.decode('iso-8859-7')): name = 'Οι '.decode('iso-8859-7') + name.replace('(Οι)'.decode('iso-8859-7'), '').strip()
                elif name.endswith('(Τα)'.decode('iso-8859-7')): name = 'Τα '.decode('iso-8859-7') + name.replace('(Τα)'.decode('iso-8859-7'), '').strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(show, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.replace(url.split("/")[2], link().cinegreece_base.split("//")[-1])
                url = url.encode('utf-8')
                image = common.parseDOM(show, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': '0', 'genre': 'Greek', 'plot': ''})
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
        if url.startswith(link().megatv_feed):
            self.list = self.megatv_list(name, url, image, imdb, genre, plot, show)
        elif url.startswith(link().megatv_base):
            self.list = self.megatv_list2(name, url, image, imdb, genre, plot, show)
        elif url.startswith(link().antenna_base):
            self.list = self.antenna_list(name, url, image, imdb, genre, plot, show)
        elif url.startswith(link().alphatv_base):
            self.list = self.alphatv_list(name, url, image, imdb, genre, plot, show)
        elif url.startswith(link().star_base):
            self.list = self.star_list(name, url, image, imdb, genre, plot, show)
        elif url.startswith(link().skai_base):
            self.list = self.skai_list(name, url, image, imdb, genre, plot, show)
        elif url.startswith(link().nickelodeon_base):
            self.list = self.nickelodeon_list(name, url, image, imdb, genre, plot, show)
        elif url.startswith(link().cinegreece_base):
            self.list = self.cinegreece_list(name, url, image, imdb, genre, plot, show)
        elif url.startswith(link().novasports_base):
            self.list = self.novasports_list(name, url, image, imdb, genre, plot, show)
        elif url.startswith(link().madtv_base):
            self.list = self.madchart_list(name, url, image, imdb, genre, plot, show)
        elif url.startswith(link().youtube_api):
            self.list = self.youtube_list(name, url, image, imdb, genre, plot, show)
        elif url.startswith(link().dailymotion_api):
            self.list = self.dailymotion_list(name, url, image, imdb, genre, plot, show)
        index().episodeList(self.list)


    def megatv_list(self, name, url, image, imdb, genre, plot, show):
        try:
        	result = getUrl(url, mobile=True).result
        	result = common.parseDOM(result, "section", attrs = { "class": "ekpompes.+?" })[0]
        	episodes = common.parseDOM(result, "li")
        except:
        	return
        for episode in episodes:
        	try:
        	    name = common.parseDOM(episode, "h5")[0]
        	    name = common.replaceHTMLCodes(name)
        	    name = name.encode('utf-8')
        	    url = common.parseDOM(episode, "a", ret="data-vUrl")[0]
        	    url = common.replaceHTMLCodes(url)
        	    url = url.encode('utf-8')
        	    image = common.parseDOM(episode, "img", ret="src")[0]
        	    image = common.replaceHTMLCodes(image)
        	    image = image.encode('utf-8')
        	    self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'season': '1', 'episode': '1'})
        	except:
        	    pass

        return self.list

    def megatv_list2(self, name, url, image, imdb, genre, plot, show):
        try:
        	result = getUrl(url).result
        	result = result.decode('iso-8859-7').encode('utf-8')

        	v1 = '/megagegonota/'
        	match = re.search("addPrototypeElement[(]'.+?','REST','(.+?)','(.+?)'.+?[)]", result)
        	v2,v3 = match.groups()
        	redirect = '%s%s%s?%s' % (link().megatv_base, v1, v2, v3)

        	result = getUrl(redirect).result
        	result = result.decode('iso-8859-7').encode('utf-8')
        	result = common.parseDOM(result, "div", attrs = { "class": "rest" })[0]
        	episodes = common.parseDOM(result, "li")
        except:
        	return
        for episode in episodes:
        	try:
        	    name = common.parseDOM(episode, "a")[1]
        	    name = common.replaceHTMLCodes(name)
        	    name = name.encode('utf-8')
        	    url = common.parseDOM(episode, "a", ret="href")[0]
        	    url = url.split("catid=")[-1].replace("')",'')
        	    url = '%s/r.asp?catid=%s' % (link().megatv_base, url)
        	    url = common.replaceHTMLCodes(url)
        	    url = url.encode('utf-8')
        	    image = common.parseDOM(episode, "img", ret="src")[0]
        	    if not image.startswith('http://'):
        	        image = '%s%s%s' % (link().megatv_base, v1, image)
        	    image = common.replaceHTMLCodes(image)
        	    image = image.encode('utf-8')
        	    self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'season': '1', 'episode': '1'})
        	except:
        	    pass

        return self.list

    def antenna_list(self, name, url, image, imdb, genre, plot, show):
        try:
            result = getUrl(url, mobile=True).result

            if url.startswith(link().antenna_episodes):
                id = json.loads(result)
                id = id['feed']['show']['videolib']
                if url.endswith('sid=223077'): id = '3110'#EUROPA LEAGUE
                elif url.endswith('sid=318756'): id = '3246'#ΟΛΑ ΤΡΕΛΑ
            elif url.startswith(link().antenna_episodes2):
                id = ''

            if id == '':
                episodes = result.replace("'",'"').replace('"title"','"caption"').replace('"image"','"webpath"').replace('"trailer_contentid"','"contentid"')
                episodes = re.compile('({.+?})').findall(episodes)
            else:
                url = link().antenna_episodes2 + id
                episodes = getUrl(url, mobile=True).result
                episodes = re.compile('({.+?})').findall(episodes)
        except:
            return

        for episode in episodes:
            try:
                i = json.loads(episode)
                name = i['caption'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                image = i['webpath'].strip()
                image = '%s/%s' % (link().antenna_img, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                url = i['contentid'].strip()
                url = link().antenna_watch % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'season': '1', 'episode': '1'})
            except:
                pass

        return self.list

    def alphatv_list(self, name, url, image, imdb, genre, plot, show):
        try:
        	redirects = [url + '/webtv/shows?page=0', url + '/webtv/shows?page=1' , url + '/webtv/episodes?page=0', url + '/webtv/episodes?page=1', url + '/webtv/news?page=0', url + '/webtv/news?page=1']

        	count = 0
        	threads = []
        	result = ''
        	for redirect in redirects:
        	    self.data.append('')
        	    threads.append(Thread(self.thread, redirect, count))
        	    count = count + 1
        	[i.start() for i in threads]
        	[i.join() for i in threads]
        	for i in self.data: result += i

        	episodes = common.parseDOM(result, "div", attrs = { "class": "views-field.+?" })
        except:
        	return
        for episode in episodes:
        	try:
        	    name = common.parseDOM(episode, "img", ret="alt")[-1]
        	    if name == '': raise Exception()
        	    name = common.replaceHTMLCodes(name)
        	    name = name.encode('utf-8')
        	    url = common.parseDOM(episode, "a", ret="href")[-1]
        	    url = '%s%s' % (link().alphatv_base, url)
        	    url = common.replaceHTMLCodes(url)
        	    url = url.encode('utf-8')
        	    if url in str(self.list): raise Exception()
        	    image = common.parseDOM(episode, "img", ret="src")[-1]
        	    if not image.startswith('http://'): image = '%s%s' % (link().alphatv_base, image)
        	    image = common.replaceHTMLCodes(image)
        	    image = image.encode('utf-8')
        	    self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'season': '1', 'episode': '1'})
        	except:
        	    pass

        return self.list

    def star_list(self, name, url, image, imdb, genre, plot, show):
        try:
            result = getUrl(url, mobile=True).result
            result = json.loads(result)

            try: plot = result['programme']['StoryLinePlain'].strip()
            except: plot = ' '
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')

            episodes = result['videosprogram']
        except:
        	return
        for episode in episodes:
            try:
                i = episode
                name = i['Title'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = i['VideoID'].strip()
                url = link().star_watch % (url, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'season': '1', 'episode': '1'})
            except:
                pass

        return self.list

    def skai_list(self, name, url, image, imdb, genre, plot, show):
        try:
            result = getUrl(url).result
            url = common.parseDOM(result, "li", ret="id", attrs = { "class": "active_sub" })[0]

            threads = []
            result = ''
            for i in range(1, 3):
                self.data.append('')
                episodesUrl = link().skai_episodes % url + '&Page=%s' % str(i)
                threads.append(Thread(self.thread, episodesUrl, i-1))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "Item")
        except:
        	return
        for episode in episodes:
            try:
                title = common.parseDOM(episode, "Title")[0]
                title = title.split('[')[-1].split(']')[0]
                date = common.parseDOM(episode, "Date")[0]
                date = date.split('[')[-1].split(']')[0]
                date = date.split('T')[0]
                name = '%s (%s)' % (title, date)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "File")[0]
                url = url.split('[')[-1].split(']')[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(episode, "Photo1")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'season': '1', 'episode': '1'})
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

    def cinegreece_list(self, name, url, image, imdb, genre, plot, show):
        try:
            result = getUrl(url).result
            image = common.parseDOM(result, "a", attrs = { "imageanchor": ".+?" })[0]
            image = common.parseDOM(image, "img", ret="src")[0]
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
            episodes = re.compile('(<button.+?</button>)').findall(result)
            episodes = uniqueList(episodes).list
        except:
            return
        for episode in episodes:
            try:
                name = common.parseDOM(episode, "button")[0]
                try: name = common.parseDOM(name, "span")[0]
                except: pass
                if '#' in name: raise Exception()
                name = name.replace('&nbsp;&nbsp;&nbsp;','-').strip()
                name = 'Επεισόδιο '.decode('iso-8859-7') + name
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "button", ret="onclick")[0]
                url = re.compile("'(.+?)'").findall(url)[0]
                if url.startswith('popvid'):
                    url = common.parseDOM(result, "div", attrs = { "id": url })[0]
                    url = common.parseDOM(url, "embed", ret="src")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'season': '1', 'episode': '1'})
            except:
                pass

        return self.list

    def novasports_list(self, name, url, image, imdb, genre, plot, show):
        try:
            result = getUrl(url).result
            episodes = common.parseDOM(result, "li")
        except:
            return
        for episode in episodes:
            try:
                name = common.parseDOM(episode, "a", ret="title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "a", ret="href")[-1]
                url = link().novasports_episodes % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(episode, "img", ret="src")[-1]
                image = '%s/%s' % (link().novasports_base, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'season': '1', 'episode': '1'})
            except:
                pass

        return self.list

    def madchart_list(self, name, url, image, imdb, genre, plot, show):
        try:
            result = getUrl(link().madtv_charts).result
            result = '{' + result.split('{', 1)[1].rsplit('}', 1)[0] + '}'
            result = json.loads(result)
            result = result['chartmenu']

            url = [i['link'] for i in result if i['item'] == name][0]
            url = url.split('=')[-1]

            result = getUrl(link().madtv_chart % url).result
            result = '{' + result.split('{', 1)[1].rsplit('}', 1)[0] + '}'
            result = json.loads(result)
            result = result['oldcharts']

            links = []
            if len(str(result[0]['id'])) == 4:
                for i in result[:4]: links.append(link().madtv_chart % i['id'])
            else:
                links.append(link().madtv_chart % url)
                for i in result[:3]: links.append(link().madtv_oldchart % i['id'])

            count = 0
            threads = []
            for i in links:
                self.data.append('')
                threads.append(Thread(self.thread, i, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            result = []
            date = ''
            for i in self.data:
                i = '{' + i.split('{', 1)[1].rsplit('}', 1)[0] + '}'
                i = json.loads(i)
                i = i['chart']
                if date == '': date = i['to']
                i = i['songs']
                result += i

            episodes = result
            date = date.replace('/','-').replace('.','-')
            date = common.replaceHTMLCodes(date)
            date = date.encode('utf-8')
            image = '%s/%s_wide.png' % (addonArt, name)
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
        except:
            return
        for episode in episodes:
            try:
                name = '%s - %s' % (episode['artist'].strip(), episode['title'].strip())
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                show = episode['artist'].strip()
                show = common.replaceHTMLCodes(show)
                show = show.encode('utf-8')
                query = name.replace('=','').replace('&','').replace("'",'')
                url = link().youtube_search + query + ' official'
                url = common.replaceHTMLCodes(url)
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'season': '1', 'episode': '1', 'date': date})
            except:
                pass

        enumerate_list = [x for i,x in enumerate(self.list) if x not in self.list[i+1:]]
        self.list = enumerate_list
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

    def dailymotion_list(self, name, url, image, imdb, genre, plot, show):
        try:
            threads = []
            result = []
            for i in range(1, 3):
                self.data.append('')
                episodesUrl = url + '&limit=100&page=%s' % str(i)
                threads.append(Thread(self.thread, episodesUrl, i-1))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += json.loads(i)['list']

            episodes = result
        except:
        	return
        for episode in episodes:
            try:
                name = episode['title']
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = episode['id']
                url = link().dailymotion_watch % url
                url = url.encode('utf-8')
                image = episode['thumbnail_large_url']
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
    def __init__(self):
        self.data = []

    def run(self, url, name=None, play=True):
        try:
            if player().status() is True: return

            if url.startswith(link().megatv_hls): url = self.megatv_hls(url)
            elif url.startswith(link().megatv_base): url = self.megatv(url)
            elif url.startswith(link().antenna_base): url = self.antenna(url)
            elif url.startswith(link().alphatv_base): url = self.alphatv(url)
            elif url.startswith(link().nickelodeon_base): url = self.nickelodeon(url)
            elif url.startswith(link().novasports_base): url = self.novasports(url)
            elif url.startswith(link().youtube_search): url = self.youtube_search(url)
            elif url.startswith(link().youtube_base): url = self.youtube(url)
            elif url.startswith(link().dailymotion_base): url = self.dailymotion(url)
            if url is None: raise Exception()

            if play == False: return url
            player().run(name, url)
            return url
        except:
            index().infoDialog(language(30317).encode("utf-8"))
            return

    def megatv(self, url):
        try:
            url = url.split("catid=")[-1]
            url = link().megatv_info % url
            result = getUrl(url).result

            playpath = common.parseDOM(result, "location")[-1]
            try: rtmp = common.parseDOM(result, "meta", attrs = { "rel": "streamer" })[0]
            except: rtmp = ''

            if playpath.endswith("/manifest.f4m"):
                rtmp = 'rtmp://cp78455.edgefcs.net/ondemand/vod/'
                try: playpath = re.compile('.+?,.+?,(.+?),.csmil/manifest.f4m').findall(playpath)[0]
                except: playpath = re.compile('.+?,(.+?),.csmil/manifest.f4m').findall(playpath)[0]

            url = '%s%s timeout=10' % (rtmp, playpath)
            if not url.startswith('rtmp://'): url = '%s%s' % (rtmp, playpath)
            return url
        except:
            return

    def megatv_hls(self, url):
        try:
            rtmp = 'rtmp://cp78455.edgefcs.net/ondemand/vod/'
            playpath = url.replace(',', '')
            playpath = re.compile('/i/(.+?)[.]csmil').findall(playpath)[0]
            url = '%s%s timeout=10' % (rtmp, playpath)
            return url
        except:
            return

    def antenna(self, url):
        id = url.split("?")[-1].split("cid=")[-1].split("&")[0]
        dataUrl = link().antenna_info % id
        pageUrl = link().antenna_watch % id
        swfUrl = 'http://www.antenna.gr/webtv/images/fbplayer.swf'

        try:
            result = getUrl(dataUrl).result
            rtmp = common.parseDOM(result, "FMS")[0]
            playpath = common.parseDOM(result, "appStream")[0]
            if playpath.endswith('/GR.flv'): raise Exception()
            url = '%s playpath=%s pageUrl=%s swfUrl=%s swfVfy=true timeout=10' % (rtmp, playpath, pageUrl, swfUrl)
            if playpath.startswith('http://'): url = playpath
            return url
        except:
            pass

        try:
            proxies = self.proxynova()
            if proxies == []: raise Exception()

            count = 0
            threads = []
            result = ''
            for proxy in proxies:
                self.data.append('')
                threads.append(Thread(self.thread, dataUrl, proxy, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            rtmp = common.parseDOM(result, "FMS")[0]
            playpath = common.parseDOM(result, "appStream")[0]
            if playpath.endswith('/GR.flv'): raise Exception()
            url = '%s playpath=%s pageUrl=%s swfUrl=%s swfVfy=true timeout=10' % (rtmp, playpath, pageUrl, swfUrl)
            if playpath.startswith('http://'): url = playpath
            return url
        except:
            pass

    def alphatv(self, url):
        try:
            result = getUrl(url).result
            result = result.replace('\n','')

            try:
                url = re.compile("playlist:.+?file: '(.+?[.]m3u8)'").findall(result)[0]
                if "EXTM3U" in getUrl(url).result: return url
            except:
                pass

            url = re.compile('playlist:.+?"(rtmp[:].+?)"').findall(result)[0]
            url += ' timeout=10'
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

    def novasports(self, url):
        try:
            result = getUrl(url).result
            url = re.compile("type: 'html5'.+?'file': '(.+?)'").findall(result)[0]
            return url
        except:
            return

    def youtube_search(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30321).encode("utf-8"), language(30322).encode("utf-8"))
                return

            query = url.split("?q=")[-1].split("/")[-1].split("?")[0]
            url = url.replace(query, urllib.quote_plus(query))
            result = getUrl(url).result
            result = common.parseDOM(result, "entry")
            result = common.parseDOM(result, "id")

            for url in result[:5]:
                url = url.split("/")[-1]
                url = link().youtube_watch % url
                url = self.youtube(url)
                if not url is None: return url
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

    def dailymotion(self, url):
        try:
            id = url.split("/")[-1].split("?")[0]
            result = getUrl(link().dailymotion_info % id).result
            quality = None
            try: quality = re.compile('"stream_h264_ld_url":"(.+?)"').findall(result)[0]
            except: pass
            try: quality = re.compile('"stream_h264_url":"(.+?)"').findall(result)[0]
            except: pass
            try: quality = re.compile('"stream_h264_hq_url":"(.+?)"').findall(result)[0]
            except: pass
            try: quality = re.compile('"stream_h264_hd_url":"(.+?)"').findall(result)[0]
            except: pass
            try: quality = re.compile('"stream_h264_hd1080_url":"(.+?)"').findall(result)[0]
            except: pass
            url = urllib.unquote(quality).decode('utf-8').replace('\\/', '/')
            return url
        except:
            return

    def proxynova(self):
        try:
            proxyList = []
            url = 'http://www.proxynova.com/proxy-server-list/country-gr/'
            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            hosts = common.parseDOM(result, "tr")
        except:
            return proxyList
        for host in hosts:
            try:
                time = common.parseDOM(host, "time", attrs = { "class": "time-ago recent" })[0]
                ip = common.parseDOM(host, "span", attrs = { "class": "row_proxy_ip" })[0]
                ip = ip.split('(')[-1].split(')')[0].replace(' ','').replace('"','').replace('+','')
                ip = common.replaceHTMLCodes(ip)
                port = common.parseDOM(host, "a", attrs = { "href": ".+?" })[0]
                proxyList.append(ip+':'+port)
            except:
                pass

        return proxyList

    def thread(self, url, proxy, i):
        try:
            result = getUrl(url,proxy=proxy).result
            self.data[i] = result
        except:
            return


main()