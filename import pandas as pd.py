import pandas as pd
import random
from faker import Faker

def generate_dealer_data(num_records=2000):
    fake = Faker()
    Faker.seed(42)
    random.seed(42)

    dealer_rows = []

    for _ in range(num_records):
        first = fake.first_name()
        last = fake.last_name()
        nicknames = [first.lower(), fake.user_name()]
        nametag_id = random.choice(nicknames).capitalize()

        ee_number = "700" + str(random.randint(1000000, 9999999))
        email = f"{first.lower()}.{last.lower()}@dealersim.com"
        phone = fake.phone_number()

        ft_pt = random.choice(["FULL TIME", "PART TIME"])

        dealer_group = random.choices(
            ["Any", "Holdem", "Live"],
            weights=[0.7, 0.2, 0.1],
            k=1
        )[0]

        avail_days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        if ft_pt == "FULL TIME":
            num_avail = random.choice([5, 6, 7])
        else:
            num_avail = random.choice([3, 4])

        selected_days = random.sample(avail_days, num_avail)
        availability = {f"AVAIL-{day}": day in selected_days for day in avail_days}

        dealer = {
            "first_name": first,
            "last_name": last,
            "nametag_id": nametag_id,
            "ee_number": ee_number,
            "email": email,
            "phone": phone,
            "ft_pt": ft_pt,
            "dealer_group": dealer_group,
            **availability,
            "User_Added": True
        }

        dealer_rows.append(dealer)

    return pd.DataFrame(dealer_rows)

# Generate and export
df = generate_dealer_data()
df.to_excel("dealer_master_list.xlsx", index=False)
print("✅ Synthetic dealer_master_list.xlsx generated.")