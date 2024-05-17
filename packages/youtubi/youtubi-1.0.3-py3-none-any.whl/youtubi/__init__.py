from pytube import YouTube 
from bs4 import BeautifulSoup 
import os 

def download(link, output_path ) : 
	cache_file = os.path.join(output_path,'.youtu.be.history')
	if not os.path.exists(cache_file): 
		open(cache_file,"w").close()
	else : 
		downloaded_links = {i.strip()  for i in open(cache_file).read().split('\n')}
		if not (link in downloaded_links) : 
			try: 
				yt = YouTube(link) 
				mp4_streams = yt.streams.first()
				mp4_streams.download(output_path=output_path)
				print('Video downloaded successfully!' , yt.title)
				print(link , file = open(cache_file , "a"))
			except: print("Connection Error") 



def process(text, output_path = "./videos") : 
	if not os.path.exists(output_path) : 
		os.mkdir(output_path)
	urls = text.strip().split("\n")
	links = set()
	for line in urls : 
		_i = line.strip()
		if len(_i) > 6 : 
			links.add(_i)
	for link in links : 
		download(link, output_path)



def get_channel(htmlcode) : 
	soup = BeautifulSoup(htmlcode, 'lxml') 
	playlists = soup.findAll('ytd-playlist-panel-renderer', attrs = {'id':'playlist'}) 
	current_playlist = [playlist for playlist in playlists if len(playlist.findAll("a" , attrs = {"id" : "thumbnail"})) != 0 ]
	if len(current_playlist) > 0 :
		playlist = current_playlist[0]
		hrefs = [ a.get('href',None) .replace('/watch?v=','').split("&")[0] for a in playlist.findAll("a" , attrs = {"id" : "thumbnail"}) if a.get('href',None) is not None]
		hrefs = [f"\nhttps://www.youtube.com/watch?v={href}" for href in hrefs]
		print(f"Found {len(hrefs)} youtube video .")
		return "".join(hrefs) + "\n"
	else  : 
		print('Can not find <ytd-playlist-panel-renderer id ="playlist" ' )
		return ""

__all__ = [process,get_channel]