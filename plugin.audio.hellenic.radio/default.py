# -*- coding: utf-8 -*-

'''
    hellenic radio XBMC Addon
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
try:	import CommonFunctions
except:	import commonfunctionsdummy as CommonFunctions


language			= xbmcaddon.Addon().getLocalizedString
setSetting			= xbmcaddon.Addon().setSetting
getSetting			= xbmcaddon.Addon().getSetting
addonName			= xbmcaddon.Addon().getAddonInfo("name")
addonVersion		= xbmcaddon.Addon().getAddonInfo("version")
addonId				= xbmcaddon.Addon().getAddonInfo("id")
addonPath			= xbmcaddon.Addon().getAddonInfo("path")
addonIcon			= os.path.join(addonPath,'icon.png')
addonRadios			= os.path.join(addonPath,'radios.xml')
addonFanart			= os.path.join(addonPath,'resources/fanart/1.jpg')
addonFanart2		= os.path.join(addonPath,'resources/fanart/2.jpg')
addonLogos			= os.path.join(addonPath,'resources/logos')
addonIcons			= os.path.join(addonPath,'resources/icons')
dataPath			= xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData			= os.path.join(dataPath,'views.cfg')
favData				= os.path.join(dataPath,'favourites.cfg')
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

        try:		action	= urllib.unquote_plus(params["action"])
        except:		action	= None
        try:		radio = urllib.unquote_plus(params["radio"])
        except:		radio = None
        try:		area = urllib.unquote_plus(params["area"])
        except:		area = None

        if action	==	None:						categories().get()
        elif action	== 'favourite_add':				contextMenu().favourite_add(radio, area)
        elif action	== 'favourite_delete':			contextMenu().favourite_delete(radio, area)
        elif action	== 'favourite_moveUp':			contextMenu().favourite_moveUp(radio, area)
        elif action	== 'favourite_moveDown':		contextMenu().favourite_moveDown(radio, area)
        elif action	== 'global_view':				contextMenu().global_view()
        elif action	== 'favourite_radios':			favourites().get()
        elif action	== 'all_radios':				radios().all()
        elif action	== 'international_radios':		radios().international()
        elif action	== 'eclectic_radios':			radios().eclectic()
        elif action	== 'rock_radios':				radios().rock()
        elif action	== 'greek_radios':				radios().greek()
        elif action	== 'laika_radios':				radios().laika()
        elif action	== 'sports_radios':				radios().sports()
        elif action	== 'news_radios':				radios().news()
        elif action	== 'religious_radios':			radios().religious()
        elif action	== 'traditional_radios':		radios().traditional()
        elif action	== 'attica_radios':				radios().attica()
        elif action	== 'salonica_radios':			radios().salonica()
        elif action	== 'internet_radios':			radios().internet()
        elif action	== 'aegean_radios':				radios().aegean()
        elif action	== 'epirus_radios':				radios().epirus()
        elif action	== 'thessaly_radios':			radios().thessaly()
        elif action	== 'thrace_radios':				radios().thrace()
        elif action	== 'ionian_radios':				radios().ionian()
        elif action	== 'crete_radios':				radios().crete()
        elif action	== 'cyprus_radios':				radios().cyprus()
        elif action	== 'macedonia_radios':			radios().macedonia()
        elif action	== 'peloponnese_radios':		radios().peloponnese()
        elif action	== 'centralgreece_radios':		radios().centralgreece()
        elif action	== 'play':						player().run(radio, area)

        viewDict = {
            'skin.confluence'	: 500,	'skin.aeon.nox'		: 512,	'skin.back-row'			: 51,
            'skin.bello'		: 56,	'skin.carmichael'	: 50,	'skin.diffuse'			: 58,
            'skin.droid'		: 55,	'skin.metropolis'	: 58,	'skin.pm3-hd'			: 53,
            'skin.rapier'		: 63,	'skin.re-touched'	: 500,	'skin.simplicity'		: 500,
            'skin.transparency'	: 53,	'skin.xeebo'		: 52,	'skin.xperience1080'	: 50
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

    def favList(self, favList):
        total = len(favList)
        count = 0
        for i in favList:
            try:
                name, band, genre, area, desc, url = i['name'], i['band'], i['genre'], i['area'], i['desc'], i['url']
                sysname, sysarea = urllib.quote_plus(name.replace(' ','_')), urllib.quote_plus(area.replace(' ','_'))
                image = '%s/%s/%s.png' % (addonLogos, area, name)
                u = '%s?action=play&radio=%s&area=%s' % (sys.argv[0], sysname, sysarea)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&radio=%s&area=%s)' % (sys.argv[0], sysname, sysarea)))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&radio=%s&area=%s)' % (sys.argv[0], sysname, sysarea)))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&radio=%s&area=%s)' % (sys.argv[0], sysname, sysarea)))

                item = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
                item.setInfo( type="Music", infoLabels={ "Title": name, "Label": name, "Album": name, "Artist": band, "Genre": genre, "Comment": desc, "Duration": "1440" } )
                item.setProperty("IsPlayable", "true")
                item.setProperty( "Music", "true" )
                item.setProperty("Album_Label", area)
                item.setProperty("Album_Description", desc)
                count = count + 1
                if count % 2 == 0:
                    item.setProperty("Fanart_Image", addonFanart2)
                else:
                    item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

    def catList(self, catList):
        total = len(catList)
        count = 0
        for i in catList:
            try:
                name, desc, action = language(i['name']).encode("utf-8"), language(i['desc']).encode("utf-8"), i['action']
                image = '%s/%s' % (addonIcons, i['image'])
                u = '%s?action=%s' % (sys.argv[0], action)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Music", infoLabels={ "Title": name, "Label": name, "Album": name } )
                item.setProperty("Album_Description", desc)
                count = count + 1
                if count % 2 == 0:
                    item.setProperty("Fanart_Image", addonFanart2)
                else:
                    item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def radioList(self, radioList):
        file = open(favData,'r')
        favRead = file.read()
        file.close()

        total = len(radioList)
        count = 0
        for i in radioList:
            try:
                name, band, genre, area, desc, url = i['name'], i['band'], i['genre'], i['area'], i['desc'], i['url']
                sysname, sysarea = urllib.quote_plus(name.replace(' ','_')), urllib.quote_plus(area.replace(' ','_'))
                image = '%s/%s/%s.png' % (addonLogos, area, name)
                u = '%s?action=play&radio=%s&area=%s' % (sys.argv[0], sysname, sysarea)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                favMatch = '"%s"|"%s"' % (name, area)
                if not favMatch in favRead:
                    cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&radio=%s&area=%s)' % (sys.argv[0], sysname, sysarea)))
                else:
                    cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&radio=%s&area=%s)' % (sys.argv[0], sysname, sysarea)))

                item = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
                item.setInfo( type="Music", infoLabels={ "Title": name, "Label": name, "Album": name, "Artist": band, "Genre": genre, "Comment": desc, "Duration": "1440" } )
                item.setProperty("IsPlayable", "true")
                item.setProperty( "Music", "true" )
                item.setProperty("Album_Label", area)
                item.setProperty("Album_Description", desc)
                count = count + 1
                if count % 2 == 0:
                    item.setProperty("Fanart_Image", addonFanart2)
                else:
                    item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

class contextMenu:
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

    def favourite_add(self, radio, area):
        try:
            index().container_refresh()
            name = radio.replace('_',' ')
            area = area.replace('_',' ')
            file = open(favData, 'a+')
            file.write('"%s"|"%s"\n' % (name, area))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"))
        except:
            return

    def favourite_delete(self, radio, area):
        try:
            index().container_refresh()
            name = radio.replace('_',' ')
            area = area.replace('_',' ')
            file = open(favData,'r')
            read = file.read()
            file.close()
            read = read.replace('"%s"|"%s"' % (name, area),'')
            file = open(favData, 'w')
            for line in re.compile('(".+?\n)').findall(read):
                file.write(line)
            file.close()
            index().infoDialog(language(30304).encode("utf-8"))
        except:
            return

    def favourite_moveUp(self, radio, area):
        try:
            index().container_refresh()
            list = []
            name = radio.replace('_',' ')
            area = area.replace('_',' ')
            file = open(favData,'r')
            read = file.read()
            file.close()
            for line in re.compile('(".+?)\n').findall(read):
                list.append(line)
            i = list.index('"%s"|"%s"' % (name, area))
            if i == 0 : return
            list[i], list[i-1] = list[i-1], list[i]
            file = open(favData, 'w')
            for line in list:
                file.write('%s\n' % (line))
            file.close()
            index().infoDialog(language(30305).encode("utf-8"))
        except:
            return

    def favourite_moveDown(self, radio, area):
        try:
            index().container_refresh()
            list = []
            name = radio.replace('_',' ')
            area = area.replace('_',' ')
            file = open(favData,'r')
            read = file.read()
            file.close()
            for line in re.compile('(".+?)\n').findall(read):
                list.append(line)
            i = list.index('"%s"|"%s"' % (name, area))
            if i+1 == len(list): return
            list[i], list[i+1] = list[i+1], list[i]
            file = open(favData, 'w')
            for line in list:
                file.write('%s\n' % (line))
            file.close()
            index().infoDialog(language(30306).encode("utf-8"))
        except:
            return

class radioList:
    def __init__(self):
        descDict = {
            ''					:	'',
            'International'		:	language(30721).encode("utf-8"),
            'Eclectic'			:	language(30722).encode("utf-8"),
            'Rock'				:	language(30723).encode("utf-8"),
            'Greek'				:	language(30724).encode("utf-8"),
            'Laika'				:	language(30725).encode("utf-8"),
            'Sports'			:	language(30726).encode("utf-8"),
            'News'				:	language(30727).encode("utf-8"),
            'Religious'			:	language(30728).encode("utf-8"),
            'Traditional'		:	language(30729).encode("utf-8")
        }

        try:
            radioList = []
            file = open(addonRadios,'r')
            result = file.read()
            file.close()
            radios = common.parseDOM(result, "radio", attrs = { "active": "True" })
        except:
            return
        for radio in radios:
            try:
                name = common.parseDOM(radio, "name")[0]
                band = common.parseDOM(radio, "band")[0]
                genre = common.parseDOM(radio, "genre")[0]
                area = common.parseDOM(radio, "area")[0]
                desc = descDict[genre]
                desc = common.replaceHTMLCodes(desc)
                url = common.parseDOM(radio, "url")[0]
                url = common.replaceHTMLCodes(url)
                radioList.append({'name': name, 'band': band, 'genre': genre, 'area': area, 'desc': desc, 'url': url})
            except:
                pass

        self.radioList = radioList

class favourites:
    def __init__(self):
        self.list = radioList().radioList

    def get(self):
        favList = []
        file = open(favData,'r')
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"').findall(read)
        for name, area in match:
            favList += [i for i in self.list if name == i['name'] and area == i['area']]
        index().favList(favList)

class categories:
    def get(self):
        catList = []
        catList.append({'name': 30501, 'desc': 30601, 'image': '01.png', 'action': 'favourite_radios'})
        catList.append({'name': 30502, 'desc': 30602, 'image': '02.png', 'action': 'all_radios'})
        catList.append({'name': 30521, 'desc': 30621, 'image': '03.png', 'action': 'international_radios'})
        catList.append({'name': 30522, 'desc': 30622, 'image': '04.png', 'action': 'eclectic_radios'})
        catList.append({'name': 30523, 'desc': 30623, 'image': '05.png', 'action': 'rock_radios'})
        catList.append({'name': 30524, 'desc': 30624, 'image': '06.png', 'action': 'greek_radios'})
        catList.append({'name': 30525, 'desc': 30625, 'image': '07.png', 'action': 'laika_radios'})
        catList.append({'name': 30526, 'desc': 30626, 'image': '08.png', 'action': 'sports_radios'})
        catList.append({'name': 30527, 'desc': 30627, 'image': '09.png', 'action': 'news_radios'})
        catList.append({'name': 30528, 'desc': 30628, 'image': '10.png', 'action': 'religious_radios'})
        catList.append({'name': 30529, 'desc': 30629, 'image': '11.png', 'action': 'traditional_radios'})
        catList.append({'name': 30541, 'desc': 30641, 'image': '12.png', 'action': 'attica_radios'})
        catList.append({'name': 30542, 'desc': 30642, 'image': '13.png', 'action': 'salonica_radios'})
        catList.append({'name': 30543, 'desc': 30643, 'image': '14.png', 'action': 'internet_radios'})
        catList.append({'name': 30544, 'desc': 30644, 'image': '15.png', 'action': 'aegean_radios'})
        catList.append({'name': 30545, 'desc': 30645, 'image': '16.png', 'action': 'epirus_radios'})
        catList.append({'name': 30546, 'desc': 30646, 'image': '17.png', 'action': 'thessaly_radios'})
        catList.append({'name': 30547, 'desc': 30647, 'image': '18.png', 'action': 'thrace_radios'})
        catList.append({'name': 30548, 'desc': 30648, 'image': '19.png', 'action': 'ionian_radios'})
        catList.append({'name': 30549, 'desc': 30649, 'image': '20.png', 'action': 'crete_radios'})
        catList.append({'name': 30550, 'desc': 30650, 'image': '21.png', 'action': 'cyprus_radios'})
        catList.append({'name': 30551, 'desc': 30651, 'image': '22.png', 'action': 'macedonia_radios'})
        catList.append({'name': 30552, 'desc': 30652, 'image': '23.png', 'action': 'peloponnese_radios'})
        catList.append({'name': 30553, 'desc': 30653, 'image': '24.png', 'action': 'centralgreece_radios'})
        index().catList(catList)

class radios:
    def __init__(self):
        self.list = radioList().radioList

    def all(self):
        index().radioList(self.list)

    def international(self):
        filter = [i for i in self.list if i['genre'] == 'International']
        index().radioList(filter)

    def eclectic(self):
        filter = [i for i in self.list if i['genre'] == 'Eclectic']
        index().radioList(filter)

    def rock(self):
        filter = [i for i in self.list if i['genre'] == 'Rock']
        index().radioList(filter)

    def greek(self):
        filter = [i for i in self.list if i['genre'] == 'Greek']
        index().radioList(filter)

    def laika(self):
        filter = [i for i in self.list if i['genre'] == 'Laika']
        index().radioList(filter)

    def sports(self):
        filter = [i for i in self.list if i['genre'] == 'Sports']
        index().radioList(filter)

    def news(self):
        filter = [i for i in self.list if i['genre'] == 'News']
        index().radioList(filter)

    def religious(self):
        filter = [i for i in self.list if i['genre'] == 'Religious']
        index().radioList(filter)

    def traditional(self):
        filter = [i for i in self.list if i['genre'] == 'Traditional']
        index().radioList(filter)

    def attica(self):
        filter = [i for i in self.list if i['area'] == 'Attica']
        index().radioList(filter)

    def salonica(self):
        filter = [i for i in self.list if i['area'] == 'Salonica']
        index().radioList(filter)

    def internet(self):
        filter = [i for i in self.list if i['area'] == 'Internet']
        index().radioList(filter)

    def aegean(self):
        filter = [i for i in self.list if i['area'] == 'Aegean']
        index().radioList(filter)

    def epirus(self):
        filter = [i for i in self.list if i['area'] == 'Epirus']
        index().radioList(filter)

    def thessaly(self):
        filter = [i for i in self.list if i['area'] == 'Thessaly']
        index().radioList(filter)

    def thrace(self):
        filter = [i for i in self.list if i['area'] == 'Thrace']
        index().radioList(filter)

    def ionian(self):
        filter = [i for i in self.list if i['area'] == 'Ionian']
        index().radioList(filter)

    def crete(self):
        filter = [i for i in self.list if i['area'] == 'Crete']
        index().radioList(filter)

    def cyprus(self):
        filter = [i for i in self.list if i['area'] == 'Cyprus']
        index().radioList(filter)

    def macedonia(self):
        filter = [i for i in self.list if i['area'] == 'Macedonia']
        index().radioList(filter)

    def peloponnese(self):
        filter = [i for i in self.list if i['area'] == 'Peloponnese']
        index().radioList(filter)

    def centralgreece(self):
        filter = [i for i in self.list if i['area'] == 'Central Greece']
        index().radioList(filter)

class player:
    def __init__(self):
        self.list = radioList().radioList

    def run(self, radio, area):
        try:
            xbmc.Player().stop()
            xbmc.PlayList(xbmc.PLAYLIST_MUSIC).clear()
            name = radio.replace('_',' ')
            area = area.replace('_',' ')

            i = [x for x in self.list if name == x['name'] and area == x['area']]
            name, band, genre, area, desc, url = i[0]['name'], i[0]['band'], i[0]['genre'], i[0]['area'], i[0]['desc'], i[0]['url']
            image = '%s/%s/%s.png' % (addonLogos, area, name)

            if url.startswith('http://iphone-streaming.ustream.tv'):
                url = self.ustream(url)
            elif url.startswith('http://www.youtube.com/user/'):
                url = self.youtubelive(url)
            elif url.startswith('http://www.youtube.com'):
                url = self.youtube(url)

            if url is None: return
            item = xbmcgui.ListItem(path=url, iconImage=image, thumbnailImage=image)
            item.setInfo( type="Video", infoLabels={ "Title": "" } )
            item.setInfo( type="Music", infoLabels={ "Title": name, "Label": name, "Album": name, "Artist": band, "Genre": genre, "Comment": desc, "Duration": "1440" } )
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        except:
            index().okDialog(language(30351).encode("utf-8"), language(30352).encode("utf-8"))
            return

    def youtube(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30353).encode("utf-8"), language(30354).encode("utf-8"))
                return
            url = url.split("?v=")[-1]
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
            return url
        except:
            return

    def youtubelive(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30353).encode("utf-8"), language(30354).encode("utf-8"))
                return
            url += '/videos?view=2&flow=grid'
            result = getUrl(url).result
            url = re.compile('"/watch[?]v=(.+?)"').findall(result)[0]
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
            return url
        except:
            return

    def ustream(self, url):
        try:
            for i in range(1, 51):
                result = getUrl(url).result
                if "EXT-X-STREAM-INF" in result: return url
                if not "EXTM3U" in result: return
        except:
            return

main()