# -*- coding: utf-8 -*-
import spynner  
import pyquery  
import time  
import BeautifulSoup  
import sys  
from scrapy.http import HtmlResponse  
class WebkitDownloaderTest( object ):  
    def process_request( self, request, spider ):  
#        if spider.name in settings.WEBKIT_DOWNLOADER:  
#            if( type(request) is not FormRequest ):  
                browser = spynner.Browser()  
                browser.create_webview()  
                browser.set_html_parser(pyquery.PyQuery)  
                browser.load(request.url, 40)  
                try:  
                        browser.wait_load(20)  
                except:  
                        pass  
                string = browser.html  
                browser.close()
                string=string.encode('utf-8')  
                renderedBody = str(string)  
                return HtmlResponse( request.url, body=renderedBody )  