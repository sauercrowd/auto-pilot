import subprocess
from PIL import Image

class FFmpegDesktopCapture:
    def __init__(self, size=(1024, 768), framerate=10, pos=":0.0+100,200", ffmpeg_binary='/usr/bin/ffmpeg'):
        self.size = size
        self.framerate = framerate
        self.pos = pos
        self.ffmpeg_binary = ffmpeg_binary
        self._start()

    def _start(self):
        ffmpeg_cmd = [
            self.ffmpeg_binary,
            '-video_size',
            '{}x{}'.format(self.size[0], self.size[1]),
            '-framerate',
            str(self.framerate),
            '-f',
            'x11grab',
            '-i',
            self.pos,
            '-f',
            'image2pipe',
            '-pix_fmt',
            'rgb24',
            '-vcodec',
            'rawvideo',
            '-'
        ]
        self.ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, bufsize=10**8, stdout=subprocess.PIPE)
    
    def get_frame(self):
        line = self.ffmpeg_proc.stdout.read(self.size[0] * self.size[1] * 3)
        image = Image.frombytes(mode='RGB', size=self.size, data=line)
        self.ffmpeg_proc.stdout.flush()
        return image
    
    def stop(self):
        #self.ffmpeg_proc.stdout.flush()
        self.ffmpeg_proc.kill()