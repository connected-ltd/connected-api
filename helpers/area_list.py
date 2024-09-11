from app.areas.model import Areas
from app.areas.schema import AreasSchema

# Lists of LGAs and State they belong to in the format LGA - STATE
# NOTE: Update ONLY with areas that do not exist in the same format above
# Make sure all first letters are uppercase 
# TODO: Update the above list wuth more LGAs as we expand
areas = [
    "Kajuru - Kaduna", 
    "Birnin Gwari - Kaduna", 
    "Chikun - Kaduna", 
    "Giwa - Kaduna", 
    "Igabi - Kaduna", 
    "Ikara - Kaduna", 
    "Jaba - Kaduna", 
    "Jema'a - Kaduna", 
    "Kachia - Kaduna", 
    "Kaduna North - Kaduna", 
    "Kaduna South - Kaduna", 
    "Kagarko - Kaduna", 
    "Kaura - Kaduna", 
    "Kauru - Kaduna", 
    "Kubau - Kaduna", 
    "Kudan - Kaduna", 
    "Lere - Kaduna", 
    "Makarfi - Kaduna", 
    "Sabon Gari - Kaduna", 
    "Sanga - Kaduna", 
    "Soba - Kaduna", 
    "Zangon-Kataf - Kaduna", 
    "Zaria - Kaduna", 
    "Akwanga - Nasarawa", 
    "Awe - Nasarawa", 
    "Doma - Nasarawa", 
    "Karu - Nasarawa", 
    "Keana - Nasarawa", 
    "Keffi - Nasarawa", 
    "Kokona - Nasarawa", 
    "Lafia - Nasarawa", 
    "Nasarawa - Nasarawa", 
    "Nasarawa-Eggon - Nasarawa", 
    "Obi - Nasarawa", 
    "Toto - Nasarawa", 
    "Wamba - Nasarawa", 
    "Abaji - FCT", 
    "Abuja - FCT", 
    "Bwari - FCT", 
    "Gwagwalada - FCT", 
    "Kuje - FCT", 
    "Kwali - FCT"
]


def initialize_area():
    # Function for adding area to database upon deployment
    for area_name in areas:
        area_exists = Areas.get_all_by_name(area_name)
        if area_exists: # If area exists, skip
            print(f"Area {area_name} exists. Skipping.......")
        else: # If area does not exist, Add area to the database upon initialization
            print(f"Adding area {area_name}")
            new_area = Areas.create(name=area_name) # Add the area to the database
            print(f"Added area: {AreasSchema().dump(new_area)}")

            
    print("Database Initialization complete!")

