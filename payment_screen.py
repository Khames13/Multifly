from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.event import EventDispatcher
from kivy.uix.textinput import TextInput

import threading
import requests


class AutoWrapLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(width=self.update_text_size)
        self.markup = True
        self.size_hint_y = None
        self.halign = 'left'
        self.valign = 'top'
        self.text_size = (self.width, None)

    def update_text_size(self, *args):
        self.text_size = (self.width, None)
        self.texture_update()
        self.height = self.texture_size[1]


class PaymentScreen(Screen, EventDispatcher):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_subscription_success')

        self.selected_payment_method = None

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.title_label = Label(
            text="[b]Upgrade to Premium[/b]",
            markup=True,
            font_size='24sp',
            size_hint=(1, None),
            height=40,
            halign='center',
            valign='middle'
        )
        self.title_label.bind(size=self._update_text_size)
        self.layout.add_widget(self.title_label)

        # PayPal Button
        self.paypal_button = Button(
            text="[b][color=1a73e8]PayPal Payment Details[/color][/b]",
            markup=True,
            size_hint=(1, None),
            height=40,
            background_normal='',
            background_color=(0.9, 0.9, 1, 1),
            color=(0, 0, 0, 1)
        )
        self.paypal_button.bind(on_release=self.toggle_paypal_info)
        self.layout.add_widget(self.paypal_button)

        # PayPal Info
        self.paypal_label = AutoWrapLabel(
            text=self.get_paypal_info(),
            opacity=0
        )
        self.layout.add_widget(self.paypal_label)

        # Mpesa Button
        self.mpesa_button = Button(
            text="[b][color=008000]Mpesa Payment Details[/color][/b]",
            markup=True,
            size_hint=(1, None),
            height=40,
            background_normal='',
            background_color=(0.9, 1, 0.9, 1),
            color=(0, 0, 0, 1)
        )
        self.mpesa_button.bind(on_release=self.toggle_mpesa_info)
        self.layout.add_widget(self.mpesa_button)

        # Mpesa Info
        self.mpesa_label = AutoWrapLabel(
            text=self.get_mpesa_info(),
            opacity=0
        )
        self.layout.add_widget(self.mpesa_label)

        # Transaction Code Label
        self.txn_label = Label(
            text="Enter Transaction Code:",
            size_hint=(1, None),
            height=30,
            halign='left',
            valign='middle'
        )
        self.txn_label.bind(size=self._update_text_size)
        self.layout.add_widget(self.txn_label)

        # Transaction Code Input
        self.txn_input = TextInput(
            hint_text="e.g., ABC123XYZ",
            multiline=False,
            size_hint=(1, None),
            height=40,
            font_size='16sp',
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(0, 0, 0, 1)
        )
        self.layout.add_widget(self.txn_input)

        # Subscribe Button
        self.subscribe_button = Button(
            text="Subscribe Now",
            size_hint=(1, None),
            height=50,
            background_color=(0.2, 0.6, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        self.subscribe_button.bind(on_release=self.subscribe)
        self.layout.add_widget(self.subscribe_button)

        # Back Button
        self.back_button = Button(
            text="← Back",
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_color=(0.7, 0.7, 0.7, 1),
            color=(0, 0, 0, 1)
        )
        self.back_button.bind(on_release=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def _update_text_size(self, instance, size):
        instance.text_size = (size[0], None)
        instance.texture_update()
        instance.height = instance.texture_size[1]

    def toggle_paypal_info(self, instance):
        self.selected_payment_method = "paypal"
        if self.mpesa_label.opacity > 0:
            Animation(opacity=0, d=0.3).start(self.mpesa_label)
        Animation(opacity=1 if self.paypal_label.opacity == 0 else 0, d=0.3).start(self.paypal_label)

    def toggle_mpesa_info(self, instance):
        self.selected_payment_method = "mpesa"
        if self.paypal_label.opacity > 0:
            Animation(opacity=0, d=0.3).start(self.paypal_label)
        Animation(opacity=1 if self.mpesa_label.opacity == 0 else 0, d=0.3).start(self.mpesa_label)

    def get_paypal_info(self):
        return (
            "[b]PayPal Account:[/b] your-paypal-email@example.com\n"
            "[b]Amount:[/b] 300 KES\n"
            "[b]Payment Type:[/b] Monthly Subscription\n\n"
            "Please send payment and email your transaction ID to support@example.com."
        )

    def get_mpesa_info(self):
        return (
            "[b]Paybill Number:[/b] 123456\n"
            "[b]Account Number:[/b] Your phone number\n"
            "[b]Amount:[/b] 300 KES\n"
            "[b]Payment Type:[/b] Monthly Subscription\n\n"
            "After payment, send your Mpesa code to support@example.com."
        )

    def subscribe(self, *args):
        txn_code = self.txn_input.text.strip()
        if not txn_code:
            self.show_popup("Please enter your payment transaction ID/code before subscribing.")
            return

        if len(txn_code) < 8:
            self.show_popup("Transaction code seems too short. Please check again.")
            return

        if not self.selected_payment_method:
            self.show_popup("Please select a payment method first.")
            return

        self.show_popup("Processing subscription...")
        threading.Thread(target=self.process_subscription, args=(txn_code,)).start()

    def process_subscription(self, txn_code):
        url = "http://127.0.0.1:5000/subscribe"  # Replace with your actual backend URL

        data = {
            "user_id": "12345",  # Replace with real user ID if available
            "payment_method": self.selected_payment_method,
            "amount": 300,
            "currency": "KES",
            "transaction_code": txn_code
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                self.dispatch('on_subscription_success')
            else:
                self.show_popup(f"Subscription failed: {response.text}")
        except Exception as e:
            self.show_popup(f"Error contacting server: {str(e)}")

    def on_subscription_success(self, *args):
        self.dismiss_popup()
        self.txn_input.text = ""
        self.show_popup("Subscription successful! Your account is now premium.")

    def show_popup(self, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        btn = Button(text="OK", size_hint=(1, 0.3))
        content.add_widget(btn)

        self._popup = Popup(title="Info", content=content, size_hint=(0.7, 0.4))
        btn.bind(on_release=self._popup.dismiss)
        self._popup.open()

    def dismiss_popup(self):
        if hasattr(self, '_popup'):
            self._popup.dismiss()

    def go_back(self, instance):
        self.manager.current = 'level_select'
