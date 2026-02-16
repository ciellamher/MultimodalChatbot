# src/main.py
import sys
# Fix import paths if running as a script
import os
sys.path.append(os.getcwd())

from src.word_bot import define_word
from src.image_bot import describe_image
from src.safety import is_safe_request

HELP = """
Commands:
  define <word>       Look up a word
  describe <path>     Describe an image file (jpg/png)
  help                Show this help
  exit                Quit
"""

def main():
    print("Multimodal Dictionary Chatbot (type 'help' for commands)")
    
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not line:
            continue
            
        if line == "exit":
            print("Bye.")
            break
            
        if line == "help":
            print(HELP)
            continue
            
        parts = line.split(maxsplit=1)
        if len(parts) < 2:
            print("Usage: define <word> | describe <image_path>")
            continue
            
        cmd, arg = parts[0], parts[1]
        
        # Safety Check [cite: 657]
        if not is_safe_request(arg):
            print("Sorry, I can't help with that request.")
            continue
            
        if cmd == "define":
            print(define_word(arg))
        elif cmd == "describe":
            print(describe_image(arg))
        else:
            print("Unknown command. Type 'help' for options.")

if __name__ == "__main__":
    main()