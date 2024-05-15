import os
import sys

from utils_base import Console, File, Log

from utils_ai.providers import ProviderFactory

log = Log('ChatApp')


class ChatApp:
    @staticmethod
    def set_profile(ai, profile_path: str):
        if os.path.exists(profile_path):
            profile_content = File(profile_path).read()
            ai.set_profile(profile_content)
            print(Console.note(f'{profile_path}'))
            print('')

    @staticmethod
    def run_iter(ai):
        message = input('>> ')
        print('')

        if len(message) == 0:
            return

        if message in ['quit', 'exit', 'q', 'x', 'exit()', 'quit()']:
            print(Console.note('Bye!'))
            print()
            sys.exit(0)

        if message.lower().startswith('draw:'):
            image_path = ai.draw(prompt=message[5:])
            if image_path:
                print(Console.note(image_path))
                print('')
                os.startfile(image_path)
            return

        reply = ai.chat(message)
        if reply:
            print(Console.note(reply))
            print('')

    @staticmethod
    def run(provider_name: str, profile_path: str):
        ai = ProviderFactory.from_name(provider_name)
        print('')
        print(Console.note(f'[{ai.NAME}/{ai.MODEL}]'))
        print('')

        ChatApp.set_profile(ai, profile_path)

        while True:
            ChatApp.run_iter(ai)
