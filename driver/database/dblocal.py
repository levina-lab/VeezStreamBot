""" mongo database """

from motor.motor_asyncio import AsyncIOMotorClient as Bot
from config import MONGODB_URL as tmo


MONGODB_CLI = Bot(tmo)
db = MONGODB_CLI.program
