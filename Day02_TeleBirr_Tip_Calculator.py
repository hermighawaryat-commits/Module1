bill_total = 100000
people = ["sami", "abebe", "chala"]


def split_bill(total, people, tip_rate=0.10):

    if len(people) == 0:
       return("Number of people must be greater than zero")

    tip_amount = total * tip_rate
    total_with_tip = total + tip_amount
    amount_per_person = total_with_tip / len(people)

    for person in people:
        print(f"{person}: {amount_per_person}")

    return amount_per_person

split_bill(bill_total, people)
