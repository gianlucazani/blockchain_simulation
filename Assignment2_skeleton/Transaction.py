import re


class Transaction:
    def __init__(self, sender, content):
        self.sender = sender
        self.content = content
        # self.transaction = f"tx|{sender}|{content}"  # will store a string in the format tx|sender|content

    def validate(self):
        """
        Validates the transaction as specified in the assignment sheet
        :return: True if the transaction is valid, False otherwise
        """
        sender_pattern = re.compile("[A-Za-z0-9]+")
        if sender_pattern.fullmatch(self.sender) is None:  # checks sender correct format
            return False
        if "\\" in self.content or len(self.content) > 70:  # checks correctness of the content field
            return False
        return True

    def get_as_string(self):
        """
        Returns the transaction in the form tx|[sender]|[content]
        :return: transaction as a string
        """
        return f"tx|{self.sender}|{self.content}"

