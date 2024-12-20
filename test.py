import csv


offices = [
    {
      "id": 1,
      "name": "HSBC Holdings",
      "coordinates": [-0.017419592045310562, 51.50580488916447],
      "address": "8 Canada Square, Canary Wharf, London E14 5HQ, UK",
      "description": (
          "The headquarters of HSBC, a global financial giant, located in the heart of Canary Wharf. "
          "This building boasts cutting-edge infrastructure, eco-friendly designs, and a modern workspace that attracts leading talent from across the globe. "
          "It includes advanced meeting facilities, flexible office spaces, and a comprehensive security system."
      ),
      "facilities": [
          "Meeting rooms",
          "Cafeteria",
          "Parking",
          "24/7 Security",
          "High-speed elevators",
      ],
  },
  {
      "id": 2,
      "name": "The Shard",
      "coordinates": [-0.0865000039113876, 51.504660248284715],
      "address": "32 London Bridge St, London SE1 9SG, UK",
      "description": (
          "One of London’s most iconic skyscrapers, The Shard is a mixed-use building offering luxury offices with breathtaking views of the city skyline. "
          "It houses various companies in its state-of-the-art workspace that features modern designs and unparalleled amenities, including access to fine dining and event spaces."
      ),
      "facilities": [
          "24/7 Security",
          "High-speed internet",
          "Gym",
          "Private meeting rooms",
          "Restaurant access",
      ],
  },
  {
      "id": 3,
      "name": "30 St Mary Axe (The Gherkin)",
      "coordinates": [-0.08029577507492063, 51.51461195286293],
      "address": "30 St Mary Axe, London EC3A 8BF, UK",
      "description": (
          "Popularly known as 'The Gherkin', this iconic London landmark features a futuristic design and is home to various multinational corporations. "
          "Its eco-efficient architecture ensures reduced energy usage, while its premium office spaces cater to businesses of all sizes. "
          "The building is a symbol of innovation and modernity in London's financial district."
      ),
      "facilities": [
          "Conference halls",
          "Cafeteria",
          "Energy-efficient design",
          "Parking",
          "Panoramic city views",
      ],
  },
  {
      "id": 4,
      "name": "BT Tower",
      "coordinates": [-0.1389712867889066, 51.52215462140962],
      "address": "60 Cleveland St, London W1T 4JZ, UK",
      "description": (
          "Once the tallest building in London, BT Tower is a prominent communication hub. "
          "Its historic significance is matched by its modern amenities, making it a preferred choice for tech companies and startups. "
          "The building provides stunning 360-degree views of London and offers exclusive spaces for corporate events and meetings."
      ),
      "facilities": [
          "Event spaces",
          "High-speed internet",
          "24/7 access",
          "Dedicated server rooms",
          "Scenic views",
      ],
  },
  {
      "id": 5,
      "name": "Centre Point",
      "coordinates": [-0.12975837692482123, 51.5160078553034],
      "address": "103 New Oxford St, London WC1A 1DD, UK",
      "description": (
          "Centre Point is a beautifully restored mid-20th-century tower offering a mix of office spaces and cultural attractions. "
          "Located near Tottenham Court Road, it is a hub of creativity and innovation, ideal for creative agencies and tech firms. "
          "The building features flexible floor plans, modern interiors, and communal areas designed for collaboration."
      ),
      "facilities": [
          "Flexible office spaces",
          "Cafeteria",
          "Recreation areas",
          "Secure bike storage",
          "Nearby public transport",
      ],
  },
  {
      "id": 6,
      "name": "Shakespeare Tower",
      "coordinates": [-0.09479561008334313, 51.52098834271611],
      "address": "Barbican Estate, London EC2Y 8DR, UK",
      "description": (
          "Part of the renowned Barbican complex, Shakespeare Tower is a residential and commercial building offering serene workspaces away from the hustle of central London. "
          "Its proximity to cultural venues like the Barbican Centre makes it an ideal location for companies in the arts and media industries."
      ),
      "facilities": [
          "Quiet environment",
          "Cultural venue access",
          "Secure entry",
          "Dedicated parking",
          "Proximity to public transport",
      ],
  },
  {
      "id": 7,
      "name": "One Canada Square",
      "coordinates": [-0.019468417404192397, 51.50512250292114],
      "address": "Canary Wharf, London E14 5AB, UK",
      "description": (
          "A towering skyscraper in Canary Wharf, One Canada Square is a premium office destination for multinational corporations. "
          "Its sleek design, advanced facilities, and proximity to financial institutions make it a hub for financial and legal services. "
          "The building also offers an array of dining and shopping options nearby, adding to its appeal."
      ),
      "facilities": [
          "Cafeteria",
          "Conference halls",
          "Parking",
          "High-speed elevators",
          "Proximity to shopping areas",
      ],
  },
  {
      "id": 8,
      "name": "10 Upper Bank Street",
      "coordinates": [-0.0170608269258342, 51.50280736584336],
      "address": "Canary Wharf, London E14 5NP, UK",
      "description": (
          "10 Upper Bank Street is a modern office building known for its eco-friendly construction and contemporary workspaces. "
          "With flexible leasing options, it caters to businesses of all sizes, from startups to global corporations. "
          "The building also provides easy access to transportation links and various recreational facilities in Canary Wharf."
      ),
      "facilities": [
          "Rooftop terrace",
          "Gym",
          "Childcare services",
          "Flexible leases",
          "Proximity to public transport",
      ],
  },
  {
      "id": 9,
      "name": "Westfield Stratford City Offices",
      "coordinates": [-0.003804390749762684, 51.54463514335122],
      "address": "Montfichet Rd, London E20 1EJ, UK",
      "description": (
          "Located near one of Europe’s largest shopping centers, Westfield Stratford City Offices offer unparalleled convenience and accessibility. "
          "The building provides a mix of open-plan and private offices designed for productivity and collaboration."
      ),
      "facilities": [
          "Shopping center access",
          "Parking",
          "Event spaces",
          "High-speed internet",
          "On-site cafes",
      ],
  },
  {
      "id": 10,
      "name": "Victoria House",
      "coordinates": [-0.12217284623881178, 51.51959414777511],
      "address": "Bloomsbury Square, London WC1B 4DA, UK",
      "description": (
          "Victoria House is a historic building with a modern twist, offering premium office spaces in the heart of Bloomsbury. "
          "Its classic architecture is complemented by state-of-the-art facilities, making it an ideal choice for law firms and consultancies."
      ),
      "facilities": [
          "Classic architecture",
          "Flexible layouts",
          "24/7 access",
          "On-site cafeteria",
          "Proximity to museums",
      ],
  },
  {
    "id": 11,
    "name": "Lloyd's Building",
    "coordinates": [-0.0822747039107868, 51.51279072667084],
    "address": "1 Lime Street, London EC3M 7HA, UK",
    "description": (
        "The Lloyd's Building, often referred to as the 'Inside-Out Building,' is a high-tech landmark in London's financial district. "
        "Designed by architect Richard Rogers, its unique architecture places services such as lifts and pipes on the exterior. "
        "It is home to Lloyd's of London, the famous insurance market."
    ),
    "facilities": [
        "Conference rooms",
        "Cafeteria",
        "24/7 Security",
        "High-speed elevators",
        "Energy-efficient design",
    ],
},
{
    "id": 12,
    "name": "Broadgate Tower",
    "coordinates": [-0.07940013274584716, 51.52132038968242],
    "address": "20 Primrose Street, London EC2A 2EW, UK",
    "description": (
        "Broadgate Tower is a sleek skyscraper located in the heart of London's business hub. ",
        "Its floor-to-ceiling windows offer stunning views of the city skyline, and it provides state-of-the-art office facilities. "
        "The tower is designed for flexibility and productivity, catering to companies of all sizes."
    ),
    "facilities": [
        "Flexible office spaces",
        "Parking",
        "24/7 access",
        "High-speed internet",
        "Nearby public transport",
    ],
},
{
    "id": 13,
    "name": "Heron Tower (Salesforce Tower)",
    "coordinates": [ -0.08106818856759718, 51.51637330116875],
    "address": "110 Bishopsgate, London EC2N 4AY, UK",
    "description": (
        "Heron Tower, now known as the Salesforce Tower, is a modern skyscraper in London's financial district. "
        "It offers premium office spaces with panoramic views, cutting-edge amenities, and access to some of London's best restaurants and bars on-site."
    ),
    "facilities": [
        "Cafeteria",
        "Rooftop bar",
        "24/7 Security",
        "High-speed elevators",
        "Energy-efficient lighting",
    ],
},
{
    "id": 14,
    "name": "Tower 42",
    "coordinates": [-0.0843778769248678, 51.51550975690947],
    "address": "25 Old Broad Street, London EC2N 1HQ, UK",
    "description": (
        "Tower 42 is one of London's original skyscrapers and remains an iconic presence in the city's skyline. "
        "It offers luxurious office spaces, private dining rooms, and advanced facilities for corporate clients."
    ),
    "facilities": [
        "Conference halls",
        "Private dining",
        "Parking",
        "24/7 Security",
        "Nearby public transport",
    ],
},
{
    "id": 15,
    "name": "One Churchill Place",
    "coordinates":  [-0.014032202807136167, 51.50535635059497],
    "address": "Canary Wharf, London E14 5RB, UK",
    "description": (
        "One Churchill Place is the headquarters of Barclays Bank and one of the tallest buildings in Canary Wharf. "
        "The building features cutting-edge office spaces, robust security systems, and modern amenities tailored for financial institutions."
    ),
    "facilities": [
        "Cafeteria",
        "Conference rooms",
        "Parking",
        "High-speed internet",
        "Proximity to shopping and dining",
    ],
},

]

# Prepare data for CSV
csv_data = []
header = ["id", "name", "latitude", "longitude", "address", "description", "facilities"]
csv_data.append(header)

for office in offices:
    csv_data.append([
        office["id"],
        office["name"],
        office["coordinates"][1],
        office["coordinates"][0],
        office["address"],
        office["description"],
        "; ".join(office["facilities"]),
    ])

# File path for saving the CSV
file_path = "offices.csv"

# Write to CSV
with open(file_path, mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)

file_path
