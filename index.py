from pytube import YouTube

yt = YouTube("https://www.youtube.com/watch?v=INwWJicYwds",proxies={"https":"http://127.0.0.1:1080"})

print(yt.streams.all())

stream = yt.streams[2]

print(stream)

stream.download('./')