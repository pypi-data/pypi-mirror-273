from MatrixChatbotGenerator.classes import UserInterface
from MatrixChatbotGenerator.classes import QTIParser

qti_parser = QTIParser()
questions = qti_parser.get_questions()
# questions.print_short()

ui = UserInterface(questions)
ui.loop()


