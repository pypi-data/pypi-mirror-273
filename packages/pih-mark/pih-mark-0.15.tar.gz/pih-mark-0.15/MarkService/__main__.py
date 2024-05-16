import ipih


def start() -> None:
    from MarkService.service import start

    start(True)


if __name__ == "__main__":
    start()
