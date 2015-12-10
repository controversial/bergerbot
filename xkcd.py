import bs4
import urllib2
    
def writeComic(number=None):
    print "Input arg:", number
    url='http://xkcd.com/'+str(number)
    if number is not None:
        if 'random' in number:
            url = 'http://c.xkcd.com/random/comic/'
    elif number is None:
        url='http://xkcd.com/'
    print "URL:",url
        
    
    soup = bs4.BeautifulSoup(urllib2.urlopen(url).read())

    comiclink = 'http:' + [s['src'] for s in soup.select('img') if 'imgs.xkcd.com/comics' in s['src']][0]
    extension = comiclink.split('.')[-1]
    comic = urllib2.urlopen(comiclink)
    with open('comic.'+extension,'w') as comicfile:
        comicfile.write(comic.read())

    return 'comic.'+extension

if __name__ == '__main__':
    from PIL import Image
    Image.open(writeComic('random')).show()
