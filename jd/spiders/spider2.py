# -*-coding:UTF-8-*- 
import scrapy,random,sys,time,os,urllib,re,json,requests,chardet
reload(sys)
sys.setdefaultencoding('utf-8')

class Spider(scrapy.Spider):
    name = "gjwsearch"
    allowed_domains = ["www.gjw.com"]
    f = open('file/kw.txt','r')
    start_urls =[]
    with open('w.txt','w') as wa:
        for kw in f.readlines():
            kws='http://www.gjw.com/product/search.htm?key=%s'%urllib.quote(kw.strip())
            wa.write(kws)
            start_urls.append(kws)
    global ft
    t = time.strftime('%Y年%m月%d日')
    ft = time.strftime('%Y%m%d')
    
    if not os.path.exists('D:/scrapy/gjw'+ft):
        os.mkdir('D:/scrapy/gjw'+ft)
    else:
        print('File Exists')

    # if os.path.exists('url.txt'):
    #     os.remove('url.txt')

    def parse(self, response):
        def random_str(randomlength=9):
            str = ''
            chars = '123456789'
            for i in range(randomlength):
                str+=chars[random.randint(0, 8)]
            return str
        def search(req,html):
            text = re.search(req,html)
            if text:
                data = text.group(1)
            else:
                data = 'no'
            return data
        def getHTml(url):
            host = search('^([^/]*?)/',re.sub(r'(https|http)://','',url))
            headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding":"gzip, deflate, sdch",
                "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
                "Cache-Control":"no-cache",
                "Connection":"keep-alive",
                #"Cookie":"__cfduid=df26a7c536a0301ccf36481a14f53b4a81469608715; BIDUPSID=E9B0B6A35D4ABC6ED4891FCC0FD085BD; PSTM=1474352745; lsv=globalTjs_97273d6-wwwTcss_8eba1c3-routejs_6ede3cf-activityControllerjs_b6f8c66-wwwBcss_eabc62a-framejs_902a6d8-globalBjs_2d41ef9-sugjs_97bfd68-wwwjs_8d1160b; MSA_WH=1433_772; BAIDUID=E9B0B6A35D4ABC6ED4891FCC0FD085BD:FG=1; plus_cv=1::m:2a9fb36a; H_WISE_SIDS=107504_106305_100040_100100_109550_104341_107937_108437_109700_109794_107961_108453_109737_109558_109506_110022_107895_107917_109683_109588_110072_107318_107300_107242_100457; BDUSS=XNNMTJlWEdDdzFPdU1nSzVEZ1REYn4tNWNwZk94NVducXpaaThjWjE4bU1TQXRZQVFBQUFBJCQAAAAAAAAAAAEAAADLTBsKYTYzMTM4MTcwMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIy741eMu-NXQ; BDRCVFR[ltbVPlNi2ac]=mk3SLVN4HKm; BDRCVFR[C0p6oIjvx-c]=mbxnW11j9Dfmh7GuZR8mvqV; BDRCVFR[uLXjBGr0i56]=mbxnW11j9Dfmh7GuZR8mvqV; rsv_jmp_slow=1474644236473; sug=3; sugstore=1; ORIGIN=0; bdime=21110; H_PS_645EC=60efFRJ1dM8ial205oBcDuRmtLgH3Q6NaRzxDuIkbMkGVXNSHmXBfW0GZL4l5pnj; BD_UPN=123253; BD_CK_SAM=1; BDSVRTM=110; H_PS_PSSID=17947",
                "Host":host,
                "Pragma":"no-cache",
                "Upgrade-Insecure-Requests":"1",
                #"User-Agent":useragent.pcualist()
            }
            html = requests.get(url,headers=headers,timeout=30)
            code = html.encoding
            return html.content
        #gethtml end
    	yhdurl=response.url
        print yhdurl
    	html = response
        isempty = html.xpath('//div[@class="sorrybox"]')
        print len(isempty)
        with open('file/errkwt.txt','a') as yc:
            yc.write(yhdurl+'\n')
        yc.close()
        if len(isempty) > 0:
            print 'is no resault'
            pass
        else:
            cats = html.xpath('//title/text()').extract()[0]
            cats = cats.split('-')[0]
            gettext = ''
            tcc = cats.strip()
            try:
                print tcc
            except Exception,e:
                print e
                with open('file/errkw.txt','a') as yc:
                    yc.write(tcc+'\tyhdurl'+'\n')
                yc.close()
            gettext += tcc+'价格表：\n'
            itemss = html.xpath('//*[@class="main_wrap"]')
            items = itemss.xpath('div[@class="min_in"]')
            #print len(items),'---'
            totaln=len(items)
            if totaln>0 and totaln<=10:
                randnl = range(1,totaln)
            elif totaln > 10 and totaln <=25:
                clnn = range(1,totaln)
                crnum = random.randint(6,12)
                randnl = random.sample(clnn, crnum)
            else :
                clnn = range(1,25)
                crnum = random.randint(6,12)
                randnl = random.sample(clnn, crnum)
            global j
            j = 0
            for xx,item in enumerate(items,1):
                for xii in randnl:
                    if xii == xx :
                        j+=1
                        tit = item.xpath('div/a/@title').extract()[0]
                        if tit == '':
                            break
                        rt = item.xpath('p/em/@title').extract()[0]
                        itemcons = '%s、%s  价格：%s\n'%(j,tit,rt)
                        print itemcons
                        gettext +=itemcons
            filename = 'D:/scrapy/gjw'+ft+'/'+tcc+'.txt'
            print filename
            f = open(filename,'a')
            f.write(gettext)
            f.close()

        time.sleep(random.randint(4,9))