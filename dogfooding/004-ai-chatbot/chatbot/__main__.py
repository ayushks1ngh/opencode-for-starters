import sys

from chatbot.cli import main

if __name__ == "__main__":
    debug = "--debug" in sys.argv
    main(debug=debug)
