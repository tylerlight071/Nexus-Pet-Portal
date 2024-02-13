import time
from tabulate import tabulate
from colorama import Fore, Style
from common_functions import clear_screen

def notifications():
    notifications = [
        {"id": 1, "text": "Notification 1", "read": False},
        {"id": 2, "text": "Notification 2", "read": False},
        {"id": 3, "text": "Notification 3", "read": False},
    ]

    while True:
        clear_screen()

        print("\nNotifications:")
        table = [[notif['id'], notif['text'], 'Read' if notif['read'] else 'Unread'] for notif in notifications]
        print(tabulate(table, headers=['ID', 'Text', 'Status'], tablefmt='pretty'))

        print("\nOptions:")
        print(Fore.CYAN + "1. Read a notification")
        print(Fore.CYAN + "2. Delete a notification")
        print(Fore.CYAN + "3. Clear read notifications")
        print(Fore.CYAN + "4. Exit" + Style.RESET_ALL)

        option = input("\nPlease select an option: ")

        if option == '1':
            clear_screen()
            notif_id = int(input("\nEnter the ID of the notification you want to read: "))
            for notification in notifications:
                if notification['id'] == notif_id:
                    notification['read'] = True
                    print(Fore.GREEN + f"\n{notification['text']}" + Style.RESET_ALL)
                    break
            else:
                print(Fore.RED + "Notification not found." + Style.RESET_ALL)
        elif option == '2':
            clear_screen()
            notif_id = int(input("\nEnter the ID of the notification you want to delete: "))
            notifications = [notification for notification in notifications if notification['id'] != notif_id]
        elif option == '3':
            notifications = [notification for notification in notifications if not notification['read']]
        elif option == '4':
            break
        else:
            print(Fore.RED + "Invalid option. Please try again." + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()

        time.sleep(2)

