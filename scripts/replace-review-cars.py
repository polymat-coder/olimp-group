#!/usr/bin/env python3
"""Replace premium review cars with models from the approved list."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPLICIT_REVIEWS = [
    ("Mercedes-Benz GLE 2024", "Mercedes-Benz GLC 2024", "Mercedes GLE 2024", "Mercedes GLC 2024"),
    ("Porsche Cayenne 2022", "Toyota Land Cruiser Prado 2022", "Porsche Cayenne", "Toyota Land Cruiser Prado"),
    ("Range Rover Sport 2024", "Jeep Grand Cherokee 2024", "Range Rover Sport", "Jeep Grand Cherokee"),
    ("Kia Rio 2023", "Kia Sorento 2023", "Kia Rio", "Kia Sorento"),
    ("Hyundai Solaris 2023", "Hyundai Santa Fe 2023", "Hyundai Solaris", "Hyundai Santa Fe"),
    ("Hyundai Sonata 2023", "Mazda CX-60 2023", "Hyundai Sonata", "Mazda CX-60"),
    ("Land Rover Defender 2023", "Toyota Highlander 2023", "Land Rover Defender", "Toyota Highlander"),
    ("Volvo XC90 2023", "Lexus RX 2023", "Volvo XC90", "Lexus RX"),
    ("Porsche 911 2022", "Genesis GV80 2022", "Porsche 911", "Genesis GV80"),
]

FINAL_NORMALIZATIONS = [
    ("Mercedes-Benz E-Class", "Mercedes-Benz E-Класс"),
    ("Mercedes E-Class", "Mercedes E-Класс"),
]

NEW_40_CARS = [
    "BMW X3 2024",
    "BMW 5 серии 2024",
    "BMW X4 2023",
    "Audi Q5 2024",
    "Audi A6 2023",
    "Mercedes-Benz E-Класс 2024",
    "Mercedes-Benz GLC 2024",
    "Toyota Land Cruiser Prado 2023",
    "Toyota RAV4 2024",
    "Toyota Highlander 2023",
    "Lexus NX 2024",
    "Lexus RX 2023",
    "Mazda CX-60 2024",
    "Mazda CX-9 2023",
    "Hyundai Palisade 2024",
    "Kia Sorento 2023",
    "Hyundai Santa Fe 2024",
    "Genesis GV70 2024",
    "Genesis GV80 2023",
    "Kia Carnival 2024",
    "Geely Monjaro 2024",
    "LiXiang L6 2024",
    "Zeekr 001 2024",
    "Ford Explorer 2023",
    "Jeep Grand Cherokee 2024",
    "Cadillac XT6 2023",
    "BMW X3 2023",
    "BMW 5 серии 2023",
    "Audi Q5 2023",
    "Audi A6 2024",
    "Mercedes-Benz E-Класс 2023",
    "Mercedes-Benz GLC 2023",
    "Toyota RAV4 2023",
    "Lexus NX 2023",
    "Lexus RX 2024",
    "Mazda CX-60 2023",
    "Hyundai Palisade 2023",
    "Kia Sorento 2024",
    "Genesis GV70 2023",
    "Ford Explorer 2024",
]

OLD_40_CARS = [
    "BMW X5 2023",
    "Mercedes-Benz GLE 2024",
    "Audi Q7 2023",
    "Porsche Cayenne 2022",
    "Range Rover Sport 2024",
    "BMW X3 2023",
    "Mercedes-Benz E-Class 2024",
    "Audi A6 2023",
    "Volkswagen Touareg 2023",
    "BMW 5 Series 2024",
    "Mercedes-Benz C-Class 2023",
    "Audi Q5 2024",
    "Porsche Macan 2023",
    "BMW X7 2024",
    "Land Rover Defender 2023",
    "Volkswagen Tiguan 2023",
    "Audi A4 2024",
    "BMW 3 Series 2023",
    "Mercedes-Benz GLC 2024",
    "Volvo XC90 2023",
    "Audi Q3 2024",
    "BMW X1 2023",
    "Mercedes-Benz GLA 2024",
    "Volkswagen Passat 2023",
    "Audi A7 2024",
    "BMW X6 2023",
    "Mercedes-Benz S-Class 2024",
    "Porsche 911 2023",
    "Range Rover Velar 2024",
    "Audi Q8 2023",
    "BMW 7 Series 2024",
    "Mercedes-Benz AMG GT 2023",
    "Audi RS6 2024",
    "Volkswagen Arteon 2023",
    "Volvo XC60 2024",
    "Land Rover Discovery 2023",
    "BMW M5 2024",
    "Mercedes-Benz G-Class 2023",
    "Audi e-tron 2024",
    "Porsche Panamera 2023",
]


def quoted_js_list(cars):
    return 'a=[' + ",".join(f'"{car}"' for car in cars) + "]"


def replace_all(path, replacements):
    content = path.read_text(encoding="utf-8")
    original = content

    for old, new in replacements:
        if old not in content:
            if new in content:
                continue
            raise RuntimeError(f"Expected pattern not found in {path}: {old!r}")
        content = content.replace(old, new)

    path.write_text(content, encoding="utf-8")
    return content != original


def main():
    replacements = []
    for old_car, new_car, old_text, new_text in EXPLICIT_REVIEWS:
        replacements.extend(((old_car, new_car), (old_text, new_text)))

    html_replacements = [
        *replacements,
        ("Привезли Lexus RX из Швеции", "Привезли Lexus RX из Германии"),
        ("BMW X5 2023", "BMW X3 2023"),
        *FINAL_NORMALIZATIONS,
    ]
    js_replacements = [
        (quoted_js_list(OLD_40_CARS), quoted_js_list(NEW_40_CARS)),
        *replacements,
        ("Привезли Lexus RX из Швеции", "Привезли Lexus RX из Германии"),
        *FINAL_NORMALIZATIONS,
    ]

    replace_all(ROOT / "reviews.html", html_replacements)
    replace_all(
        ROOT / "_next/static/chunks/app/reviews/page-ab6c9ef3709db77c.js",
        js_replacements,
    )


if __name__ == "__main__":
    main()
