# -*- coding: utf-8 -*-

'''
    hellenic movies XBMC Addon
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
addonDesc1			= language(30451).encode("utf-8")
addonDesc2			= language(30452).encode("utf-8")
addonIcon			= os.path.join(addonPath,'icon.png')
addonFanart			= os.path.join(addonPath,'fanart.jpg')
addonArt			= os.path.join(addonPath,'resources/art')
addonFolder			= os.path.join(addonPath,'resources/art/Folder.png')
addonPoster			= os.path.join(addonPath,'resources/art/Poster.jpg')
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
        try:		url = urllib.unquote_plus(params["url"])
        except:		url = None
        try:		image = urllib.unquote_plus(params["image"])
        except:		image = None

        if action == None:							categories().get()
        elif action == 'item_play':					contextMenu().item_play()
        elif action == 'item_random_play':			contextMenu().item_random_play()
        elif action == 'item_queue':				contextMenu().item_queue()
        elif action == 'item_play_from_here':		contextMenu().item_play_from_here(url)
        elif action == 'favourite_add':				contextMenu().favourite_add(name, url, image)
        elif action == 'favourite_delete':			contextMenu().favourite_delete(name, url, image)
        elif action == 'favourite_moveUp':			contextMenu().favourite_moveUp(name, url, image)
        elif action == 'favourite_moveDown':		contextMenu().favourite_moveDown(name, url, image)
        elif action == 'favourite_from_search':		contextMenu().favourite_from_search(name, url, image)
        elif action == 'playlist_start':			contextMenu().playlist_start()
        elif action == 'playlist_open':				contextMenu().playlist_open()
        elif action == 'settings_open':				contextMenu().settings_open()
        elif action == 'global_view':				contextMenu().global_view()
        elif action == 'favourites':				favourites().get()
        elif action == 'channels':					channels().get()
        elif action == 'cinegreece_menus':			menus().cinegreece()
        elif action == 'greekmovies_menus':			menus().greekmovies()
        elif action == 'movies':					movies().get(url)
        elif action == 'movies_recent':				movies().recent()
        elif action == 'search':					search().run()
        elif action == 'live':						player().live(name)
        elif action == 'play':						player().run(url)

        viewDict = {
            'skin.confluence'	: 503,	'skin.aeon.nox'		: 50,	'skin.back-row'			: 519,
            'skin.bello'		: 50,	'skin.carmichael'	: 50,	'skin.diffuse'			: 55,
            'skin.droid'		: 50,	'skin.metropolis'	: 55,	'skin.pm3-hd'			: 58,
            'skin.rapier'		: 66,	'skin.re-touched'	: 50,	'skin.simplicity'		: 50,
            'skin.transparency'	: 58,	'skin.xeebo'		: 50,	'skin.xperience1080'	: 50
            }

        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
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
        for i in favList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                year = ""
                try: year = re.compile('[[](\d*)[]]').findall(name)[0]
                except: pass
                try: year = re.compile('[(](\d*)[)]').findall(name)[0]
                except: pass
                title = name.replace(year,'').replace('()','').replace('[]','').strip()
                if url.startswith(player().cinegreeceUrl): addonDesc = addonDesc1
                elif url.startswith(player().greekmoviesUrl): addonDesc = addonDesc2
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)
                u = '%s?action=play&url=%s' % (sys.argv[0], sysurl)

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_play_from_here&url=%s)' % (sys.argv[0], sysurl)))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": title, "Title": title, "Year": year, "Genre": "Greek", "Plot": addonDesc } )
                item.setProperty("IsPlayable", "true")
                item.setProperty( "Video", "true" )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
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
                if action.startswith('movies') or action == 'favourites':
                    cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                    cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def channelList(self, channelList):
        total = len(channelList)
        for i in channelList:
            try:
                name = i['name']
                image = '%s/%s.png' % (addonArt, name)
                sysname = urllib.quote_plus(name)
                u = '%s?action=live&name=%s' % (sys.argv[0], sysname)

                cm = []
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Duration": "1440", "Plot": addonDesc } )
                item.setProperty("IsPlayable", "true")
                item.setProperty( "Video", "true" )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

    def menuList(self, menuList):
        total = len(menuList)
        for i in menuList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)
                u = '%s?action=movies&url=%s' % (sys.argv[0], sysurl)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def movieList(self, movieList):
        file = open(favData,'r')
        favRead = file.read()
        file.close()

        total = len(movieList)
        for i in movieList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                year = ""
                try: year = re.compile('[[](\d*)[]]').findall(name)[0]
                except: pass
                try: year = re.compile('[(](\d*)[)]').findall(name)[0]
                except: pass
                title = name.replace(year,'').replace('()','').replace('[]','').strip()
                if url.startswith(player().cinegreeceUrl): addonDesc = addonDesc1
                elif url.startswith(player().greekmoviesUrl): addonDesc = addonDesc2
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)
                u = '%s?action=play&url=%s' % (sys.argv[0], sysurl)

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_play_from_here&url=%s)' % (sys.argv[0], sysurl)))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                if not url in favRead:
                    cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                else:
                    cm.append((language(30414).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": title, "Title": title, "Year": year, "Genre": "Greek", "Plot": addonDesc } )
                item.setProperty("IsPlayable", "true")
                item.setProperty( "Video", "true" )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

    def searchList(self, searchList):
        total = len(searchList)
        for i in searchList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                year = ""
                try: year = re.compile('[[](\d*)[]]').findall(name)[0]
                except: pass
                try: year = re.compile('[(](\d*)[)]').findall(name)[0]
                except: pass
                title = name.replace(year,'').replace('()','').replace('[]','').strip()
                label = '[B]%s[/B]' % name
                if url.startswith(player().cinegreeceUrl):
                    addonDesc = addonDesc1
                    label += ' - Cine-Greece'
                elif url.startswith(player().greekmoviesUrl):
                    addonDesc = addonDesc2
                    label += ' - Greek-Movies'
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)
                u = '%s?action=play&url=%s' % (sys.argv[0], sysurl)

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_play_from_here&url=%s)' % (sys.argv[0], sysurl)))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=favourite_from_search&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": title, "Title": title, "Year": year, "Genre": "Greek", "Plot": addonDesc } )
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

    def favourite_from_search(self, name, url, image):
        try:
            file = open(favData,'r')
            read = file.read()
            file.close()
            if url in read:
                index().infoDialog(language(30307).encode("utf-8"), name)
                return
            file = open(favData, 'a+')
            file.write('"%s"|"%s"|"%s"\n' % (name, url, image))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
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
        catList.append({'name': 30502, 'image': 'Live.png', 'action': 'channels'})
        catList.append({'name': 30503, 'image': 'Cine-Greece.png', 'action': 'cinegreece_menus'})
        catList.append({'name': 30504, 'image': 'Greek-Movies.png', 'action': 'greekmovies_menus'})
        catList.append({'name': 30505, 'image': 'Recent.png', 'action': 'movies_recent'})
        catList.append({'name': 30506, 'image': 'Search.png', 'action': 'search'})
        index().catList(catList)

class channels:
    def __init__(self):
        self.list = []

    def get(self):
        self.list.append({'name': 'GREEK CINEMA'})
        index().channelList(self.list)

class menus:
    def __init__(self):
        self.list = []
        self.cinegreeceUrl			= 'http://www.cinegreece.com'
        self.greekmoviesUrl			= 'http://greek-movies.com'
        self.cinegreece_menusUrl	= 'http://www.cinegreece.com/p/blog-page.html'
        self.greekmovies_menusUrl	= 'http://greek-movies.com/movies.php'

    def cinegreece(self):
        self.list = self.cinegreece_list()
        index().menuList(self.list)

    def greekmovies(self):
        self.list = self.greekmovies_list()
        index().menuList(self.list)

    def cinegreece_list(self):
        try:
            result = getUrl(self.cinegreece_menusUrl).result
            menus = common.parseDOM(result, "select", attrs = { "name": "menu1" })[0]
            menus = re.compile('(<option.+?</option>)').findall(menus)
            menus = [x for x in menus if not "/p/blog-page.html" in x]
        except:
            return
        for menu in menus:
            try:
                name = common.parseDOM(menu, "option")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(menu, "option", ret="value")[0]
                url = common.replaceHTMLCodes(url)
                url = url.replace(url.split("/")[2], self.cinegreeceUrl.split("//")[-1])
                url = url.encode('utf-8')
                image = addonFolder.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

    def greekmovies_list(self):
        try:
            result = getUrl(self.greekmovies_menusUrl).result
            menus = common.parseDOM(result, "select", attrs = { "onChange": ".+?" })[0]
            menus = re.compile('(<option.+?</option>)').findall(menus)
            menus = [x for x in menus if not "?y=&g=&p=" in x]
        except:
            return
        for menu in menus:
            try:
                name = common.parseDOM(menu, "p")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(menu, "option", ret="value")[0]
                url = common.replaceHTMLCodes(url)
                url = '%s/%s' % (self.greekmoviesUrl, url)
                url = url.replace('&y=&g=&p=', '')
                url = url.encode('utf-8')
                image = addonFolder.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class movies:
    def __init__(self):
        self.list = []
        self.data = ''
        self.cinegreeceUrl			= 'http://www.cinegreece.com'
        self.greekmoviesUrl			= 'http://greek-movies.com'
        self.cinegreecerecentUrl	= 'http://www.cinegreece.com/search/label/%CE%95%CE%BB%CE%BB%CE%B7%CE%BD%CE%B9%CE%BA%CE%AD%CF%82%20%CE%A4%CE%B1%CE%B9%CE%BD%CE%AF%CE%B5%CF%82'

    def get(self, url):
        if url.startswith(self.cinegreeceUrl):
            self.list = self.cinegreece_list(url)
        elif url.startswith(self.greekmoviesUrl):
            self.list = self.greekmovies_list(url)
        self.list = sorted(self.list, key=itemgetter('name'))
        index().movieList(self.list)

    def recent(self):
        self.list = self.cinegreece_list2(self.cinegreecerecentUrl)
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
                name = common.parseDOM(movie, "img", ret="title")[0]
                url = common.parseDOM(movie, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.replace(url.split("/")[2], self.cinegreeceUrl.split("//")[-1])
                url = url.encode('utf-8')
                year = url.split("/")[-1].split(".")[0].split("_")[0]
                name = '%s (%s)' % (name, year)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                image = common.parseDOM(movie, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image})
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
                name = common.replaceHTMLCodes(name)
                name = name.replace('[','(').replace(']',')').strip()
                name = name.encode('utf-8')
                url = common.parseDOM(movie, "h3")[0]
                url = common.parseDOM(url, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.replace(url.split("/")[2], self.cinegreeceUrl.split("//")[-1])
                url = url.encode('utf-8')
                image = common.parseDOM(movie, "div", attrs = { "class": "separator" })[0]
                image = common.parseDOM(image, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

    def greekmovies_list(self, url):
        try:
            threads = []
            for i in range(1, 9):
                moviesUrl = '%s&y=%s' % (url, str(i))
                threads.append(Thread(self.greekmovies_list2, moviesUrl))
            [i.start() for i in threads]
            [i.join() for i in threads]

            result = self.data
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
                url = '%s/%s' % (self.greekmoviesUrl, url)
                url = url.encode('utf-8')
                image = common.parseDOM(movie, "IMG", ret="SRC")[0]
                image = common.replaceHTMLCodes(image)
                image = '%s/%s' % (self.greekmoviesUrl, image)
                if image.endswith('icon/film.jpg'): image = addonPoster
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

    def greekmovies_list2(self, url):
        try:
            result = getUrl(url).result
            self.data += result
        except:
            return

class search:
    def __init__(self):
        self.list = []
        self.cinegreeceUrl			= 'http://www.cinegreece.com'
        self.greekmoviesUrl			= 'http://greek-movies.com'
        self.searchUrl				= 'https://encrypted.google.com/search?as_q=%s'

    def run(self):
        self.query = common.getUserInput(language(30506).encode("utf-8"), '')
        self.greekmovies_list()
        self.cinegreece_list()
        index().searchList(self.list)

    def cinegreece_list(self):
        try:
            searchUrl = self.searchUrl % urllib.quote_plus(self.query) + '&as_sitesearch=cinegreece.com'
            result = getUrl(searchUrl).result
            search = re.compile('cinegreece.com/(.+?/.+?[.]html)').findall(result)
            search = uniqueList(search).list

            threads = []
            for url in search:
                url = common.replaceHTMLCodes(url)
                url = '%s/%s' % (self.cinegreeceUrl, url)
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
            self.list.append({'name': name, 'url': url, 'image': image})
        except:
            pass

    def greekmovies_list(self):
        try:
            searchUrl = self.searchUrl % urllib.quote_plus(self.query) + '&as_sitesearch=greek-movies.com'
            result = getUrl(searchUrl).result
            search = re.compile('greek-movies.com/(movies.php[?]m=\d*)').findall(result)
            search = uniqueList(search).list

            threads = []
            for url in search:
                url = common.replaceHTMLCodes(url)
                url = '%s/%s' % (self.greekmoviesUrl, url)
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
            image = '%s/%s' % (self.greekmoviesUrl, image)
            if image.endswith('icon/film.jpg'): image = addonPoster
            image = image.encode('utf-8')
            self.list.append({'name': name, 'url': url, 'image': image})
        except:
            pass

class player:
    def __init__(self):
        self.list = []
        self.cinegreeceUrl			= 'http://www.cinegreece.com'
        self.greekmoviesUrl			= 'http://greek-movies.com'
        self.youtubeUrl				= 'http://www.youtube.com'
        self.youtube_infoUrl		= 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'
        self.flashxUrl				= 'http://flashx.tv'
        self.streamcloudUrl			= 'http://streamcloud.eu'
        self.putlockerUrl			= 'http://www.putlocker.com'
        self.datemuleUrl			= 'http://www.datemule.com'
        self.dailymotionUrl			= 'http://www.dailymotion.com'
        self.veohUrl				= 'http://www.veoh.com'
        self.vimeoUrl				= 'http://vimeo.com'

    def run(self, url):
        if url.startswith(self.cinegreeceUrl):
            sources = self.cinegreece(url)
            str = ' Greek-Movies.'
        elif url.startswith(self.greekmoviesUrl):
            sources = self.greekmovies(url)
            str = ' Cine-Greece.'

        for url in sources:
            if url.startswith(self.youtubeUrl):
                url = self.youtube(url)
            elif url.startswith(self.flashxUrl):
                url = self.flashx(url)
            elif url.startswith(self.streamcloudUrl):
                url = self.streamcloud(url)
            elif url.startswith(self.putlockerUrl):
                url = self.putlocker(url)
            elif url.startswith(self.datemuleUrl):
                url = self.datemule(url)
            elif url.startswith(self.dailymotionUrl):
                url = self.dailymotion(url)
            elif url.startswith(self.veohUrl):
                url = self.veoh(url)
            elif url.startswith(self.vimeoUrl):
                url = self.vimeo(url)
            if url is not None: break

        if url is None or sources is None or sources == []:
            index().infoDialog(language(30309).encode("utf-8")+str, header=language(30308).encode("utf-8"))
            return
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        return url

    def live(self, channel):
        channelDict = {
            'GREEK CINEMA'		:	[{'type': '', 'url': 'rtmp://94.102.58.46:80/cinema playpath=cinema.sdp pageUrl=http://www.kanalia.eu/ live=1 timeout=10', 'type2': 'False', 'url2': 'False'}]
        }

        playerDict = {
            ''					:	self.direct
        }

        i = channelDict[channel][0]
        type, url, type2, url2 = i['type'], i['url'], i['type2'], i['url2']
        url = playerDict[type](url)
        if url is None and not type2 == "False": url = playerDict[type2](url2)
        if url is None: return

        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        return url

    def cinegreece(self, url):
        try:
            result = getUrl(url).result
            url = common.parseDOM(result, "div", attrs = { "itemprop": "articleBody" })[0]
            url = common.parseDOM(url, "a", ret="onclick")[0]
            url = re.compile("'(.+?)'").findall(url)[0]
            url = url.split("&amp;")[0].split("/")[-1].split("=")[-1]
            url = 'http://www.youtube.com/watch?v=%s' % url
            return [url]
        except:
            return

    def greekmovies(self, url):
        try:
            result = getUrl(url).result
            sources = common.parseDOM(result, "DIV", attrs = { "class": "maincontent" })[0]
            sources = common.parseDOM(sources, "tr",)[-1]
            sources = common.parseDOM(sources, "p")
            sources = uniqueList(sources).list
            for source in sources:
                try:
                    source = common.parseDOM(source, "a", ret="href")
                    if len(source) > 1: raise Exception()
                    source = '%s/%s' % (self.greekmoviesUrl, source[0])
                    self.list.append(source)
                except:
                    pass
            threads = []
            for i in range(0, len(self.list)):
                threads.append(Thread(self.greekmovies2, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            list = []
            list += [i for i in self.list if self.youtubeUrl in i]
            list += [i for i in self.list if self.putlockerUrl in i]
            list += [i for i in self.list if self.datemuleUrl in i]
            list += [i for i in self.list if self.dailymotionUrl in i]
            list += [i for i in self.list if self.veohUrl in i]
            list += [i for i in self.list if self.vimeoUrl in i]
            self.list = list

            return self.list
        except:
            return

    def greekmovies2(self, i):
        try:
            result = getUrl(self.list[i]).result
            source = common.parseDOM(result, "button", ret="OnClick")[0]
            source = source.split("'")[1]
            self.list[i] = source
        except:
            return

    def direct(self, url):
        return url

    def youtube(self, url):
        try:
            id = url.split("?v=")[-1]

            state, reason = None, None
            result = getUrl(self.youtube_infoUrl % id).result
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
                index().okDialog(language(30351).encode("utf-8"), language(30352).encode("utf-8"))
                return

            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
            return url
        except:
            return

    def flashx(self, url):
        try:
            result = getUrl(url).result
            embedUrl = re.compile('"(http://play.flashx.tv/player/embed.php.+?)"').findall(result)[0]

            post = ''
            result = getUrl(embedUrl).result
            php = re.compile('action="(.+?.php)"').findall(result)[0]
            phpUrl = 'http://play.flashx.tv/player/%s' % php
            match = common.parseDOM(result, "form", attrs = { "action": php })[0]
            match = re.compile('name="(.+?)".+?value="(.+?)"').findall(match)
            for name, value in match:
                post += '%s=%s&' % (name, urllib.quote_plus(value))

            result = getUrl(phpUrl,post=post).result
            swfUrl = re.compile('(http://play.flashx.tv/nuevo/player/player.swf.+?)"').findall(result)[0]
            cfgUrl = swfUrl.split("?config=")[-1]

            getUrl(swfUrl,referer=phpUrl).result
            result = getUrl(cfgUrl,referer=phpUrl).result
            url = common.parseDOM(result, "file")[0]

            return url
        except:
            return

    def streamcloud(self, url):
        try:
            import time
            result = getUrl(url).result

            post = ''
            match = common.parseDOM(result, "form", attrs = { "class": "proform" })[0]
            match = re.compile('name="(.+?)".+?value="(.+?)"').findall(match)
            for name, value in match:
                post += '%s=%s&' % (name, urllib.quote_plus(value))

            count = re.compile('var count(.+?)\n').findall(result)[0]
            count = int(re.sub("\D", "", count)) + 1

            time.sleep(count)
            result = getUrl(url,post=post).result
            url = re.compile('file: "(.+?)"').findall(result)[0]

            return url
        except:
            return

    def putlocker(self, url):
        try:
            import urlparse
            try: password = urlparse.parse_qs(urlparse.urlparse(url).query)['file_password'][0]
            except: password = ''
            result = getUrl(url).result
            hash = re.compile('value="(.+?)".+?name="hash"').findall(result)[0]
            post = 'hash=%s&confirm=Continue+as+Free+User&file_password=%s' % (hash, password)
            result = getUrl(url,post=post).result
            url = re.compile('href="(.+?)".+?class="download_file_link"').findall(result)[0]
            url = "http://putlocker.com%s" % url
            return url
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

    def dailymotion(self, url):
        try:
            result = getUrl(url).result
            url = re.compile('"flashvars".+?value="(.+?)"').findall(result)[0]
            url = urllib.unquote(url).decode('utf-8').replace('\\/', '/')
            try:	qURL = re.compile('"video_url":"(.+?)"').findall(url)[0]
            except:	pass
            try:	qURL = re.compile('"ldURL":"(.+?)"').findall(url)[0]
            except:	pass
            try:	qURL = re.compile('"sdURL":"(.+?)"').findall(url)[0]
            except:	pass
            try:	qURL = re.compile('"hqURL":"(.+?)"').findall(url)[0]
            except:	pass
            qURL = urllib.unquote(qURL) + '&redirect=0'
            url = getUrl(qURL).result
            return url
        except:
            return

    def veoh(self, url):
        try:
            url = 'http://www.flashvideodownloader.org/download.php?u=%s' % url
            result = getUrl(url).result
            url = common.parseDOM(result, "div", attrs = { "class": "mod_download" })[0]
            url = common.parseDOM(url, "a", ret="href")[0]
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

main()