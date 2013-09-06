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
        while (not xbmc.abortRequested):
            epg().get()
            count = 60
            while (not xbmc.abortRequested) and count > 0:
                count -= 1
                time.sleep(1)

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

class epg:
    dates, dummyData, oteData, cytaData = [], [], [], []
    channelsFile = "%s/channels.xml" % addonPath
    stringsFile = "%s/resources/language/Greek/strings.xml" % addonPath
    logoFolder = "%s/resources/logos" % addonPath
    xmltvFile = "%s/xmltv.xml" % addonPath
    tmpFolder = "%s/tmp" % dataPath
    tmpFile = "%s/tmp/xmltv.xml" % dataPath

    def get(self):
        if xbmc.abortRequested == True: sys.exit()
        try:
            t1 = datetime.datetime.utcfromtimestamp(os.path.getmtime(self.xmltvFile))
            t2 = datetime.datetime.utcnow()
            update = abs(t2 - t1) > datetime.timedelta(hours=24)
            if update is False: return
        except:
            pass

        if Window.getProperty('htv_Service_Running') == 'true': return
        Window.setProperty('htv_Service_Running', 'true')

        try: shutil.rmtree(self.tmpFolder)
        except: pass
        try: os.makedirs(self.tmpFolder)
        except: pass

        epg().get_dates()
        epg().dummy_data()

        threads = []
        threads.append(Thread(epg().ote_data))
        threads.append(Thread(epg().cyta_data))
        [i.start() for i in threads]
        [i.join() for i in threads]

        epg().ote_programme("MEGA", "90")
        epg().ote_programme("ANT1", "150")
        epg().ote_programme("STAR", "98")
        epg().ote_programme("ALPHA", "132")
        epg().ote_programme("SKAI", "120")
        epg().ote_programme("MACEDONIA TV", "152")
        epg().ote_programme("EDT", "593")
        epg().ote_programme("BOYLH TV", "119")
        epg().ote_programme("EURONEWS", "19")
        epg().ote_programme("NICKELODEON", "117")
        #epg().ote_programme("MTV", "121")
        epg().ote_programme("MAD TV", "144")
        epg().ote_programme("KONTRA CHANNEL", "44")
        epg().ote_programme("EXTRA 3", "135")
        epg().ote_programme("ART CHANNEL", "156")
        epg().ote_programme("GR TV", "157")
        epg().ote_programme("BLUE SKY", "153")
        #epg().ote_programme("SBC TV", "136")
        epg().ote_programme("TV 100", "137")
        epg().ote_programme("4E TV", "133")
        epg().ote_programme("STAR KENTRIKIS ELLADOS", "139")
        epg().ote_programme("EPIRUS TV1", "145")
        epg().ote_programme("KRITI TV", "138")
        epg().ote_programme("DIKTYO TV", "146")
        epg().ote_programme("DELTA TV", "147")

        epg().cyta_programme("MEGA CYPRUS", "2")
        epg().cyta_programme("ANT1 CYPRUS", "3")
        epg().cyta_programme("SIGMA", "4")
        #epg().cyta_programme("TV PLUS", "5")
        #epg().cyta_programme("EXTRA TV", "6")
        epg().cyta_programme("CAPITAL", "7")

        for channel in self.dummyData:
            try:
                channel = channel["channel"]
                programme = "%s/%s.xml" % (self.tmpFolder, channel)
                if not os.path.isfile(programme):
                    epg().dummy_programme(channel)
            except:
                pass

        epg().xmltv_creator()

        try: shutil.copy(self.tmpFile, self.xmltvFile)
        except: pass
        try: shutil.rmtree(self.tmpFolder)
        except: pass

        Window.clearProperty('htv_Service_Running')

    def get_dates(self):
        if xbmc.abortRequested == True: sys.exit()
        try:
            now = epg().greek_datetime()
            today = datetime.date(now.year, now.month, now.day)
            for i in range(0, 3):
                d = today + datetime.timedelta(days=i)
                self.dates.append(str(d))
        except:
            return

    def dummy_data(self):
        if xbmc.abortRequested == True: sys.exit()
        try:
            file = open(self.channelsFile,'r')
            channelData = file.read()
            file.close()
            file = open(self.stringsFile,'r')
            stringsData = file.read()
            file.close()
        except:
            return

        channels = common.parseDOM(channelData, "channel", attrs = { "active": "True" })

        for channel in channels:
            epg = common.parseDOM(channel, "epg")[0]
            epg = common.parseDOM(stringsData, "string", attrs = { "id": epg })[0]
            channel = common.parseDOM(channel, "name")[0]
            self.dummyData.append({'channel': channel, 'epg': epg})

    def ote_data(self):
        if xbmc.abortRequested == True: sys.exit()
        threads = []
        for date in self.dates:
            date = date.replace('-','')
            url = 'http://otetv.ote.gr/otetv_program/ProgramListServlet?t=sat&d=%s' % date
            threads.append(Thread(epg().ote_data2, date, url))
        [i.start() for i in threads]
        [i.join() for i in threads]

    def ote_data2(self, date, url):
        if xbmc.abortRequested == True: sys.exit()
        try:
            result = getUrl(url).result
            self.oteData.append({'date': date, 'value': result})
        except:
            return

    def cyta_data(self):
        if xbmc.abortRequested == True: sys.exit()
        threads = []
        for i in range(0, 3):
            url = 'http://data.cytavision.com.cy/epg/?category=3&lang=el&day=%s' % str(i)
            threads.append(Thread(epg().cyta_data2, self.dates[i].replace('-',''), url))
        [i.start() for i in threads]
        [i.join() for i in threads]

    def cyta_data2(self, date, url):
        if xbmc.abortRequested == True: sys.exit()
        try:
            result = getUrl(url).result
            result = result.decode('iso-8859-7').encode('utf-8')
            self.cytaData.append({'date': date, 'value': result})
        except:
            return

    def dummy_programme(self, channel):
        if xbmc.abortRequested == True: sys.exit()
        programmeList = []

        desc = [i for i in self.dummyData if channel == i['channel']]
        desc = desc[0]['epg']

        for date in self.dates:
            for i in range(0, 2400, 1200):
                start = date.replace('-','') + '%04d' % i + '00'
                start = epg().start_processor(start)
                if channel == "RIK SAT":
                    title = 'ƒœ—’÷œ—… œ —… '.decode('iso-8859-7')
                elif channel == "NICKELODEON+":
                    title = '–¡…ƒ… œ –—œ√—¡ÃÃ¡'.decode('iso-8859-7')
                elif channel == "MUSIC TV":
                    title = 'Ãœ’”… œ –—œ√—¡ÃÃ¡'.decode('iso-8859-7')
                elif channel == "GREEK CINEMA":
                    title = '≈ÀÀ«Õ… « ‘¡…Õ…¡'.decode('iso-8859-7')
                elif channel == "CY SPORTS":
                    title = '¡»À«‘… œ –—œ√—¡ÃÃ¡'.decode('iso-8859-7')
                elif channel == "ODIE TV":
                    title = '…––œƒ—œÃ…≈”'.decode('iso-8859-7')
                elif channel == "SMILE TV":
                    title = '–¡…ƒ… œ –—œ√—¡ÃÃ¡'.decode('iso-8859-7')
                elif channel == "GNOMI TV":
                    title = 'Ãœ’”… œ –—œ√—¡ÃÃ¡'.decode('iso-8859-7')
                else:
                    title = channel
                programmeList.append({'start': start, 'title': title, 'desc': desc})

        epg().programme_creator(channel, programmeList)

    def ote_programme(self, channel, id):
        if xbmc.abortRequested == True: sys.exit()
        programmes = []
        programmeList = []

        for data in self.oteData:
            try:
                dataList = []
                date = data["date"]
                data = data["value"]
                data = json.loads(data)
                data = data["titles"]
                data = data[id]
                data = data.iteritems()
                [dataList.append({'key': key, 'date': date, 'value': value}) for key, value in data]
                dataList = sorted(dataList, key=itemgetter('key'))
                programmes += dataList
            except:
                pass

        for programme in programmes:
            try:
                date = programme["date"]
                programme = programme["value"]
                start = programme["start"].replace(':','')
                start = date + str('%04d' % int(start)) + '00'
                start = epg().start_processor(start)
                title = programme["title"]
                title = epg().title_prettify(title)
                subtitle = programme["category"]
                desc = programme["desc"].split("<br/>")[-1]
                desc = epg().desc_prettify(desc)
                programmeList.append({'start': start, 'title': title, 'desc': desc})
            except:
                pass

        programmeList = sorted(programmeList, key=itemgetter('start'))
        epg().programme_creator(channel, programmeList)

    def cyta_programme(self, channel, id):
        if xbmc.abortRequested == True: sys.exit()
        programmes = []
        programmeList = []

        for data in self.cytaData:
            try:
                dataList = []
                date = data["date"]
                data = data["value"]
                data = common.parseDOM(data, "div", attrs = { "class": "epgrow clearfix" })[int(id)]
                data = common.parseDOM(data, "div", attrs = { "class": "program" })
                [dataList.append({'date': date, 'value': value}) for value in data]
                programmes += dataList
            except:
                pass

        for programme in programmes:
            try:
                date = programme["date"]
                programme = programme["value"]
                title = common.parseDOM(programme, "span", attrs = { "class": "program_title" })[0]
                title = epg().title_prettify(title)
                start = common.parseDOM(programme, "h4")[0]
                start = re.split('\s+', start)[0]
                start = start.replace(':','')
                start = date + str('%04d' % int(start)) + '00'
                start = epg().start_processor(start)
                desc = common.parseDOM(programme, "div", attrs = { "class": "data" })[0]
                desc = desc.split("</h4>")[-1]
                desc = epg().desc_prettify(desc)
                programmeList.append({'start': start, 'title': title, 'desc': desc})
            except:
                pass

        programmeList = sorted(programmeList, key=itemgetter('start'))
        epg().programme_creator(channel, programmeList)

    def title_prettify(self, title):
        if xbmc.abortRequested == True: sys.exit()
        acuteDict = {
            u'\u0386': u'\u0391', u'\u0388': u'\u0395', u'\u0389': u'\u0397', u'\u038A': u'\u0399',
            u'\u038C': u'\u039F', u'\u038E': u'\u03A5', u'\u038F': u'\u03A9', u'\u0390': u'\u03AA',
            u'\u03B0': u'\u03AB'
        }
        title = common.replaceHTMLCodes(title)
        title = title.strip().upper()
        for key in acuteDict:
            title = title.replace(key, acuteDict[key])
        return title

    def desc_prettify(self, desc):
        if xbmc.abortRequested == True: sys.exit()
        desc = common.replaceHTMLCodes(desc)
        desc = desc.strip()
        return desc

    def start_processor(self, start):
        if xbmc.abortRequested == True: sys.exit()
        dt1 = epg().greek_datetime()
        dt2 = datetime.datetime.now()
        dt3 = datetime.datetime.utcnow()
        dt1 = datetime.datetime(dt1.year, dt1.month, dt1.day, dt1.hour)
        dt2 = datetime.datetime(dt2.year, dt2.month, dt2.day, dt2.hour)
        dt3 = datetime.datetime(dt3.year, dt3.month, dt3.day, dt3.hour)
        start = datetime.datetime(*time.strptime(start, "%Y%m%d%H%M%S")[:6])
        if dt2 >= dt1 :
            dtd = (dt2 - dt1).seconds/60/60
            tz = (dt1 - dt3).seconds/60/60
            tz = ' +' + '%02d' % (dtd + tz) + '00'
            start = start + datetime.timedelta(hours = int(dtd))
        else:
            dtd = (dt1 - dt2).seconds/60/60
            tz = (dt1 - dt3).seconds/60/60
            tz = ' -' + '%02d' % (dtd - tz) + '00'
            start = start - datetime.timedelta(hours = int(dtd))
        start = '%04d' % start.year + '%02d' % start.month + '%02d' % start.day + '%02d' % start.hour + '%02d' % start.minute + '%02d' % start.second + tz
        return start

    def greek_datetime(self):
        if xbmc.abortRequested == True: sys.exit()
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours = 2)
        d = datetime.datetime(dt.year, 4, 1)
        dston = d - datetime.timedelta(days=d.weekday() + 1)
        d = datetime.datetime(dt.year, 11, 1)
        dstoff = d - datetime.timedelta(days=d.weekday() + 1)
        if dston <=  dt < dstoff:
            return dt + datetime.timedelta(hours = 1)
        else:
            return dt

    def programme_creator(self, channel, programmeList):
        if xbmc.abortRequested == True: sys.exit()
        w = XMLWriter.XMLWriter("%s/%s.xml" % (self.tmpFolder, channel), encoding='utf-8')

        for i in range(0, len(programmeList)):
            start = programmeList[i]['start']
            try:	stop = programmeList[i+1]['start']
            except:	stop = programmeList[i]['start']
            title = programmeList[i]['title']
            desc = programmeList[i]['desc']

            w.start("programme", channel=channel, start=start, stop=stop)
            w.element("title", title, lang="el")
            w.element("desc", desc)
            w.end()

    def xmltv_creator(self):
        if xbmc.abortRequested == True: sys.exit()
        w = XMLWriter.XMLWriter(self.tmpFile, encoding='utf-8')
        w.start("tv")
        for channel in self.dummyData:
            try:
                channel = channel["channel"]
                programme = "%s/%s.xml" % (self.tmpFolder, channel)
                if os.path.isfile(programme):
                    w.start("channel", id=channel)
                    w.element("display-name", channel)
                    w.element("icon", src="%s/%s.png" % (self.logoFolder, channel))
                    w.element("stream", "plugin://plugin.video.hellenic.tv/?action=play_video&channel=%s" % channel.replace(' ','_'))
                    w.end()
            except:
                pass
        for channel in self.dummyData:
            try:
                channel = channel["channel"]
                programme = "%s/%s.xml" % (self.tmpFolder, channel)
                r = open(programme,"r")
                w = open(self.tmpFile, 'a')
                [w.write(line) for line in r]
                r.close()
                w.close()
            except:
                pass
        w = open(self.tmpFile, 'a')
        w.write("</tv>")
        w.close()


main()