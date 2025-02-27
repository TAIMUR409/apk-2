from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import os
import json

# Vault Configuration
VAULT_FOLDER = "hidden_vault"
PASSWORD_FILE = "vault_password.json"
DEFAULT_PASSWORD = "1234"

if not os.path.exists(VAULT_FOLDER):
    os.makedirs(VAULT_FOLDER)

def load_password():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as f:
            return json.load(f)["password"]
    else:
        with open(PASSWORD_FILE, "w") as f:
            json.dump({"password": DEFAULT_PASSWORD}, f)
        return DEFAULT_PASSWORD

current_password = load_password()

class CalculatorVault(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.display = TextInput(font_size=32, readonly=True, halign='right', size_hint_y=0.2)
        self.add_widget(self.display)

        grid = GridLayout(cols=4)
        buttons = [
            ('AC', 'red'), ('±', 'gray'), ('%', 'gray'), ('÷', 'orange'),
            ('7', 'darkgray'), ('8', 'darkgray'), ('9', 'darkgray'), ('×', 'orange'),
            ('4', 'darkgray'), ('5', 'darkgray'), ('6', 'darkgray'), ('-', 'orange'),
            ('1', 'darkgray'), ('2', 'darkgray'), ('3', 'darkgray'), ('+', 'orange'),
            ('○', 'darkgray'), ('0', 'darkgray'), ('.', 'darkgray'), ('=', 'orange')
        ]

        for text, color in buttons:
            btn = Button(text=text, background_color=self.get_color(color), font_size=28)
            btn.bind(on_press=self.on_button_click)
            grid.add_widget(btn)
        
        self.add_widget(grid)

    def get_color(self, name):
        colors = {
            'red': (1, 0, 0, 1), 'gray': (0.7, 0.7, 0.7, 1), 'orange': (1, 0.5, 0, 1), 'darkgray': (0.3, 0.3, 0.3, 1)
        }
        return colors.get(name, (1, 1, 1, 1))

    def on_button_click(self, instance):
        text = instance.text
        if text == 'AC':
            self.display.text = ''
        elif text == '=':
            self.calculate_result()
        elif text == '±':
            self.toggle_sign()
        elif text == '%':
            self.calculate_percentage()
        else:
            self.display.text += text

    def calculate_result(self):
        try:
            expression = self.display.text.replace('×', '*').replace('÷', '/')
            if expression == current_password:
                self.open_vault()
            else:
                self.display.text = str(eval(expression))
        except:
            self.display.text = 'Error'

    def toggle_sign(self):
        if self.display.text:
            if self.display.text[0] == '-':
                self.display.text = self.display.text[1:]
            else:
                self.display.text = '-' + self.display.text

    def calculate_percentage(self):
        try:
            self.display.text = str(float(self.display.text) / 100)
        except:
            self.display.text = 'Error'

    def open_vault(self):
        content = BoxLayout(orientation='vertical')
        open_button = Button(text='Open Vault', size_hint_y=0.2)
        open_button.bind(on_press=lambda x: os.system(f"explorer {VAULT_FOLDER}"))
        
        change_password_button = Button(text='Change Password', size_hint_y=0.2)
        change_password_button.bind(on_press=self.change_password)
        
        content.add_widget(open_button)
        content.add_widget(change_password_button)
        
        popup = Popup(title='Vault Options', content=content, size_hint=(0.8, 0.4))
        popup.open()

    def change_password(self, instance):
        content = BoxLayout(orientation='vertical')
        self.new_password_input = TextInput(hint_text='Enter New Password', password=True, multiline=False)
        confirm_button = Button(text='Confirm', size_hint_y=0.2)
        confirm_button.bind(on_press=self.save_new_password)
        content.add_widget(self.new_password_input)
        content.add_widget(confirm_button)
        
        self.password_popup = Popup(title='Change Password', content=content, size_hint=(0.8, 0.4))
        self.password_popup.open()
    
    def save_new_password(self, instance):
        global current_password
        new_password = self.new_password_input.text.strip()
        if new_password:
            current_password = new_password
            with open(PASSWORD_FILE, "w") as f:
                json.dump({"password": new_password}, f)
            self.password_popup.dismiss()
            popup = Popup(title='Success', content=Label(text='Password changed successfully!'), size_hint=(0.6, 0.3))
            popup.open()

class CalculatorVaultApp(App):
    def build(self):
        return CalculatorVault()

if __name__ == '__main__':
    CalculatorVaultApp().run()
