import os
import time
import random
import winsound

def type_out(text, delay=0.05, pause=3):
    for char in text:
        print(char, end='', flush=True)
    print()
    winsound.Beep(1000, 200)
    time.sleep(pause)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def simulate_commands(commands, delay=0.02, pause=0.5):
    for command in commands:
        print(command, flush=True)
        time.sleep(delay)
    time.sleep(pause)

discouraging_responses = [
    "Computer: Are you even trying?",
    "Computer: Seriously? Try harder.",
    "Computer: That's just embarrassing.",
    "Computer: Is this your first day hacking?",
    "Computer: You call this hacking? Pathetic.",
    "Computer: You’re making the feds’ job easier.",
]

def incorrect_response():
    type_out(random.choice(discouraging_responses))

def hacking_game():
    while input("Write start to start the game").strip().lower() != "start":
        pass
    
    type_out("Computer: You need to mask your identity before connecting to Spygle servers.")
    type_out("John: You mean my IP address?")
    type_out("Computer: Then what genius, hurry and use an encrypted tunnel.")
    type_out("Hint: connect ***")

    while True:
        answer = input("> ").strip().lower()
        if answer == "connect vpn":
            type_out("Connecting to VPN...")
            type_out("Computer: VPNs can mask your IP address, but they log metadata like timestamps and source IPs which would be very convenient for the feds to subpoena.")
            break
        else:
            incorrect_response()
    input("To progress to next level write next")
    

    type_out("John: Well in that case let me use the onion.")
    type_out("Hint: connect ***")

    while True:
        answer = input("> ").strip().lower()
        if answer == "connect tor":
            type_out("Connecting to Tor...")
            simulate_commands([
                ">> Establishing Tor circuit...",
                ">> Encrypting data...",
                ">> Hopping through relay nodes...",
                ">> Connection established via exit node 45.67.89.101",
            ])
            type_out("Computer: Tor encrypts your data and uses multiple relay nodes to obfuscate your origin and destination. But keep and eye out since the exit node can still see what you are connecting to")
            break
        else:
            incorrect_response()

    input("To progress to next level write next")

    type_out("Computer: The enumeration phase gave us this hash: 2c70e12b7a0646f92279f427c7b38e7334d8e5389cff167a1dc30e73f826b683.")
    type_out("John: Let's decrypt it?")
    type_out("Hint: use the most common hashing alogorithm, use external tools")

    while True:
        answer = input("> ").strip().lower()
        if answer == "key":
            simulate_commands([
                ">> Hash identified: SHA-256",
                ">> Searching wordlist...",
                ">> Matching hash to password...",
                ">> Found: password = 'key'",
            ])
            type_out("Computer: That was quick. We are lucky he didn't use a good password, that would take billions of years to crack.")
            type_out("John: This will be usefull later.")
            break
        else:
            incorrect_response()

    input("To progress to next level write next")

    type_out("Computer: Let’s try logging into his email.")
    type_out("John: The password worked, but he has 2FA.")
    type_out("Computer: Didn’t we grab his phone number from LinkedIn?")
    type_out("John: Right.")
    type_out("Hint: Do a *** ******** attack")

    while True:
        answer = input("> ").strip().lower()
        if answer == "sim swapping":
            simulate_commands([
                ">> Spoofing target phone number...",
                ">> Requesting SMS verification code...",
                ">> Intercepting code...",
                ">> Verification successful!",
            ])
            type_out("Executing SIM swapping attack...")
            type_out("Computer: Some phone providers in third world countries sell access to hackers to do Sim Swapping attack. SMS 2FA can not be trusted. Authenticator apps are a much safer alternative.")
            break
        else:
            incorrect_response()

    input("To progress to next level write next")

    type_out("Computer: We recovered an image from the email, it is inside the enum folder and it is named 'mksteg'.")
    type_out("John: Could there be something hidden in there.")
    type_out("Hint: Use https://futureboy.us/ and research steganography")

    while True:
        answer = input("> ").strip().lower()
        if answer == "username: jacksmith, ip:192.168.1.1":
            simulate_commands([
                ">> username: jacksmith",
                ">> ip:192.168.1.1",
            ])
            type_out("Computer: We found the shh username and ip to the server")
            type_out("John: Let's wipe the servr then")
            break
        else:
            incorrect_response()

    input("To progress to next level write next")

    type_out("Computer: We need a shell on the server to wipe the data.")
    type_out("Hint: *** ***@***.***.***.***, research about shells")

    while True:
        answer = input("> ").strip().lower()
        if answer == "ssh jacksmith@192.168.1.1":
            simulate_commands([
                ">> Scanning ports...",
                ">> Open port found: 22 (SSH)",
                ">> Attempting connection...",
                ">> Authentication successful. Welcome jacksmith.",
            ])
            type_out("Connecting to server via SSH...")
            break
        else:
            incorrect_response()

    input("To progress to next level write next")

    type_out("Computer: Now is the time to wipe the server.")
    type_out("Hint: delete")

    while True:
        answer = input("> ").strip().lower()
        if answer == "delete":
            simulate_commands([
                ">> Wiping data...",
                ">> Overwriting database files...",
                ">> Deletion complete.",
            ])
            type_out("Computer: Spygle’s data on millions of people has been wiped. Game over.")
            break
        else:
            incorrect_response()

if __name__ == "__main__":
    hacking_game()
