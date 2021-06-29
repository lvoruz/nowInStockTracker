from discord_webhook import DiscordWebhook

class DiscordBot():
    def __init__(self, webhookUrl):
        self.webhookUrl = webhookUrl
        self.webhook = DiscordWebhook(url=self.webhookUrl)

    def execute(self, content):
        self.webhook.set_content(content)
        self.webhook.execute()