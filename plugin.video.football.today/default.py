# -*- coding: utf-8 -*-

'''
    Football Today XBMC Addon
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
addonNext           = os.path.join(addonPath,'resources/art/Next.png')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData            = os.path.join(dataPath,'views.cfg')
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
        try:        show = urllib.unquote_plus(params["show"])
        except:     show = None
        try:        title = urllib.unquote_plus(params["title"])
        except:     title = None
        try:        date = urllib.unquote_plus(params["date"])
        except:     date = None
        try:        query = urllib.unquote_plus(params["query"])
        except:     query = None


        if action == None:                            root().get()
        elif action == 'item_play':                   contextMenu().item_play()
        elif action == 'item_random_play':            contextMenu().item_random_play()
        elif action == 'item_queue':                  contextMenu().item_queue()
        elif action == 'item_play_from_here':         contextMenu().item_play_from_here(url)
        elif action == 'playlist_open':               contextMenu().playlist_open()
        elif action == 'settings_open':               contextMenu().settings_open()
        elif action == 'addon_home':                  contextMenu().addon_home()
        elif action == 'view_home':                   contextMenu().view('home')
        elif action == 'view_episodes':               contextMenu().view('episodes')
        elif action == 'matches':                     episodes().livefootballvideo(show, url, mode=None)
        elif action == 'matches_all':                 episodes().livefootballvideo(show, url, mode='0')
        elif action == 'matches_premierleague':       episodes().livefootballvideo(show, url, mode='1')
        elif action == 'matches_laliga':              episodes().livefootballvideo(show, url, mode='2')
        elif action == 'matches_bundesliga':          episodes().livefootballvideo(show, url, mode='3')
        elif action == 'matches_seriea':              episodes().livefootballvideo(show, url, mode='4')
        elif action == 'matches_ligue1':              episodes().livefootballvideo(show, url, mode='5')
        elif action == 'matches_eredivisie':          episodes().livefootballvideo(show, url, mode='6')
        elif action == 'matches_primeiraliga':        episodes().livefootballvideo(show, url, mode='7')
        elif action == 'matches_uefachampionsleague': episodes().livefootballvideo(show, url, mode='8')
        elif action == 'matches_uefaeuropaleague':    episodes().livefootballvideo(show, url, mode='9')
        elif action == 'matches_copalibertadores':    episodes().livefootballvideo(show, url, mode='10')
        elif action == 'matches_parts':               episodes().livefootballvideo_parts(url, image, show, title, date)
        elif action == 'highlights':                  episodes().livefootballvideo_highlights(show, url, mode=None)
        elif action == 'highlights_all':              episodes().livefootballvideo_highlights(show, url, mode='0')
        elif action == 'highlights_parts':            episodes().livefootballvideo2_parts(url, image, show, title, date)
        elif action == 'search':                      episodes().livefootballvideo_search(query)
        elif action == 'play':                        player().run(url, name)

        if action is None:
            index().container_view('home', {'skin.confluence' : 500})
        elif action.startswith('matches') or action.startswith('highlights') or action == 'search':
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            index().container_view('episodes', {'skin.confluence' : 504})
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
        response = urllib2.urlopen(request, timeout=60)
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

    def resolve(self, url):
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

    def rootList(self, rootList):
        total = len(rootList)
        for i in rootList:
            try:
                name = language(i['name']).encode("utf-8")
                image = '%s/%s' % (addonArt, i['image'])
                action = i['action']
                sysshow, sysimage = urllib.quote_plus(name), urllib.quote_plus(image)
                u = '%s?action=%s&show=%s&image=%s' % (sys.argv[0], action, sysshow, sysimage)

                cm = []
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=view_home)' % (sys.argv[0])))
                cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def nextList(self, show, next):
        if next == '': return
        name, url, image = language(30361).encode("utf-8"), next, addonNext
        sysshow, sysurl = urllib.quote_plus(show), urllib.quote_plus(url)

        if action.startswith('matches'):
            u = '%s?action=matches&show=%s&url=%s' % (sys.argv[0], sysshow, sysurl)
        elif action.startswith('highlights'):
            u = '%s?action=highlights&show=%s&url=%s' % (sys.argv[0], sysshow, sysurl)

        cm = []
        cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
        cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
        cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

        item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems(cm, replaceItems=True)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def episodeList(self, episodeList):
        total = len(episodeList)
        for i in episodeList:
            try:
                name, url, image, title, show, date = i['name'], i['url'], i['image'], i['title'], i['show'], i['date']
                if image == '': image = addonFanart
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)
                systitle, sysshow, sysdate = urllib.quote_plus(title), urllib.quote_plus(show), urllib.quote_plus(date)

                if action.startswith('matches'):
                    u = '%s?action=matches_parts&url=%s&image=%s&show=%s&title=%s&date=%s' % (sys.argv[0], sysurl, sysimage, sysshow, systitle, sysdate)
                elif action.startswith('highlights'):
                    u = '%s?action=highlights_parts&url=%s&image=%s&show=%s&title=%s&date=%s' % (sys.argv[0], sysurl, sysimage, sysshow, systitle, sysdate)
                elif action == 'search' and '/fullmatch/' in url:
                    u = '%s?action=matches_parts&url=%s&image=%s&title=%s' % (sys.argv[0], sysurl, sysimage, systitle)
                elif action == 'search':
                    u = '%s?action=highlights_parts&url=%s&image=%s&title=%s' % (sys.argv[0], sysurl, sysimage, systitle)

                meta = {'label': title, 'title': title, 'tvshowtitle': show, 'premiered': date, 'genre' : '', 'plot': addonDesc}

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30427).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))
                cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels= meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def episodepartsList(self, episodeList):
        total = len(episodeList)
        for i in episodeList:
            try:
                name, url, image, title, show, date = i['name'], i['url'], i['image'], i['title'], i['show'], i['date']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)

                u = '%s?action=play&name=%s&url=%s' % (sys.argv[0], sysname, sysurl)
                meta = {'label': title, 'title': title, 'tvshowtitle': show, 'premiered': date, 'genre' : '', 'plot': addonDesc}

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_play_from_here&url=%s)' % (sys.argv[0], sysurl)))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30427).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))
                cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels= meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
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
        subtitles().get(name)

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

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'Matches.png', 'action': 'matches_all'})
        rootList.append({'name': 30502, 'image': 'Highlights.png', 'action': 'highlights_all'})
        rootList.append({'name': 30503, 'image': 'Search.png', 'action': 'search'})
        rootList.append({'name': 30504, 'image': 'Premier League.png', 'action': 'matches_premierleague'})
        rootList.append({'name': 30505, 'image': 'La Liga.png', 'action': 'matches_laliga'})
        rootList.append({'name': 30506, 'image': 'Bundesliga.png', 'action': 'matches_bundesliga'})
        rootList.append({'name': 30507, 'image': 'Serie A.png', 'action': 'matches_seriea'})
        rootList.append({'name': 30508, 'image': 'Ligue 1.png', 'action': 'matches_ligue1'})
        rootList.append({'name': 30509, 'image': 'Eredivisie.png', 'action': 'matches_eredivisie'})
        rootList.append({'name': 30510, 'image': 'Primeira Liga.png', 'action': 'matches_primeiraliga'})
        rootList.append({'name': 30511, 'image': 'UEFA Champions League.png', 'action': 'matches_uefachampionsleague'})
        rootList.append({'name': 30512, 'image': 'UEFA Europa League.png', 'action': 'matches_uefaeuropaleague'})
        rootList.append({'name': 30513, 'image': 'Copa Libertadores.png', 'action': 'matches_copalibertadores'})
        index().rootList(rootList)

class link:
    def __init__(self):
        self.dailymotion_base = 'http://www.dailymotion.com'
        self.playwire_base = 'http://cdn.playwire.com'
        self.rutube_base = 'http://rutube.ru'
        self.vkontakte_base = 'http://vk.com'
        self.sapo_base = 'http://videos.sapo.pt'
        self.videa_base = 'http://videa.hu'
        self.youtube_base = 'http://www.youtube.com'
        self.youtube_info = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'
        self.livefootballvideo_base = 'http://livefootballvideo.com'
        self.livefootballvideo_all = 'http://livefootballvideo.com/fullmatch/page/1'
        self.livefootballvideo_search = 'http://www.google.com/cse?cx=partner-pub-9069051203647610:8413886168&sa=Search&ie=UTF-8&nojs=1&ref=livefootballvideo.com/&q='
        self.livefootballvideo_highlights = 'http://livefootballvideo.com/highlights/page/1'
        self.livefootballvideo_premierleague = 'http://livefootballvideo.com/competitions/premier-league/page/1'
        self.livefootballvideo_laliga = 'http://livefootballvideo.com/competitions/la-liga/page/1'
        self.livefootballvideo_bundesliga = 'http://livefootballvideo.com/competitions/bundesliga/page/1'
        self.livefootballvideo_seriea = 'http://livefootballvideo.com/competitions/serie-a/page/1'
        self.livefootballvideo_ligue1 = 'http://livefootballvideo.com/competitions/ligue-1/page/1'
        self.livefootballvideo_eredivisie = 'http://livefootballvideo.com/competitions/eredivisie/page/1'
        self.livefootballvideo_primeiraliga = 'http://livefootballvideo.com/competitions/primeira-liga/page/1'
        self.livefootballvideo_uefachampionsleague = 'http://livefootballvideo.com/competitions/uefa-champions-league/page/1'
        self.livefootballvideo_uefaeuropaleague = 'http://livefootballvideo.com/competitions/uefa-europa-league/page/1'
        self.livefootballvideo_copalibertadores = 'http://livefootballvideo.com/competitions/copa-libertadores/page/1'

class episodes:
    def __init__(self):
        self.list = []

    def livefootballvideo(self, show, url, mode=None):
        if mode == '0': url = link().livefootballvideo_all
        elif mode == '1': url = link().livefootballvideo_premierleague
        elif mode == '2': url = link().livefootballvideo_laliga
        elif mode == '3': url = link().livefootballvideo_bundesliga
        elif mode == '4': url = link().livefootballvideo_seriea
        elif mode == '5': url = link().livefootballvideo_ligue1
        elif mode == '6': url = link().livefootballvideo_eredivisie
        elif mode == '7': url = link().livefootballvideo_primeiraliga
        elif mode == '8': url = link().livefootballvideo_uefachampionsleague
        elif mode == '9': url = link().livefootballvideo_uefaeuropaleague
        elif mode == '10': url = link().livefootballvideo_copalibertadores
        self.list = cache(self.livefootballvideo_list, show, url)
        index().episodeList(self.list)
        index().nextList(self.list[0]['show'], self.list[0]['next'])

    def livefootballvideo_highlights(self, show, url, mode=None):
        if mode == '0': url = link().livefootballvideo_highlights
        self.list = cache(self.livefootballvideo2_list, show, url)
        index().episodeList(self.list)
        index().nextList(self.list[0]['show'], self.list[0]['next'])

    def livefootballvideo_search(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query is None or self.query == ''):
            self.query = link().livefootballvideo_search + urllib.quote_plus(self.query)
            self.list = self.livefootballvideo3_list('', self.query)
            index().episodeList(self.list)

    def livefootballvideo_list(self, show, url):
        try:
            result = getUrl(url).result
            episodes = re.compile('(<li.+?</li>)').findall(result)
        except:
            return
        try:
            next = common.parseDOM(result, "div", attrs = { "class": "wp-pagenavi" })
            if len(next) > 1: next = next[1]
            else: next = next[0]
            next = common.parseDOM(next, "a", ret="href", attrs = { "class": "nextpostslink" })[0]
        except:
            next = ''

        for episode in episodes:
            try:
                title = common.parseDOM(episode, "a", ret="title")[0]
                date = common.parseDOM(episode, "p")[-1]
                d = [x for x in date.split('/')]
                if len(d) == 3: date = '%s-%s-%s' % (d[2], d[0], d[1])
                name = '%s (%s)' % (title, date)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')
                url = common.parseDOM(episode, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(episode, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'show': show, 'title': title, 'date': date, 'next': next})
            except:
                pass

        return self.list

    def livefootballvideo_parts(self, url, image, show, title, date):
        try:
            hoster = [link().dailymotion_base, link().playwire_base, link().rutube_base, link().vkontakte_base, link().videa_base, link().youtube_base]
            result = getUrl(url).result
            result = result.replace('<object', '<iframe').replace(' data=', ' src=')
            episodes = common.parseDOM(result, "div", attrs = { "id": "fullvideo" })[0]
            episodes = common.parseDOM(episodes, "div", attrs = { "class": "et-learn-more.+?" })
        except:
            return
        for episode in episodes:
            try:
                info = common.parseDOM(episode, "span")[0]
                language = info.split("-")[-1].strip()
                parts = common.parseDOM(episode, "iframe", ret="src")
                count = 0
                for url in parts:
                    try:
                        count = count + 1
                        name = '%s (%s) %s' % (title, str(count), language)
                        name = common.replaceHTMLCodes(name)
                        name = name.encode('utf-8')
                        url = common.replaceHTMLCodes(url)
                        url = url.encode('utf-8')
                        if not any(url.startswith(i) for i in hoster): raise Exception()
                        self.list.append({'name': name, 'url': url, 'image': image, 'show': show, 'title': title, 'date': date})
                    except:
                        pass
            except:
                pass

        index().episodepartsList(self.list)
        return self.list

    def livefootballvideo2_list(self, show, url):
        try:
            result = getUrl(url).result
            episodes = re.compile('(<li.+?</li>)').findall(result)
        except:
            return
        try:
            next = common.parseDOM(result, "div", attrs = { "class": "wp-pagenavi" })
            if len(next) > 1: next = next[1]
            else: next = next[0]
            next = common.parseDOM(next, "a", ret="href", attrs = { "class": "nextpostslink" })[0]
        except:
            next = ''

        for episode in episodes:
            try:
                home = common.parseDOM(episode, "div", attrs = { "class": "team.+?" })[0]
                home = home.split("&nbsp;")[0]
                away = common.parseDOM(episode, "div", attrs = { "class": "team.+?" })[-1]
                away = away.split("&nbsp;")[-1]
                title = '%s vs %s' % (home, away)
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                date = common.parseDOM(episode, "span", attrs = { "class": "starttime.+?" })[0]
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')
                name = '%s (%s)' % (title, date)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "a", ret="href", attrs = { "class": "playvideo" })[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': '', 'show': show, 'title': title, 'date': date, 'next': next})
            except:
                pass

        return self.list

    def livefootballvideo2_parts(self, url, image, show, title, date):
        try:
            hoster = [link().dailymotion_base, link().playwire_base, link().rutube_base, link().vkontakte_base, link().videa_base, link().youtube_base]
            result = getUrl(url).result
            result = result.replace('<object', '<iframe').replace(' data=', ' src=')
            parts = common.parseDOM(result, "iframe", ret="src")
        except:
            return
        for url in parts:
            try:
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                if not any(url.startswith(i) for i in hoster): raise Exception()
                self.list.append({'name': title, 'url': url, 'image': image, 'show': show, 'title': title, 'date': date})
            except:
                pass

        index().episodepartsList(self.list)
        return self.list

    def livefootballvideo3_list(self, show, url):
        try:
            result = getUrl(url).result
            episodes = common.parseDOM(result, "h2")
        except:
            return
        for episode in episodes:
            try:
                name = common.parseDOM(episode, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.replace('<b>', '').replace('</b>', '').replace('Full Match Download', 'Full Match').replace('& All Goals', '').strip()
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                if not ('/fullmatch/' in url or '/highlights/' in url): raise Exception()
                self.list.append({'name': name, 'url': url, 'image': '', 'show': show, 'title': name, 'date': ''})
            except:
                pass

        return self.list

class player:
    def run(self, url, name):
        try:
            if url.startswith(link().dailymotion_base): url = self.dailymotion(url)
            elif url.startswith(link().playwire_base): url = self.playwire(url)
            elif url.startswith(link().rutube_base): url = self.rutube(url)
            elif url.startswith(link().vkontakte_base): url = self.vkontakte(url)
            elif url.startswith(link().sapo_base): url = self.sapo(url)
            elif url.startswith(link().videa_base): url = self.videa(url)
            elif url.startswith(link().youtube_base): url = self.youtube(url)

            if url is None: raise Exception()
            index().resolve(url)
        except:
            index().infoDialog(language(30317).encode("utf-8"))
            return

    def dailymotion(self, url):
        try:
            result = getUrl(url).result
            quality = None
            try: quality = re.compile('"stream_h264_ld_url":"(.+?)"').findall(result)[0]
            except: pass
            try: quality = re.compile('"stream_h264_url":"(.+?)"').findall(result)[0]
            except: pass
            try: quality = re.compile('"stream_h264_hq_url":"(.+?)"').findall(result)[0]
            except: pass
            if quality is None or not getSetting("quality") == "0":
                try: quality = re.compile('"stream_h264_hd_url":"(.+?)"').findall(result)[0]
                except: pass
            if quality is None or getSetting("quality") == "2":
                try: quality = re.compile('"stream_h264_hd1080_url":"(.+?)"').findall(result)[0]
                except: pass
            url = urllib.unquote(quality).decode('utf-8').replace('\\/', '/')
            return url
        except:
            return

    def playwire(self, url):
        try:
            url = url.split("config=")[-1]
            result = getUrl(url).result
            url = re.compile('"src":"(.+?)"').findall(result)[0]
            return url
        except:
            return

    def rutube(self, url):
        try:
            id = url.split("/")[-1].split("?")[0]
            url = 'http://rutube.ru/api/play/trackinfo/%s/?format=xml' % id
            result = getUrl(url).result
            url = common.parseDOM(result, "m3u8")[0]
            result = getUrl(url).result
            if "EXTM3U" in result: return url
        except:
            return

    def vkontakte(self, url):
        try:
            result = getUrl(url).result
            url = common.parseDOM(result, "param", ret="value", attrs = { "name": "flashvars" })[0]
            quality = None
            try: quality = re.compile('url240=(.+?)&').findall(url)[0]
            except: pass
            try: quality = re.compile('url360=(.+?)&').findall(url)[0]
            except: pass
            try: quality = re.compile('url480=(.+?)&').findall(url)[0]
            except: pass
            if quality is None or not getSetting("quality") == "0":
                try: url = re.compile('url720=(.+?)&').findall(var)[0]
                except: pass
            if quality is None or getSetting("quality") == "2":
                try: url = re.compile('url1080=(.+?)&').findall(var)[0]
                except: pass
            url = common.replaceHTMLCodes(quality)
            return url
        except:
            return

    def sapo(self, url):
        try:
            id = url.split("file=")[-1].split("sapo.pt/")[-1].split("/")[0]
            url = '%s/%s' % (link().sapo_base, id)
            result = getUrl(url).result
            url = re.compile('file=(.+?)&').findall(result)[0]
            url = getUrl(url, fetch=False).result
            return url
        except:
            return

    def videa(self, url):
        try:
            id = url.split("?v=")[-1].split("-")[-1].split("?")[0]
            url = 'http://videa.hu/flvplayer_get_video_xml.php?v=%s&m=0' % id
            result = getUrl(url).result
            result = common.parseDOM(result, "format", attrs = { "streamable": "1" })[0]
            url = common.parseDOM(result, "version", ret="video_url")[-1]
            return url
        except:
            return

    def youtube(self, url):
        try:
            id = url.split("?v=")[-1].split("/")[-1].split("?")[0]
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