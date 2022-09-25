import os
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.textinput import TextInput




Builder.load_string(open(os.path.join("config", "kvfile.kv"), encoding = "utf-8").read(), rulesonly=True)

class Manager(ScreenManager):
    pass
    
class PopupWarning(Popup):
    pass

class LoginScreen(Screen):
    def login_verification(self):
        if self.ids.email.text == 'salah@gmail.com' and self.ids.passw.text == '1234':
            self.clean_inputs()
            self.ids.dica.text= ''
            App.get_running_app().root.current = 'netflixmenu'
        else:
            self.incorrect_login()
            self.clean_inputs()

    def clean_inputs(self):
        if self.ids.checkbox.active:
            self.ids.passw.text=''
        else:
            self.ids.email.text = self.ids.passw.text = ''

    def incorrect_login(self):
        popup = PopupWarning()
        popup.open()

        self.ids.dica.text = 'email = salah@gmail.com\npassword = 1234'

    def istab_pressed(self,text):
        if len(text) > 0 and text[-1]  == '\t':
            self.ids.passw.text = text[:-1]


class NetflixHome(Screen):
    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.isupdate)
        self.ids.scroll_home.scroll_y =1
        self.add_content()

    def on_leave(self, *args):
        self.ids.content.clear_widgets()

    def isupdate(self, key ,*args):
        if key == 286:
            self.on_pre_enter()
            if App.get_running_app().root.current == 'resultpage':
                App.get_running_app().root.current = 'netflixmenu'

    def add_content(self):
        self.ids.content.clear_widgets()
        self.ids.content.add_widget(Banner())

        for folder in os.listdir('Content'):
            files = os.listdir(os.path.join('Content', folder))
            content = ContentList()
            content.create(folder, files)
            self.ids.content.add_widget(content)


class Banner(BoxLayout):
    pass

class SearchBox(FloatLayout):
    def __init__(self, **kwargs):
        super(SearchBox, self).__init__(**kwargs)
        Clock.schedule_once(lambda *_: self.ids.searchbtn.bind(on_press =self.open_animation_search_box), 1)
        self.search_input = TextInput(multiline = False, hint_text = 'title', background_color= [0,0,0,1],
                                      on_text_validats= self.search , foreground_color = [1,1,1,1])

    def search(self,*args):
        if self.search_input.text != '':
            if App.get_running_app().root.current != 'resultpage':
                App.get_running_app().root.current = 'resultpage'

            App.get_running_app().root.get_screen('resultpage').pre_search(self.search_input.text.lower().strip())

        self.search_input.text =''

    def open_animation_search_box(self, *args):
        self.btn= self.ids.searchbtn
        self.search_input.size_hint = [0.02, 0.4]
        self.search_input.pos_hint={'center_y':0.5, 'center_x':0.57}
        Clock.schedule_once(self.searchinput_focus, 0.3)

        anim_btn = Animation(size_hint = [0.15, 0.45], duration = 0.01) + Animation(size_hint = [0.08, 0.35], duration = 0.01)+\
                   Animation(pos_hint = {'center_x':0.1}, duration = 0.05)

        anim_txt = Animation(size_hint= [0.8, 0.54], d=0.15, t = 'in_sine')

        anim_btn.start(self.btn)
        self.add_widget(self.search_input)
        anim_txt.start(self.search_input)

        self.btn.undind(on_press = self.open_animation_search_box)
        self.btn.bind(on_press = self.search)

        Clock.schedule_once(lambda *_: Clock.schedule_interval(self.isdefocused, 0), 0.4)

    def close_animation_search_box(self, *args):
        anim_btn = Animation(size_hint=[0.15, 0.45], duration=0.01) + Animation(size_hint=[0.08, 0.35], duration=0.01) + \
                   Animation(pos_hint={'center_x': 0.9}, duration=0.1)

        self.remove_widget(self.search_input)
        anim_btn.start(self.btn)

        self.btn.undind(on_press=self.search)
        self.btn.bind(on_press=self.open_animation_search_box)

    def searchinput_focus(self, *args):
        self.search_input.focus = True

    def isdefocused(self, *args):
        if not self.search_input.focus:
            self.close_animation_search_box()
            Clock.unschedule(self.isdefocused)

class ContentList(BoxLayout):
    def create(self, foldername, images):
        self.padding = 0,0,0, 50
        self.ids.label.text = foldername
        self.ids.grid.cols = len(images)
        if len(images) > 0:
            for image in images:
                image_path = os.path.join('Content', foldername, image)
                image_content = ImageContent(image_path)
                self.ids.grid.add_widget(image_content)
    
class ImageContent(Button):
    def __init__(self, image_path, **kwargs):
        super().__init__(**kwargs)
        self.image_path = image_path
        self.size_hint = None,None
        self.size = 240, 151

        self.background_normal = self.background_down = self.image_path

    def on_press(self):
        print(self.im)

class ResultPage(Screen):
    def pre_search(self, text):
        if len(text) >0:
            all_images= []
            for folder , subfolders, files in os.walk('Content') :
                for file in files:
                    if filw[:-4] not in all_images:
                        all_images.append(file[:-4])

            self.search_files(text, all_images)


    def search_files(self, text, all_images):
        for individual_word in text.split(' '):
            for image in all_images:
                if individual_word in image.lower():
                    results.append(image +  '.jpg')


        folders = os.listdir('Content')
        paths = []
        for result in results:
            for folder in folders:
                folder_path= os.path.join('Content', folder)
                images = os.listdir(folder_path)
                if result in images:
                    img_index = images.index(result)
                    paths.append(os.path.join(folder_path, images[img_index]))
                    break
        self.add_content(text, paths)

    def add_content(self,text, paths= None):
        self.ids.stack.clear_widgets()
        self.ids.scroll_result.scroll_y = 1
        if len(paths) > 0:
            self.ids.searchtext.text = ' Result this itachi ' + text.title()
            for path in paths:
                self.ids.stack.add_widget(ImageContent(path))
        else:
            self.ids.searchtext.text = ' no result ' + text.title()

    
class NetClone(App):
    app_icon = os.path.join('config','icone.ico')
    netflix_logo = os.path.join('config','netflix.png')
    background_login = os.path.join('config','background.jpg')
    dropmenu_icon = os.path.join('config','icone_sair.jpg')
    search_btn =os.path.join('config','search_btn.png')
    roundborder = os.path.join('config','roundborder.png')
    banner = os.path.join('config', 'banner.jpg')
    netflix_font = os.path.join('config','net_font.ttf')
    def build(self):
        self.icon= self.app_icon
        return Manager()

NetClone().run()