#-*-coding:utf-8-*-
import re
import requests
import os

#define a net spider class
class Spider:
    val = 0

    #it has a function of saving the pictures
    def savePageInfo(self, _pic_url, _position):

        url = _pic_url
        position = _position
        pic = requests.get(url)
        print  url + str(Spider.val)
        
        #If the path not exists, then create it
        if not os.path.isdir(position):
            os.makedirs(position)

        #save pictures
        fp = open( position + str(Spider.val)+'.jpg', 'wb')
        fp.write(pic.content)
        fp.close()

        Spider.val = Spider.val + 1

##########################################
####                                  ####
####  scrapy the picure from network  ####
####                                  ####
##########################################
if __name__ == '__main__':
    pic_url = 'http://scm.sf-express.com/isc-vmi/loginmgmt/imgcode?a=0.18090831750297091'
    position = 'testpictures_k/'
    if not os.path.exists('testpictures_k'):
        os.mkdir('testpictures_k')

    spider = Spider()

    for val in range(0,100):
        spider.savePageInfo(pic_url, position)