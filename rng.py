import ephem
import json


def sun_constelation(date):
    sun = ephem.Sun()
    sun.compute(date, epoch='1875')
    const = ephem.constellation(sun)
    return const, sun


def moon_constelation(date):
    moon = ephem.Moon()
    moon.compute(date, epoch='1875')
    const = ephem.constellation(moon)
    return const, moon


def replace_ophiuchus(stars_body, target_constellation):
    """
    Oph is a real starsign
    so, we are gonna chuck it away for Sco
    """
    try:
        stars_body[target_constellation[0]]
        print("The constellation is ", target_constellation[1])
    except:
        print("We think the constellation is ", target_constellation[1])
        target_constellation = ("Sco", "Scorpio")

    print("the star is: ", stars_body[target_constellation[0]]["name"])
    return target_constellation


def normaliser(value):
    """
    want to end up with a number between 1 and 10000
    """
    if value > 10000:
        while value > 10000:
            value *= 0.75
    elif value < 1:
        while value < 1:
            value *= 10

    value = int(value)
    return value


def load_json(path):
    # Opening JSON file
    f = open(path)

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Closing file
    f.close()
    return data


def convert_to_fixedbody(star_json):
    """
    from our json, wouldnt it be nice to have
    actual pyephem objects?
    """
    stars_body = {}
    for x in star_json:
        st = ephem.FixedBody()
        st._ra = ephem.hours(star_json[x]["ra"])
        st._dec = ephem.degrees(star_json[x]["dec"])
        st.compute(epoch='1875')

        stars_body[x] = {"name": star_json[x]["name"],
                         "star body": st}

    return stars_body


stars = load_json("brightest.json")
stars_body = convert_to_fixedbody(stars)


def number_generator(date):
    sun_const, sun = sun_constelation(date)
    moon_const, moon = moon_constelation(date)

    sun_const = replace_ophiuchus(stars_body, sun_const)
    moon_const = replace_ophiuchus(stars_body, moon_const)

    sun_const_bright = stars_body[sun_const[0]]["star body"]
    moon_const_bright = stars_body[moon_const[0]]["star body"]

    moon_dist = ephem.separation(moon, moon_const_bright)
    moon_dist = float(moon_dist)*100

    sun_dist = ephem.separation(sun, sun_const_bright)
    sun_dist = float(sun_dist)*100

    print("sun dist: ", sun_dist)
    print("moon dist: ", moon_dist)

    value = moon_dist * sun_dist
    value = normaliser(value)

    return value


if __name__ == "__main__":
    date = "2021/12/24"

    print(number_generator(date))
