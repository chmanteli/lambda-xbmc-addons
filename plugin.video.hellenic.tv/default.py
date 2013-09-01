# -*- coding: utf-8 -*-

'''
    hellenic tv XBMC Addon
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

import urllib,urllib2,re,os,xbmc,xbmcplugin,xbmcgui,xbmcaddon
import threading, datetime, time, shutil
import xmlwriter as XMLWriter
from operator import itemgetter

try:	import CommonFunctions
except:	import commonfunctionsdummy as CommonFunctions
try:	import json
except:	import simplejson as json


language			= xbmcaddon.Addon().getLocalizedString
setSetting			= xbmcaddon.Addon().setSetting
getSetting			= xbmcaddon.Addon().getSetting
addonName			= xbmcaddon.Addon().getAddonInfo("name")
addonVersion		= xbmcaddon.Addon().getAddonInfo("version")
addonId				= xbmcaddon.Addon().getAddonInfo("id")
addonPath			= xbmcaddon.Addon().getAddonInfo("path")
addonIcon			= xbmc.translatePath(os.path.join(addonPath,'icon.png'))
addonFanart			= xbmc.translatePath(os.path.join(addonPath,'fanart.jpg'))
dataPath			= xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
Window				= xbmcgui.Window(10000)
Dialog				= xbmcgui.Dialog()
common				= CommonFunctions


class main:
    def __init__(self):
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
        try:		channel = urllib.unquote_plus(params["channel"])
        except:		channel = None

        if action	==	None:						channels().get()
        elif action	== 'play_video':				player().play(channel)
        elif action == 'epg_menu':					utils().epg(channel)
        elif action == 'refresh':					utils().refresh()

        xbmcplugin.setContent(int(sys.argv[1]), 'Episodes')
        xbmcplugin.setPluginFanart(int(sys.argv[1]), addonFanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

class getUrl(object):
    def __init__(self, url, fetch=True, mobile=False, proxy=None, referer=None, cookie=None):
        if not proxy is None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
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
        response = urllib2.urlopen(request)
        if fetch == True:
            result = response.read()
        else:
            result = response.geturl()
        response.close()
        self.result = result

class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

class utils:
    xmltvFile = "%s/xmltv.xml" % addonPath

    def refresh(self):
        xbmc.executebuiltin("Container.Refresh")

    def check_addon(self, id):
        check = xbmcaddon.Addon(id=id).getAddonInfo("name")
        if not check == addonName: return True

    def epg(self, channel):
        try:
            epgList = []
            channel = channel.replace('_',' ')

            now = datetime.datetime.now()
            now = '%04d' % now.year + '%02d' % now.month + '%02d' % now.day + '%02d' % now.hour + '%02d' % now.minute + '%02d' % now.second

            file = open(self.xmltvFile,'r')
            xmltvData = file.read()
            file.close()

            programmes = re.compile('(<programme.+?</programme>)').findall(xmltvData)

            for programme in programmes:
                try:
                    channel2 = common.parseDOM(programme, "programme", ret="channel")[0]

                    if channel == channel2:
                        start = common.parseDOM(programme, "programme", ret="start")[0]
                        start = re.split('\s+', start)[0]
                        stop = common.parseDOM(programme, "programme", ret="stop")[0]
                        stop = re.split('\s+', stop)[0]

                        if (int(start) <= int(now) <= int(stop)) or (int(start) >= int(now)):
                            start = datetime.datetime(*time.strptime(start, "%Y%m%d%H%M%S")[:6])
                            title = common.parseDOM(programme, "title")[0]
                            title = common.replaceHTMLCodes(title)
                            if channel == title :
                                title = language(30403).encode("utf-8")
                            epg = "%s    %s" % (str(start), title)
                            epgList.append(epg)

                except:
                    pass

        except:
            pass

        Dialog.select('%s - %s' % (language(30402).encode("utf-8"), channel), epgList)
        return

class channels:
    channelsFile = "%s/channels.xml" % addonPath
    xmltvFile = "%s/xmltv.xml" % addonPath
    logoFolder = "%s/resources/logos" % addonPath

    def get(self):
        Notification = "Notification(%s,%s, 3000)"
        if not (os.path.isfile(self.xmltvFile)) and not (Window.getProperty("htv_Service_Running") == ''):
            xbmc.executebuiltin(Notification % (addonName, language(30301).encode("utf-8")))

        epgList = channels().epgList()
        channelList = channels().channelList(epgList)
        total = len(channelList)

        for item in channelList:
            name = item['name']
            epg = item['epg']
            channels().add(total, name, epg)

        return

    def channelList(self, epgList):
        channelList = []

        try:
            file = open(self.channelsFile,'r')
            result = file.read()
            file.close()
        except:
            return

        channels = common.parseDOM(result, "channel", attrs = { "active": "True" })

        for channel in channels:
            try:
                name = common.parseDOM(channel, "name")[0]
                type = common.parseDOM(channel, "type")[0]
                url = common.parseDOM(channel, "url")[0]
                url = common.replaceHTMLCodes(url)
                epgList_filter = [i for i in epgList if name == i['channel']]
                if epgList_filter == []:
                    epg = common.parseDOM(channel, "epg")[0]
                    epg = "[B][%s] - %s[/B]\n%s" % (language(30450), name, language(int(epg)))
                    epg = epg.encode('utf-8')
                else:
                    epg = [i['epg'] for i in epgList_filter][0]

                channelList.append({'name': name, 'url': url, 'epg': epg, 'type': type})
            except:
                pass

        return channelList

    def epgList(self):
        try:
            epgList = []

            now = datetime.datetime.now()
            now = '%04d' % now.year + '%02d' % now.month + '%02d' % now.day + '%02d' % now.hour + '%02d' % now.minute + '%02d' % now.second

            file = open(self.xmltvFile,'r')
            xmltvData = file.read()
            file.close()

            programmes = re.compile('(<programme.+?</programme>)').findall(xmltvData)

            for programme in programmes:
                try:
                    start = re.compile('start="(.+?)"').findall(programme)[0]
                    start = re.split('\s+', start)[0]
                    stop = re.compile('stop="(.+?)"').findall(programme)[0]
                    stop = re.split('\s+', stop)[0]
                    if int(start) <= int(now) <= int(stop):
                        channel = common.parseDOM(programme, "programme", ret="channel")[0]
                        title = common.parseDOM(programme, "title")[0]
                        title = common.replaceHTMLCodes(title).encode('utf-8')
                        desc = common.parseDOM(programme, "desc")[0]
                        desc = common.replaceHTMLCodes(desc).encode('utf-8')
                        epg = "[B][%s] - %s[/B]\n%s" % ('ÔÙÑÁ'.decode('iso-8859-7').encode('utf-8'), title, desc)
                        epgList.append({'channel': channel, 'epg': epg})
                except:
                    pass

        except:
            pass

        return epgList

    def add(self, total, name, epg):
        if getSetting(name) == "false": return

        channel = name.replace(' ','_')
        syschannel = urllib.quote_plus(channel)
        image = '%s/%s.png' % (self.logoFolder, name)
        u = '%s?action=play_video&channel=%s' % (sys.argv[0], syschannel)

        cm = []
        cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=epg_menu&channel=%s)' % (sys.argv[0], syschannel)))
        cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=refresh)' % (sys.argv[0])))

        item = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Duration": "1440", "Plot": epg } )
        item.setProperty("IsPlayable", "true")
        item.setProperty( "Video", "true" )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems(cm, replaceItems=False)

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total)
        return

class player:
    logoFolder = "%s/resources/logos" % addonPath
    fallback = "%s/resources/fallback/fallback.mp4" % addonPath
    akamaiProxy = "%s/akamaisecurehd.py" % addonPath

    def play(self, channel):
        epgList = channels().epgList()
        channelList = channels().channelList(epgList)
        channel = channel.replace('_',' ')

        channelList_filter = [i for i in channelList if channel == i['name']]

        for item in channelList_filter:
            name = item['name']
            epg = item['epg']
            type = item['type']
            url = item['url']

        if channelList_filter == []:
            Dialog.ok(addonName, language(30351).encode("utf-8"), language(30352).encode("utf-8"))
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=self.fallback))
            return

        playerDict = {
            ''					:	player().direct,
            'hls'				:	player().hls,
            'visionip'			:	player().visionip,
            'madtv'				:	player().madtv,
            'viiideo'			:	player().viiideo,
            'dailymotion'		:	player().dailymotion,
            'livestream'		:	player().livestream,
            'ustream'			:	player().ustream,
            'veetle'			:	player().veetle,
            'justin'			:	player().justin
        }

        url = playerDict[type](url)
        if url is None: url = self.fallback

        image = '%s/%s.png' % (self.logoFolder, name)

        if not xbmc.getInfoLabel('ListItem.Plot') == '' : epg = xbmc.getInfoLabel('ListItem.Plot')

        item = xbmcgui.ListItem(path=url, iconImage=image, thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Duration": "1440", "Plot": epg } )
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        return

    def direct(self, url):
        return url

    def hls(self, url):
        try:
            result = common.fetchPage({"link": url})
            if "EXTM3U" in result["content"]: return url
        except:
            return

    def visionip(self, url):
        try:
            cookie = 'http://tvnetwork.new.visionip.tv/Hellenic_TV'
            result = getUrl(url,cookie=cookie).result
            result = common.parseDOM(result, "entry")[0]
            streamer = common.parseDOM(result, "param", ret="value")[0]
            playPath = common.parseDOM(result, "ref", ret="href")[0]
            url = '%s/%s live=1 timeout=10' % (streamer, playPath)
            return url
        except:
            return

    def madtv(self, url):
        try:
            result = common.fetchPage({"link": url})
            url = re.compile('youtube.com/embed/(.+?)"').findall(result["content"])[0]
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
            if utils().check_addon('plugin.video.youtube') is None:
                Dialog.ok(addonName, language(30353).encode("utf-8"), language(30354).encode("utf-8"))
            else:
                return url
        except:
            return

    def viiideo(self, url):
        try:
            result = common.fetchPage({"link": url})
            url = re.compile("ipadUrl.+?'http://(.+?)/playlist[.]m3u8'").findall(result["content"])[0]
            url = 'rtmp://%s live=1 timeout=10' % url
            return url
        except:
            return

    def dailymotion(self, url):
        try:
            result = common.fetchPage({"link": url})
            url = re.compile('"flashvars".+?value="(.+?)"').findall(result["content"])[0]
            url = urllib.unquote(url).decode('utf-8').replace('\\/', '/')
            try:	qURL = re.compile('"ldURL":"(.+?)"').findall(url)[0]
            except:	pass
            try:	qURL = re.compile('"sdURL":"(.+?)"').findall(url)[0]
            except:	pass
            try:	qURL = re.compile('"hqURL":"(.+?)"').findall(url)[0]
            except:	pass
            qURL += '&redirect=0'
            url = common.fetchPage({"link": qURL})["content"]
            url = '%s live=1 timeout=10' % url
            return url
        except:
            return

    def livestream(self, url):
        try:
            name = url.split("/")[-1]
            url = 'http://x%sx.api.channel.livestream.com/3.0/getstream.json' % name
            result = common.fetchPage({"link": url})
            isLive = str(result["content"].find('isLive":true'))
            if isLive == '-1': return
            url = re.compile('"httpUrl".+?"(.+?)"').findall(result["content"])[0]
            return url
        except:
            return

    def ustream(self, url):
        try:
            try:
                result = common.fetchPage({"link": url})
                id = re.compile('ustream.tv/embed/(.+?)"').findall(result["content"])[0]
            except:
                id = url.split("/embed/")[-1]
            url = 'http://iphone-streaming.ustream.tv/uhls/%s/streams/live/iphone/playlist.m3u8' % id
            for i in range(1, 51):
                result = common.fetchPage({"link": url})
                if "EXT-X-STREAM-INF" in result["content"]: return url
                if not "EXTM3U" in result["content"]: return
            return
        except:
            return

    def veetle(self, url):
        try:
            xbmc.executebuiltin('RunScript(%s)' % self.akamaiProxy)
            name = url.split("#")[-1]
            url = 'http://www.veetle.com/index.php/channel/ajaxStreamLocation/%s/flash' % name
            result = common.fetchPage({"link": url})
            try: import json
            except: import simplejson as json
            url = json.loads(result["content"])
            import base64
            url = base64.encodestring(url['payload']).replace('\n', '')
            url = 'http://127.0.0.1:64653/veetle/%s' % url
            return url
        except:
            return

    def justin(self, url):
        try:
            streams = []
            pageUrl = url
            name = url.split("/")[-1]
            swfUrl = 'http://www.justin.tv/widgets/live_embed_player.swf?channel=%s' % name
            swfUrl = getUrl(swfUrl,fetch=False,referer=url).result
            data = 'http://usher.justin.tv/find/%s.json?type=any&group=&channel_subscription=' % name
            data = getUrl(data,referer=url).result
            try: import json
            except: import simplejson as json
            data = json.loads(data)
            for i in data:
                token = None
                token = ' jtv='+i['token'].replace('\\','\\5c').replace(' ','\\20').replace('"','\\22')
                if i['needed_info'] == 'private': token = 'private'
                rtmp = i['connect']+'/'+i['play']
                try:
                    if i['type'] == "live": streamer = rtmp+token
                    else: streams.append((i['type'], rtmp, token))
                except:
                    continue
            if len(streams) < 1: pass
            elif len(streams) == 1: streamer = streams[0][1]+streams[0][2]
            else:
                for i in range(len(s_type)):
                    quality = s_type[str(i)]
                    for q in streams:
                        if q[0] == quality: streamer = (q[1]+q[2])
                        else: continue
            url = '%s swfUrl=%s pageUrl=%s swfVfy=1 live=1 timeout=10' % (streamer, swfUrl, pageUrl)
            return url
        except:
            return

main()