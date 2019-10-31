import json
from datetime import datetime


# additional imports if needed

# global variables
SHOWS_FILE = "./shows.json"
TRANSACTIONS_FILE = "./transactions.txt"
TICKET_FILE = "./ticket.txt"
SALES_TAX = 0.07  # 7% Sales Tax


def load(filename):
    with open(filename) as file:
        concert_data = json.load(file)
    return concert_data


def print_shows(all_shows):
    show_list = [i.get("artist") for i in all_shows]
    for i in show_list:
        print(i)


def get_show(all_shows):
    show_list = [i.get("artist") for i in all_shows]
    while True:
        ordered_show = input(
            """who's show would you like to go to
        >>> """
        )
        if ordered_show not in show_list:
            print("-----------")
            print(f"Sorry we do not have {ordered_show}")
            print("-----------")
            continue
        for shows in all_shows:
            if ordered_show == shows.get("artist"):
                if shows.get("tickets") > 0:
                    return ordered_show
                    break
                else:
                    print("-----------")
                    print("Sorry that show is sold out pick another!")
                    print("-----------")
                    continue


def get_price(ordered_shows, all_shows):
    for shows in all_shows:
        if ordered_shows == shows.get("artist"):
            return shows.get("price")


def get_tickets(ordered_shows, all_shows):
    for shows in all_shows:
        if ordered_shows == shows.get("artist"):
            return shows.get("tickets")


def get_code(ordered_shows, all_shows):
    for shows in all_shows:
        if ordered_shows == shows.get("artist"):
            return shows.get("code")


def valid_tickets(all_shows, tickets):
    print("-----------")
    print(f"That Show has {tickets} tickets available")
    print("-----------")
    if tickets == 0:
        print("Sorry this show is sold out pick another one!")
        print("-----------")
    while True:
        amount_of_tickets = int(
            input(
                """How many tickets do you want? 
        >>> """
            )
        )
        if amount_of_tickets <= tickets:
            if amount_of_tickets <= 4:
                print("-----------")
                print(f"That will be {amount_of_tickets} for one lonely person")
                print("-----------")
                print("Please enjoy the show")
                return amount_of_tickets
                break
            else:
                print("-----------")
                print("You can only buy at most 4 tickets")
                print("-----------")
        else:
            print("-----------")
            print(f"We only have {tickets} tickets")
            print("-----------")
            continue


def transaction(name, ordered_shows, code, tickets, price, tax, timestamp):
    return f"{name}, {ordered_shows}, {code}, {tickets}, ${price:.2f}, ${tax:.2f}, {timestamp}"


def transaction_txt(filename, trans_summary):
    with open(filename, "a") as trans_file:
        trans_file.write(trans_summary)


def update_json(ordered_shows, amount_of_tickets):
    with open(SHOWS_FILE) as shows:
        plays = json.load(shows)
    for idx, value in enumerate(plays):
        if ordered_shows == value.get("artist"):
            plays[idx]["tickets"] = abs(amount_of_tickets - plays[idx]["tickets"])
            with open(SHOWS_FILE, "w") as shows:
                json.dump(plays, shows)


def main():
    name = input("What's your name: ")
    print(f"Welcome to The Jefferson venue ticket purchasing tool {name}!")
    all_shows = load(SHOWS_FILE)
    print(f"which show would you like to go to, {name}?")
    print("""-----------""")
    print_shows(all_shows)
    print("""-----------""")
    ordered_shows = get_show(all_shows)
    tickets = get_tickets(ordered_shows, all_shows)
    amount_of_tickets = valid_tickets(all_shows, tickets)
    update_json(ordered_shows, amount_of_tickets)
    price = get_price(ordered_shows, all_shows) * amount_of_tickets
    tax = price * SALES_TAX
    code = get_code(ordered_shows, all_shows)
    timestamp = datetime.now()
    trans_summary = transaction(
        name, ordered_shows, code, amount_of_tickets, price, tax, timestamp
    )
    transaction_txt(TRANSACTIONS_FILE, trans_summary)


if __name__ == "__main__":
    main()
