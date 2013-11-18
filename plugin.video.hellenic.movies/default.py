# -*- coding: utf-8 -*-

'''
    Hellenic Movies XBMC Addon
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

import urllib,urllib2,re,os,threading,datetime,xbmc,xbmcplugin,xbmcgui,xbmcaddon
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
addonPoster         = os.path.join(addonPath,'resources/art/Poster.jpg')
addonPages          = os.path.join(addonPath,'resources/art/Pages.png')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData            = os.path.join(dataPath,'views.cfg')
favData             = os.path.join(dataPath,'favourites2.cfg')
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
        elif action == 'movies':                    movies().get(url)
        elif action == 'movies_recent':             movies().recent()
        elif action == 'movies_favourites':         favourites().movies()
        elif action == 'movies_search':             search().movies(query)
        elif action == 'pages_cinegreece':          pages().cinegreece()
        elif action == 'pages_greekmovies':         pages().greekmovies()
        elif action == 'play':                      player().run(url, name)


        if action is None or action.startswith('root'):
            pass
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

    def resolve(self, url):
        item = xbmcgui.ListItem(path=url)
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
                if action == 'movies_favourites': cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                if action == 'movies_favourites': cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels = {'label': name, 'title': name, 'plot': addonDesc} )
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def pageList(self, pageList):
        count = 0
        total = len(pageList)
        for i in pageList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)
                u = '%s?action=movies&url=%s' % (sys.argv[0], sysurl)
                fanart = '%s/%s.jpg' % (addonSlideshow, str(count)[-1])
                count = count + 1

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels = {'label': name, 'title': name, 'plot': addonDesc} )
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems([], replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def movieList(self, movieList):
        file = open(favData,'r')
        favRead = file.read()
        file.close()

        count = 0
        total = len(movieList)
        for i in movieList:
            try:
                name, url, image, imdb, genre, plot = i['name'], i['url'], i['image'], i['imdb'], i['genre'], i['plot']
                if plot == ' ': plot = addonDesc
                try: year = re.compile('[(](\d{4})[)]').findall(name)[-1]
                except: year = ' '
                title = name.replace('(%s)' % year, '').strip()

                sysname, sysurl, sysimage, sysimdb, systitle = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(imdb), urllib.quote_plus(title)
                u = '%s?action=play&name=%s&url=%s&t=%s' % (sys.argv[0], sysname, sysurl, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))

                meta = {'label': title, 'title': title, 'year': year, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                fanart = '%s/%s.jpg' % (addonSlideshow, str(count)[-1])
                count = count + 1
                poster = image

                cm = []
                if action == 'movies_favourites':
                    cm.append((language(30362).encode("utf-8"), 'Container.Update(%s?action=movies_search&query=%s)' % (sys.argv[0], sysname)))
                    cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                    cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30419).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30420).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30421).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                elif action == 'movies_search':
                    cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                    cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_from_search&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
                else:
                    cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                    if not '"%s"' % url in favRead: cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    else: cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
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

class favourites:
    def __init__(self):
        self.list = []

    def movies(self):
        file = open(favData, 'r')
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, url, image in match:
            self.list.append({'name': name, 'url': url, 'image': image, 'imdb': '0', 'genre': 'Greek', 'plot': ' '})
        index().movieList(self.list)

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'Favourites.png', 'action': 'movies_favourites'})
        rootList.append({'name': 30502, 'image': 'Listings.png', 'action': 'pages_cinegreece'})
        rootList.append({'name': 30503, 'image': 'Listings.png', 'action': 'pages_greekmovies'})
        rootList.append({'name': 30504, 'image': 'Recent.png', 'action': 'movies_recent'})
        rootList.append({'name': 30505, 'image': 'Search.png', 'action': 'movies_search'})
        index().rootList(rootList)

class link:
    def __init__(self):
        self.cinegreece_base = 'http://www.cinegreece.com'
        self.cinegreece_page = 'http://www.cinegreece.com/p/blog-page.html'
        self.cinegreece_recent = 'http://www.cinegreece.com/search/label/%CE%95%CE%BB%CE%BB%CE%B7%CE%BD%CE%B9%CE%BA%CE%AD%CF%82%20%CE%A4%CE%B1%CE%B9%CE%BD%CE%AF%CE%B5%CF%82'

        self.greekmovies_base = 'http://greek-movies.com'
        self.greekmovies_page = 'http://greek-movies.com/movies.php'

        self.google_search = 'https://encrypted.google.com/search?as_q=%s'

        self.youtube_base = 'http://www.youtube.com'
        self.youtube_watch = 'http://www.youtube.com/watch?v=%s'
        self.youtube_info = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'
        self.dailymotion_base = 'http://www.dailymotion.com'
        self.dailymotion_watch = 'http://www.dailymotion.com/video/%s'
        self.dailymotion_info = 'http://www.dailymotion.com/embed/video/%s'
        self.flashx_base = 'http://flashx.tv'
        self.streamcloud_base = 'http://streamcloud.eu'
        self.putlocker_base = 'http://www.putlocker.com'
        self.datemule_base = 'http://www.datemule.com'
        self.veoh_base = 'http://www.veoh.com'
        self.vimeo_base = 'http://vimeo.com'

class pages:
    def __init__(self):
        self.list = []

    def cinegreece(self):
        self.list = self.cinegreece_list()
        index().pageList(self.list)

    def greekmovies(self):
        self.list = self.greekmovies_list()
        index().pageList(self.list)

    def cinegreece_list(self):
        try:
            result = getUrl(link().cinegreece_page).result
            pages = common.parseDOM(result, "select", attrs = { "name": "menu1" })[0]
            pages = re.compile('(<option.+?</option>)').findall(pages)
            pages = [i for i in pages if not "/p/blog-page.html" in i]
        except:
            return
        for page in pages:
            try:
                name = common.parseDOM(page, "option")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(page, "option", ret="value")[0]
                url = common.replaceHTMLCodes(url)
                url = url.replace(url.split("/")[2], link().cinegreece_base.split("//")[-1])
                url = url.encode('utf-8')
                image = addonPages.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

    def greekmovies_list(self):
        try:
            result = getUrl(link().greekmovies_page).result
            pages = common.parseDOM(result, "select", attrs = { "onChange": ".+?" })[0]
            pages = re.compile('(<option.+?</option>)').findall(pages)
            pages = [i for i in pages if not "?y=&g=&p=" in i]
        except:
            return
        for page in pages:
            try:
                name = common.parseDOM(page, "p")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(page, "option", ret="value")[0]
                url = common.replaceHTMLCodes(url)
                url = '%s/%s' % (link().greekmovies_base, url)
                url = url.replace('&y=&g=&p=', '')
                url = url.encode('utf-8')
                image = addonPages.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class movies:
    def __init__(self):
        self.list = []
        self.data = []

    def get(self, url):
        if url.startswith(link().cinegreece_base): self.list = self.cinegreece_list(url)
        elif url.startswith(link().greekmovies_base): self.list = self.greekmovies_list(url)
        self.list = sorted(self.list, key=itemgetter('name'))
        index().movieList(self.list)

    def recent(self):
        self.list = self.cinegreece_list2(link().cinegreece_recent)
        index().movieList(self.list)


    def cinegreece_list(self, url):
        try:
            result = getUrl(url).result
            movies = common.parseDOM(result, "div", attrs = { "itemprop": "articleBody" })[0]
            movies = re.compile('(<a.+?</a>)').findall(movies)
            movies = uniqueList(movies).list
        except:
            return
        for movie in movies:
            try:
                url = common.parseDOM(movie, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.replace(url.split("/")[2], link().cinegreece_base.split("//")[-1])
                url = url.encode('utf-8')
                year = url.split("/")[-1].split("-")[-1].split(".")[0].split("_")[0]
                year = re.sub("[^0-9]", "", year)
                name = common.parseDOM(movie, "img", ret="title")[0]
                if name.endswith('(Ο)'.decode('iso-8859-7')): name = 'Ο '.decode('iso-8859-7') + name.replace('(Ο)'.decode('iso-8859-7'), '').strip()
                elif name.endswith('(Η)'.decode('iso-8859-7')): name = 'Η '.decode('iso-8859-7') + name.replace('(Η)'.decode('iso-8859-7'), '').strip()
                elif name.endswith('(Το)'.decode('iso-8859-7')): name = 'Το '.decode('iso-8859-7') + name.replace('(Το)'.decode('iso-8859-7'), '').strip()
                elif name.endswith('(Οι)'.decode('iso-8859-7')): name = 'Οι '.decode('iso-8859-7') + name.replace('(Οι)'.decode('iso-8859-7'), '').strip()
                elif name.endswith('(Τα)'.decode('iso-8859-7')): name = 'Τα '.decode('iso-8859-7') + name.replace('(Τα)'.decode('iso-8859-7'), '').strip()
                if not year == '': name = '%s (%s)' % (name, year)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                image = common.parseDOM(movie, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': '0', 'genre': 'Greek', 'plot': ' '})
            except:
                pass

        return self.list

    def cinegreece_list2(self, url):
        try:
            result = getUrl(url).result
            movies = common.parseDOM(result, "div", attrs = { "class": "post-outer" })
            movies = uniqueList(movies).list
        except:
            return
        for movie in movies:
            try:
                name = common.parseDOM(movie, "h3")[0]
                name = common.parseDOM(name, "a")[0]
                if name.endswith('(Ο)'.decode('iso-8859-7')): name = 'Ο '.decode('iso-8859-7') + name.replace('(Ο)'.decode('iso-8859-7'), '').strip()
                elif name.endswith('(Η)'.decode('iso-8859-7')): name = 'Η '.decode('iso-8859-7') + name.replace('(Η)'.decode('iso-8859-7'), '').strip()
                elif name.endswith('(Το)'.decode('iso-8859-7')): name = 'Το '.decode('iso-8859-7') + name.replace('(Το)'.decode('iso-8859-7'), '').strip()
                elif name.endswith('(Οι)'.decode('iso-8859-7')): name = 'Οι '.decode('iso-8859-7') + name.replace('(Οι)'.decode('iso-8859-7'), '').strip()
                elif name.endswith('(Τα)'.decode('iso-8859-7')): name = 'Τα '.decode('iso-8859-7') + name.replace('(Τα)'.decode('iso-8859-7'), '').strip()
                name = common.replaceHTMLCodes(name)
                name = name.replace('[','(').replace(']',')').strip()
                name = name.encode('utf-8')
                url = common.parseDOM(movie, "h3")[0]
                url = common.parseDOM(url, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.replace(url.split("/")[2], link().cinegreece_base.split("//")[-1])
                url = url.encode('utf-8')
                image = common.parseDOM(movie, "div", attrs = { "class": "separator" })[0]
                image = common.parseDOM(image, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': '0', 'genre': 'Greek', 'plot': ' '})
            except:
                pass

        return self.list

    def greekmovies_list(self, url):
        try:
            threads = []
            result = ''
            for i in range(1, 9):
                self.data.append('')
                moviesUrl = '%s&y=%s' % (url, str(i))
                threads.append(Thread(self.thread, moviesUrl, i-1))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            movies = common.parseDOM(result, "td", attrs = { "width": ".+?" })
            movies = uniqueList(movies).list
        except:
            return
        for movie in movies:
            try:
                name = common.parseDOM(movie, "p")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(movie, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = '%s/%s' % (link().greekmovies_base, url)
                url = url.encode('utf-8')
                image = common.parseDOM(movie, "IMG", ret="SRC")[0]
                image = common.replaceHTMLCodes(image)
                image = '%s/%s' % (link().greekmovies_base, image)
                if image.endswith('icon/film.jpg'): image = addonPoster
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': '0', 'genre': 'Greek', 'plot': ' '})
            except:
                pass

        return self.list

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class search:
    def __init__(self):
        self.list = []

    def movies(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query is None or self.query == ''):
            self.greekmovies_list()
            self.cinegreece_list()
            index().movieList(self.list)

    def cinegreece_list(self):
        try:
            searchUrl = link().google_search % urllib.quote_plus(self.query) + '&as_sitesearch=cinegreece.com'
            result = getUrl(searchUrl).result
            search = re.compile('cinegreece.com/(.+?/.+?[.]html)').findall(result)
            search = uniqueList(search).list

            threads = []
            for url in search:
                url = common.replaceHTMLCodes(url)
                url = '%s/%s' % (link().cinegreece_base, url)
                url = url.encode('utf-8')
                threads.append(Thread(self.cinegreece_list2, url))
            [i.start() for i in threads]
            [i.join() for i in threads]
        except:
            pass

    def cinegreece_list2(self, url): 
        try:
            result = getUrl(url).result
            if not "/%CE%95%CE%BB%CE%BB%CE%B7%CE%BD%CE%B9%CE%BA%CE%AD%CF%82%20%CE%A4%CE%B1%CE%B9%CE%BD%CE%AF%CE%B5%CF%82" in result: raise Exception()
            name = common.parseDOM(result, "h3")[0]
            name = common.replaceHTMLCodes(name)
            name = name.replace('[','(').replace(']',')').strip()
            name = name.encode('utf-8')
            image = common.parseDOM(result, "div", attrs = { "class": "separator" })[0]
            image = common.parseDOM(image, "img", ret="src")[0]
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
            self.list.append({'name': name, 'url': url, 'image': image, 'imdb': '0', 'genre': 'Greek', 'plot': ' '})
        except:
            pass

    def greekmovies_list(self):
        try:
            searchUrl = link().google_search % urllib.quote_plus(self.query) + '&as_sitesearch=greek-movies.com'
            result = getUrl(searchUrl).result
            search = re.compile('greek-movies.com/(movies.php[?]m=\d*)').findall(result)
            search = uniqueList(search).list

            threads = []
            for url in search:
                url = common.replaceHTMLCodes(url)
                url = '%s/%s' % (link().greekmovies_base, url)
                url = url.encode('utf-8')
                threads.append(Thread(self.greekmovies_list2, url))
            [i.start() for i in threads]
            [i.join() for i in threads]
        except:
            pass

    def greekmovies_list2(self, url): 
        try:
            result = getUrl(url).result
            name = common.parseDOM(result, "DIV", attrs = { "class": "maincontent" })[0]
            title = common.parseDOM(name, "p")[0]
            year = common.parseDOM(name, "p", attrs = { "class": "movieheading3" })[0].split(" ")[-1]
            name = '%s (%s)' % (title, year)
            name = common.replaceHTMLCodes(name)
            name = name.encode('utf-8')
            image = common.parseDOM(result, "DIV", attrs = { "class": "maincontent" })[0]
            image = common.parseDOM(image, "img", ret="src")[0]
            image = common.replaceHTMLCodes(image)
            image = '%s/%s' % (link().greekmovies_base, image)
            if image.endswith('icon/film.jpg'): image = addonPoster
            image = image.encode('utf-8')
            self.list.append({'name': name, 'url': url, 'image': image, 'imdb': '0', 'genre': 'Greek', 'plot': ' '})
        except:
            pass

class player:
    def __init__(self):
        self.data = []

    def run(self, url, name=None):
        try:
            if url.startswith(link().cinegreece_base): sources = self.cinegreece(url)
            elif url.startswith(link().greekmovies_base): sources = self.greekmovies(url)

            for url in sources:
                if url.startswith(link().youtube_base): url = self.youtube(url)
                elif url.startswith(link().datemule_base): url = self.datemule(url)
                elif url.startswith(link().vimeo_base): url = self.vimeo(url)
                else: url = self.urlresolver(url)
                if url is not None: break

            if url is None or sources is None or sources == []: raise Exception()
            index().resolve(url)
        except:
            index().infoDialog(language(30317).encode("utf-8"))
            return


    def cinegreece(self, url):
        try:
            result = getUrl(url).result
            url = common.parseDOM(result, "div", attrs = { "itemprop": "articleBody" })[0]
            url = common.parseDOM(url, "a", ret="onclick")[0]
            url = re.compile("'(.+?)'").findall(url)[0]
            url = common.replaceHTMLCodes(url)
            sources = [url]
            return sources
        except:
            return

    def greekmovies(self, url):
        try:
            result = getUrl(url).result
            sources = common.parseDOM(result, "DIV", attrs = { "class": "maincontent" })[0]
            sources = common.parseDOM(sources, "tr",)[-1]
            sources = common.parseDOM(sources, "p")
            sources = uniqueList(sources).list

            sourcesList = []
            for source in sources:
                try:
                    source = common.parseDOM(source, "a", ret="href")
                    if len(source) > 1: raise Exception()
                    source = '%s/%s' % (link().greekmovies_base, source[0])
                    sourcesList.append(source)
                except:
                    pass

            result = []
            threads = []
            for i in range(0, len(sourcesList)):
                self.data.append('')
                threads.append(Thread(self.thread, sourcesList[i], i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for data in self.data:
                data = common.parseDOM(data, "button", ret="OnClick")[0]
                data = data.split("'")[1]
                result.append(data)

            sources = []
            sources += [i for i in result if link().youtube_base in i]
            sources += [i for i in result if link().putlocker_base in i]
            sources += [i for i in result if link().datemule_base in i]
            sources += [i for i in result if link().dailymotion_base in i]
            sources += [i for i in result if link().veoh_base in i]
            sources += [i for i in result if link().vimeo_base in i]

            return sources
        except:
            return

    def datemule(self, url):
        try:
            result = getUrl(url).result
            url = common.parseDOM(result, "A", ret="onclick")[0]
            url = re.compile("'(.+?)'").findall(url)[0]
            url = url.split("title=")[0]
            result = getUrl(url).result
            url = re.compile('href="(.+?)"').findall(result)[0]
            return url
        except:
            return

    def vimeo(self, url):
        try:
            url = 'http://www.flashvideodownloader.org/download.php?u=%s' % url
            result = getUrl(url).result
            url = common.parseDOM(result, "div", attrs = { "class": "mod_download" })[0]
            url = common.parseDOM(url, "a", ret="href")[0]
            return url
        except:
            return

    def urlresolver(self, url):
        try:
            host = urlresolver.HostedMediaFile(url)
            if host: url = urlresolver.resolve(url)
            if url: return url
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

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return


main()