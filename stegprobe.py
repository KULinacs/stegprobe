from plat import twitter_connect as soc
from steg import outguess as stg

infile = 'testfiles/base.jpg'
datafile = 'testfiles/stegin.txt'
upfile = 'testfiles/upload.jpg'
downfile = 'testfiles/download.jpg'
outsteg = 'testfiles/stegout.txt'

stg.hide(datafile, infile, upfile)
soc.cycle_media(downfile, 'Outguess', upfile, True)
stg.retrieve(downfile, outsteg)
