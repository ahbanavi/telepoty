import asyncio
from telegram import main as telegram_main
from spotify import get_uri, add_songs_from_uri
from helpers import read_data, write_data


def main():
    # load data
    data = read_data()

    # clear items with uri
    data["items"] = [item for item in data["items"] if not item.get("uri", False)]

    # get data from telegram
    data = asyncio.run(telegram_main(data))

    # find uri
    data = get_uri(data)

    # add songs to playlist
    add_songs_from_uri(data)

    # write data
    write_data(data)

    print("Done!")


if __name__ == "__main__":
    main()
