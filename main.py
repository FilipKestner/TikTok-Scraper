import downloader 
import editor 


import sys
import getopt

# Progress Bar
from tqdm import tqdm
from time import sleep


# Usage: main.py -d directory/to/download/into @names @of @different @TikTok @profiles

opts, args = getopt.getopt(sys.argv[1:],"d:",['dir'])

print(opts)
print(args)


# Setting Download Directory
download_dir = './videos/'
for o, a in opts:
    if o == 'd':
        download_dir = a




for channel in args:
    links = downloader.Downloader.parser(channel)

    for i in tqdm(range(len(links)), desc=f'{channel}', colour='red'):
        downloader.Downloader.download(links[i],i,channel,download_dir)

    edit = editor.Editor(download_dir+channel+'/original/',download_dir+channel+'/edited/',channel)
    edit.getPaths()
    edit.processX(10)













