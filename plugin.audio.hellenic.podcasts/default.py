# -*- coding: utf-8 -*-

'''
    Hellenic Podcasts XBMC Addon
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
addonArtReal        = os.path.join(addonPath,'resources/art/REAL.png')
addonArtSkai        = os.path.join(addonPath,'resources/art/SKAI.png')
addonArtAlpha       = os.path.join(addonPath,'resources/art/ALPHA.png')
addonSound          = os.path.join(addonPath,'resources/art/sound.png')
addonSlideshow      = os.path.join(addonPath,'resources/slideshow')
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
        elif action == 'item_play':                 contextMenu().item_play()
        elif action == 'item_random_play':          contextMenu().item_random_play()
        elif action == 'item_queue':                contextMenu().item_queue()
        elif action == 'playlist_open':             contextMenu().playlist_open()
        elif action == 'settings_open':             contextMenu().settings_open()
        elif action == 'addon_home':                contextMenu().addon_home()
        elif action == 'view_root':                 contextMenu().view('root')
        elif action == 'view_tvshows':              contextMenu().view('shows')
        elif action == 'view_episodes':             contextMenu().view('podcasts')
        elif action == 'shows_real':                shows().real()
        elif action == 'shows_alpha':               shows().alphatv()
        elif action == 'shows_skai':                shows().skai()
        elif action == 'episodes':                  episodeList().get(name, url, image, imdb, genre, plot, show)
        elif action == 'episodes_parts':            partList().episodes(name, url, image, imdb, genre, plot, show)
        elif action == 'play':                      player().run(url, name)


        if action is None or action.startswith('root'):
            xbmcplugin.setContent(int(sys.argv[1]), 'albums')
            index().container_view('root', {'skin.confluence' : 500})
        elif action.startswith('shows'):
            xbmcplugin.setContent(int(sys.argv[1]), 'albums')
            index().container_view('shows', {'skin.confluence' : 506})
        elif action.startswith('episodes'):
            xbmcplugin.setContent(int(sys.argv[1]), 'albums')
            index().container_view('podcasts', {'skin.confluence' : 506})
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
        xbmc.executebuiltin('Container.Refresh')

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
        image = ''
        if url.startswith(link().real_base): image = addonArtReal
        item = xbmcgui.ListItem(path=url.split(' playpath=')[0], iconImage=image, thumbnailImage=image)
        item.setProperty('PlayPath', url.split(' playpath=')[-1]) 
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

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
                cm.append((language(30427).encode("utf-8"), 'RunPlugin(%s?action=view_root)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Music", infoLabels = {'label': name, 'title': name, 'artist': name, 'comment': addonDesc} )
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def showList(self, showList):
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

                meta = {'label': name, 'title': name, 'album' : name, 'genre' : genre, 'comment': plot}
                poster, banner = image, image

                cm = []
                cm.append((language(30429).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))


                item = xbmcgui.ListItem(name, iconImage=poster, thumbnailImage=poster)
                item.setInfo( type="Music", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Music", "true")
                item.setProperty("Album_Label", name)
                item.setProperty("Album_Description", plot)
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

                sysname, sysurl, sysimage, sysimdb, sysgenre, sysplot, sysshow = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(imdb), urllib.quote_plus(genre), urllib.quote_plus(plot), urllib.quote_plus(show)
                u = '%s?action=play&name=%s&url=%s' % (sys.argv[0], sysname, sysurl)
                if url.startswith(link().real_part):
                    u = '%s?action=episodes_parts&url=%s&image=%s&imdb=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysurl, sysimage, sysimdb, sysgenre, sysplot, sysshow)
                meta = {'label': name, 'title': name, 'album' : name, 'artist': show, 'genre' : genre, 'comment': plot}
                fanart = '%s/%s.jpg' % (addonSlideshow, str(count)[-1])
                count = count + 1
                try: fanart = i['fanart']
                except: pass
                poster = image

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30433).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage=poster, thumbnailImage=poster)
                item.setInfo( type="Music", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Music", "true")
                item.setProperty("Album_Label", show)
                item.setProperty("Album_Description", plot)
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                if url.startswith(link().real_part): xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
                else: xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
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

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(MusicPlaylist)')

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
        rootList.append({'name': 30501, 'image': 'REAL.png', 'action': 'shows_real'})
        rootList.append({'name': 30502, 'image': 'SKAI.png', 'action': 'shows_skai'})
        rootList.append({'name': 30503, 'image': 'ALPHA.png', 'action': 'shows_alpha'})
        index().rootList(rootList)

class link:
    def __init__(self):
        self.real_base = 'http://www.real.gr'
        self.real_part = 'http://www.real.gr/DefaultArthro.aspx'
        self.real_shows = 'http://www.real.gr/DefaultArthro.aspx?page=radioathens'
        self.real_episodes = 'http://www.real.gr/DefaultArthro.aspx?page=category&getPaging=true&catid='
        self.real_recent = 'http://www.real.gr/DefaultArthro.aspx?page=category&getPaging=true&catid=50'
        self.real_file = 'http://www.real.gr/audiofiles'

        self.alphatv_base = 'http://www.alpha989.com'
        self.alphatv_shows = 'http://www.alpha989.com'

        self.skai_base = 'http://www.skai.gr'
        self.skai_shows = 'http://www.skai.gr/Ajax.aspx?m=Skai.TV.ProgramListView&la=0&Type=Radio&Day=%s'
        self.skai_episodes = 'http://www.skai.gr/Ajax.aspx?m=Skai.Player.ItemView&type=Radio&cid=6&alid=%s'

class shows:
    def __init__(self):
        self.list = []

    def real(self):
        #self.list = showList().real_list()
        self.list = cache(showList().real_list)
        index().showList(self.list)

    def alphatv(self):
        #self.list = showList().alphatv_list()
        self.list = cache(showList().alphatv_list)
        index().showList(self.list)

    def skai(self):
        #self.list = showList().skai_list()
        self.list = cache(showList().skai_list)
        index().showList(self.list)

class showList:
    def __init__(self):
        self.list = []
        self.data = []

    def real_list(self):
        try:
            result = getUrl(link().real_shows).result
            shows = common.parseDOM(result, "td", attrs = { "class": "CategoryHeader" })
            self.list.append({'name': 'Πρόσφατα'.decode('iso-8859-7').encode('utf-8'), 'url': link().real_recent, 'image': addonArtReal.encode('utf-8'), 'imdb': '0', 'genre': 'Greek', 'plot': ''})
        except:
            return
        for show in shows:
            try:
                name = common.parseDOM(show, "span", attrs = { "style": "color:.+?" })[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(show, "a", ret="href")[0]
                url = url.split("=")[-1]
                url = re.sub("\D", "", url)
                url = '%s%s' % (link().real_episodes, url)
                url = url.encode('utf-8')
                image = addonArtReal.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': '0', 'genre': 'Greek', 'plot': ''})
            except:
                pass

        return self.list

    def alphatv_list(self):
        try:
            result = getUrl(link().alphatv_shows).result
            result = common.parseDOM(result, "div", attrs = { "class": "producersHome" })[0]
            shows = common.parseDOM(result, "div", attrs = { "class": "pItem" })
        except:
            return
        for show in shows:
            try:
                name = common.parseDOM(show, "h2")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(show, "a", ret="href")[0]
                url = '%s/%s' % (link().alphatv_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = addonArtAlpha.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': '0', 'genre': 'Greek', 'plot': ''})
            except:
                pass

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
                self.list.append({'name': name, 'url': url, 'image': addonArtSkai.encode('utf-8'), 'image2': image, 'imdb': '0', 'genre': 'Greek', 'plot': plot})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('name'))
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
        if url.startswith(link().real_base):
            self.list = self.real_list(name, url, image, imdb, genre, plot, show)
        elif url.startswith(link().alphatv_base):
            self.list = self.alphatv_list(name, url, image, imdb, genre, plot, show)
        elif url.startswith(link().skai_base):
            self.list = self.skai_list(name, url, image, imdb, genre, plot, show)
        index().episodeList(self.list)


    def real_list(self, name, url, image, imdb, genre, plot, show):
        threads = []
        for i in range(1, 5):
            self.data.append('')
            episodesUrl = '%s&curPage=%s' % (url, str(i))
            threads.append(Thread(self.thread, episodesUrl, i-1))
        [i.start() for i in threads]
        [i.join() for i in threads]

        result = ''
        for i in range(0, 4):
            try:
                result += '<tr>' + common.parseDOM(self.data[i], "td", attrs = { "class": "real_article_header_1stline" })[0]
                id = re.compile('<div id="(.+?Article)"').findall(self.data[i])[0]
                result += common.parseDOM(self.data[i], "div", attrs = { "id": id })[0] + '</tr>'
                id = re.compile('<div id="(.+?ArticleList)"').findall(self.data[i])[0]
                result += common.parseDOM(self.data[i], "div", attrs = { "id": id })[0]
            except:
                pass

        try:
            episodes = common.parseDOM(result, "tr")
        except:
            return
        for episode in episodes:
            try:
                name = common.parseDOM(episode, "a", attrs = { "class": ".+?" })[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "a", attrs = { "class": ".+?" }, ret="href")[0]
                url = '%s/%s' % (link().real_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = addonArtReal.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'season': '1', 'episode': '1'})
            except:
                pass

        return self.list

    def alphatv_list(self, name, url, image, imdb, genre, plot, show):
        try:
            result = ''
            threads = []
            for i in range(1, 6):
                self.data.append('')
                episodesUrl = '%s&p=%s' % (url, str(i))
                threads.append(Thread(self.thread, episodesUrl, i-1))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            result = common.parseDOM(result, "div", attrs = { "class": "playNow" })
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
                url = '%s/%s' % (link().alphatv_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = addonArtAlpha.encode('utf-8')
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
                self.list.append({'name': name, 'url': url, 'image': addonArtSkai.encode('utf-8'), 'imdb': imdb, 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'season': '1', 'episode': '1'})
            except:
                pass

        return self.list

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class partList:
    def __init__(self):
        self.list = []

    def episodes(self, name, url, image, imdb, genre, plot, show):
        self.list = self.real_list(name, url, image, imdb, genre, plot, show)
        index().episodeList(self.list)

    def real_list(self, name, url, image, imdb, genre, plot, show):
        try:
            result = getUrl(url).result
            result = common.parseDOM(result, "ul", attrs = { "id": ".+?CarouselList" })[0]
            episodes = common.parseDOM(result, "li")
        except:
            return
        for episode in episodes:
            try:
                name = common.parseDOM(episode, "img", ret="alt")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "a", ret="href")[0]
                url = url.split('FileName=')[1]
                url = '%s/%s' % (link().real_file, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = addonSound.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'season': '1', 'episode': '1'})
            except:
                pass

        return self.list

class player:
    def run(self, url, name=None):
        try:
            if url.startswith(link().alphatv_base): url = self.alphatv(url)
            if url is None: raise Exception()
            index().resolve(url)
        except:
            index().infoDialog(language(30317).encode("utf-8"))
            return

    def alphatv(self, url):
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

            url = '%s playpath=%s' % (rtmp, playpath)
            return url
        except:
            return


main()