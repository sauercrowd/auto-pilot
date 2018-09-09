import display
import multiprocessing
import ffmpeg_desktop_capture
import socket


def main():
    cap = ffmpeg_desktop_capture.FFmpegDesktopCapture(framerate=50)

    #x = display.Display('Desktop Capture')
    #x.set_poll_function(lambda: cap.get_frame())
    #x.set_finish_function(lambda: cap.stop())
    #x.show()
    server_loop(cap)

def server_loop(cap):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 7654))
    s.listen()

    conn, _ = s.accept()

    while True:
        conn.send(cap.get_frame())

if __name__ == "__main__":
    main()