import irc_client as irc
import os

WORKING_DIR = "."
BACKEND = os.getenv("IRC_SERVER_HOST"), int(os.getenv("IRC_SERVER_PORT"))
HTTP_ROOT = "/bot"
HTTP_LISTEN = "0.0.0.0", int(os.getenv("PORT"))

BOT_USERNAME = "antonia"
BOT_REALNAME = "antonia"
BOT_NICKNAME = "antonia"
BOT_CHANNELS = ("#twilightzone", "#laterpay",)
JENKINS_CHANNEL = os.getenv("JENKINS_CHANNEL")
GITHUB_CHANNEL = JENKINS_CHANNEL
GITHUB_AUTH_TOKEN = os.environ['GITHUB_AUTH_TOKEN']
GITHUB_DEFAULT_ORGANIZATION = 'laterpay'
GITHUB_DEFAULT_REPO = 'laterpay'
