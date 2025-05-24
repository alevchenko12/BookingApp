from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.city import City

# Cities to insert by new country IDs
cities_by_country_id = {
    31: ["Vienna", "Salzburg", "Innsbruck"],                  # Austria
    32: ["Brussels", "Bruges", "Antwerp"],                    # Belgium
    33: ["Sofia", "Plovdiv", "Varna"],                        # Bulgaria
    34: ["Zagreb", "Dubrovnik", "Split"],                     # Croatia
    35: ["Nicosia", "Limassol", "Larnaca"],                   # Cyprus
    36: ["Prague", "Brno", "Ostrava"],                        # Czech Republic
    37: ["Copenhagen", "Aarhus", "Odense"],                   # Denmark
    38: ["Tallinn", "Tartu", "Narva"],                        # Estonia
    39: ["Helsinki", "Espoo", "Turku"],                       # Finland
    40: ["Paris", "Nice", "Lyon"],                            # France
    41: ["Berlin", "Munich", "Hamburg"],                      # Germany
    42: ["Athens", "Thessaloniki", "Santorini"],              # Greece
    43: ["Budapest", "Debrecen", "Szeged"],                   # Hungary
    44: ["Dublin", "Cork", "Galway"],                         # Ireland
    45: ["Rome", "Venice", "Florence"],                       # Italy
    46: ["Riga", "Daugavpils", "Liepaja"],                    # Latvia
    47: ["Vilnius", "Kaunas", "Klaipeda"],                    # Lithuania
    48: ["Luxembourg City", "Esch-sur-Alzette", "Differdange"],  # Luxembourg
    49: ["Valletta", "Sliema", "St. Julian's"],               # Malta
    50: ["Amsterdam", "Rotterdam", "Utrecht"],                # Netherlands
    51: ["Warsaw", "Krakow", "Gdansk"],                       # Poland
    52: ["Lisbon", "Porto", "Faro"],                          # Portugal
    53: ["Bucharest", "Cluj-Napoca", "Brasov"],               # Romania
    54: ["Bratislava", "Kosice", "Presov"],                   # Slovakia
    55: ["Ljubljana", "Bled", "Maribor"],                     # Slovenia
    56: ["Barcelona", "Madrid", "Seville"],                   # Spain
    57: ["Stockholm", "Gothenburg", "Malmo"],                 # Sweden
    58: ["Zurich", "Geneva", "Bern"],                         # Switzerland
    59: ["Kyiv", "Lviv", "Odesa"]                             # Ukraine
}

db: Session = SessionLocal()
inserted = 0
skipped = 0

for country_id, city_names in cities_by_country_id.items():
    for name in city_names:
        existing = db.query(City).filter(
            City.name == name,
            City.country_id == country_id
        ).first()
        if existing:
            print(f"Skipping '{name}' in country {country_id} (already exists)")
            skipped += 1
            continue

        city = City(name=name, country_id=country_id)
        db.add(city)
        inserted += 1

db.commit()
db.close()

print(f"{inserted} cities inserted.")
print(f"{skipped} cities skipped (already existed).")
