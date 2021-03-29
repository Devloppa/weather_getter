import requests
from bs4 import BeautifulSoup as bs
from time import sleep
from sys import argv

# verbose = False
verbose = True


def get_weather(zipcode):
    global verbose

    root_url = "https://wunderground.com/q/zipcode:"
    complete_url = root_url + zipcode

    if verbose:
        print(f'Requesting weather from {zipcode}')

    a = requests.get(complete_url)

    if verbose:
        print(f'Parsing content...')

    soup = bs(a.content, 'lxml')
    cur_temp = soup.find("div", {"id": "curTemp"})
    cur_feel = soup.find("dev", {"id": "curFeel"})
    total_time_slept = 0

    if verbose:
        print(f"Entering parsing loop...")

    while cur_temp is None:
        sleep(1)
        total_time_slept += 1
        a = requests.get(complete_url)
        wx_html = a.content
        soup = bs(a.content, "lxml")
        cur_temp = soup.find("div", {"id": "curTemp"})
        cur_feel = soup.find("dev", {"id": "curFeel"})
        print(f'Slept a total of {total_time_slept} seconds')

        if verbose:
            print(f'Aggregating responses')

    temp_set = cur_temp.findChildren("span", recursive=False)
    feel_set = cur_feel.findChildren("span", recursive=False)
    retval = ""
    for item in temp_set:
        if item is not None:
            retval += "".join(item.text.split())
    temp = retval
    retval = ""
    for item in feel_set:
        if item is not None and item.text != "Feels Like":
            retval += "".join(item.text.split())
    feels_like = retval
    return (temp, feels_like)


def main():
    if len(argv) != 2:
        print("usage: python3 weatherget.py [zip_code]")
        exit(-1)
    zipcode = argv[1]
    temperature = get_weather(zipcode)
    print(f"Temp: {temperature[0]}")
    print(f"Feels Like: {temperature[1]}")


if __name__ == '__main__':
    main()
