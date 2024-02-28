import requests


class LineNotify:
    """A class to send notifications using LINE Notify API."""

    def __init__(self, line_token):
        """
        Initialize the LineNotify instance.

        :param line_token: A valid LINE Notify token.
        """
        self.line_token = line_token
        self.line_notify_url = "https://notify-api.line.me/api/notify"

    def send(self, message):
        """
        Send a message to LINE Notify.

        :param message: The message to be sent.
        :return: The status code of the response.
        """
        headers = {"Authorization": f"Bearer {self.line_token}"}
        data = {"message": message}
        try:
            response = requests.post(self.line_notify_url, headers=headers, data=data)
            response.raise_for_status()
            return response.status_code
        except requests.RequestException as e:
            print(f"Error sending message: {e}")
            return None


# Example usage
if __name__ == "__main__":
    token = "YOUR_LINE_TOKEN"
    line_notify = LineNotify(token)
    status = line_notify.send("Hello, LINE Notify!")
    if status:
        print(f"Message sent successfully. Status code: {status}")
    else:
        print("Failed to send message.")
