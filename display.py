from PIL import Image
from PIL import ImageTk
import tkinter
import threading

class Display:
    def __init__(self, title):
        self.tk = tkinter.Tk()
        self.tk.wm_title(title)
        self.tk.wm_protocol("WM_DELETE_WINDOW", self.destroy)
        self.frame = None
        self.finish_fn = None
        self.stop=False

    def set_poll_function(self, fn, *args):
        self.poll_fn = fn
        self.poll_args = args
    
    def show(self):
        self.thread = threading.Thread(target=self.work)
        self.stop = threading.Event()
        self.thread.start()
        self.tk.mainloop()

    def work(self):
        try:
            while not self.stop.is_set():
                img = self.poll_fn(*self.poll_args)
                if img is None:
                    continue
                img = ImageTk.PhotoImage(img)

                if self.frame == None:
                    self.frame = tkinter.Label(image=img)
                    self.frame.image = img
                    self.frame.pack(side='left', padx=10, pady=10)
                else:
                    self.frame.configure(image=img)
                    self.frame.image = img
        except RuntimeError:
            pass

    def set_finish_function(self, fn, *args):
        self.finish_fn = fn
        self.finish_fn_args = args

    def destroy(self):
        print('destroy')
        self.stop.set()
        if self.finish_fn is not None:
            self.finish_fn(*self.finish_fn_args)
        self.tk.destroy()
        exit()
