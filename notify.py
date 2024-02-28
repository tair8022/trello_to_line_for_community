from module import trello
from module import line_notify
import json
from pprint import pprint


class Community:
    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self.load_config(config_path)
        self.line = line_notify.LineNotify(self.line_token)
        self.trello = trello.TrelloBoard(
            self.trello_key, self.trello_token, self.trello_board_id
        )

    def load_config(self, config_path: str):
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            self.trello_key = config["trello_key"]
            self.trello_token = config["trello_token"]
            self.trello_board_id = config["trello_board_id"]
            self.line_token = config["line_token"]

    def weekly_sammary_report(self):
        message = self.trello.notify_board_status()
        self.line.send(message)

    def delay_report(self):
        overdue_cards = self.trello.get_overdue_cards()
        message_lines = ["\n \n【📌 逾時任務-提醒】\n"]
        if not overdue_cards:
            print("No overdue cards found.")
            return

        for card in overdue_cards:
            card_name = card["name"]
            card_url = card["shortUrl"]
            desc = card["desc"]
            due_date = self.trello.format_date(card["due"])
            tab = "    "
            message = f"{tab}任務名稱：{card_name}\n{tab}任務描述：{desc}\n{tab}到期日：{due_date}\n{tab}任務連結：{card_url}\n"
            message_lines.append(message)

        message = "\n".join(message_lines)
        self.line.send(message)
        print(f"Message sent successfully: \n{message}")

    def dayly_report(self):
        overdue_cards = self.trello.get_overdue_cards()
        message_lines = ["\n \n【🚨 逾時任務-提醒】\n"]
        if not overdue_cards:
            print("No overdue cards found.")
            return

        for card in overdue_cards:
            card_name = card["name"]
            card_url = card["shortUrl"]
            desc = card["desc"]
            due_date = self.trello.format_date(card["due"])
            tab = "    "
            message = f"{tab}任務名稱：{card_name}\n{tab}任務描述：{desc}\n{tab}到期日：{due_date}\n{tab}任務連結：{card_url}\n"
            message_lines.append(message)

        message = "\n".join(message_lines)
        self.line.send(message)
        print(f"Message sent successfully: \n{message}")

    def get_upcoming_due_cards(self):
        message_lines = ["\n \n【⏰ 即將到期-提醒】\n"]
        upcoming_due_cards = self.trello.get_cards_due_soon(1)

        if not upcoming_due_cards:
            print("No overdue cards found.")
            return

        for card in upcoming_due_cards:
            card_name = card["name"]
            card_url = card["shortUrl"]
            desc = card["desc"]
            due_date = self.trello.format_date(card["due"])
            tab = "    "
            message = f"{tab}- 任務名稱：{card_name}\n{tab}  到期日：{due_date}\n{tab}  任務連結：{card_url}\n"
            message_lines.append(message)

        message = "\n".join(message_lines)
        self.line.send(message)
        print(f"Message sent successfully: \n{message}")


if __name__ == "__main__":
    config_path = r"testConfig.json"
    community = Community(config_path)

    card = community.get_upcoming_due_cards()
 
