import requests
from datetime import datetime
import json
from datetime import datetime, timezone, timedelta
from pprint import pprint


class TrelloBoard:
    """A class to interact with Trello boards."""

    def __init__(self, key, token, board_id):
        """
        Initialize the TrelloBoard instance.

        :param key: Trello API key.
        :param token: Trello API token.
        :param board_id: ID of the Trello board.
        """
        self.key = key
        self.token = token
        self.board_id = board_id

    def get_board_lists(self):
        """Retrieve lists from the Trello board."""
        url = f"https://api.trello.com/1/boards/{self.board_id}/lists"
        query = {"key": self.key, "token": self.token}
        try:
            response = requests.get(url, params=query)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error retrieving board lists: {e}")
            return None

    def get_cards_from_list(self, list_id):
        """Retrieve cards from a specific list on the Trello board."""
        url = f"https://api.trello.com/1/lists/{list_id}/cards"
        query = {"key": self.key, "token": self.token}
        try:
            response = requests.get(url, params=query)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error retrieving cards from list: {e}")
            return None

    def format_date_with_chinese_weekday(date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        weekday_str = weekdays[date_obj.weekday()]
        return date_obj.strftime(f"%Y %m/%d({weekday_str}) %H:%M ")

    @staticmethod
    def format_date(date_str):
        def format_date_with_chinese_weekday(date_str):
            date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            weekdays = ["一", "二", "三", "四", "五", "六", "日"]
            weekday_str = weekdays[date_obj.weekday()]
            return date_obj.strftime(f"%Y-%m/%d({weekday_str}) %H:%M ")

        """Format the date string from Trello to a more readable format."""
        if date_str:
            return format_date_with_chinese_weekday(date_str)
        else:
            return "無截止日期"

    def notify_board_status(self) -> str:
        board_lists = self.get_board_lists()
        message_lines = ["\n【📌 任務清單】\n"]
        skip_lists = ["已完成"]  # 不顯示的列表名稱

        for lst in board_lists:
            list_name = lst["name"]
            list_id = lst["id"]
            print(f"list_name: {list_name}, list_id: {list_id}")
            cards = self.get_cards_from_list(list_id)

            if not cards or list_name in skip_lists:
                continue  # 如果列表中沒有卡片，則跳過

            message_lines.append(f"\n📋 列表名稱：{list_name}\n")
            for card in cards:
                due_date = self.format_date(card["due"])
                desc = card["desc"] if card["desc"] else "無描述"
                card_info = (
                    f"    - 任務名稱：{card['name']}"
                    # f"      任務描述：{desc}\n"
                    # f"      截止日期：{due_date}\n"
                )

                message_lines.append(card_info)
                message_lines.append("")  # 添加空行作為分隔
        message_lines.append("看板連接:https://trello.com/b/gVyPTDzo")
        message = "\n".join(message_lines)
        print(str(message))  # 顯示消息以供調試
        return message

    def get_overdue_cards(self):
        """Retrieve all overdue cards from the Trello board."""
        overdue_cards = []
        board_lists = self.get_board_lists()
        if not board_lists:
            return overdue_cards

        for lst in board_lists:
            list_id = lst["id"]

            cards = self.get_cards_from_list(list_id)
            if not cards:
                continue
            for card in cards:

                due_date = card.get("due")
                due_complete = card.get("dueComplete")
                if self.is_overdue(due_date) and not due_complete:
                    overdue_cards.append(card)

        return overdue_cards

    def get_cards_due_soon(self, days_until_due):
        """Retrieve all cards that are due within the specified number of days."""
        due_soon_cards = []
        board_lists = self.get_board_lists()
        if not board_lists:
            return due_soon_cards

        now = datetime.now(timezone.utc)
        due_limit = now + timedelta(days=days_until_due)

        for lst in board_lists:
            list_id = lst['id']
            cards = self.get_cards_from_list(list_id)
            if not cards:
                continue

            for card in cards:
                due_date_str = card.get('due')
                due_complete = card.get('dueComplete')
                if due_complete is False and due_date_str:
                    # 将 due_date 转换为 offset-aware datetime 对象
                    due_date = datetime.strptime(
                        due_date_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
                    if now <= due_date <= due_limit:
                        due_soon_cards.append(card)

        return due_soon_cards

    @staticmethod
    def is_overdue(due_date_str):
        """Check if a given due date is in the past."""
        if not due_date_str:
            return False
        # 将 due_date 转换为 offset-aware datetime 对象
        due_date = datetime.strptime(
            due_date_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        return due_date < now
