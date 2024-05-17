#!/usr/bin/env python
#  buzz [--server URL] [--token TOKEN] list
"""
Buzz client

Usage:
    buzz [options] list
    buzz [options] version
    buzz [options] send <notifier> --recipient <recipient> [--title <title>] [--severity <severity>] [--attach <file>] [<body>...]
    buzz --version


Options:
    -h  --help                   show this help message and exit
    -v --version                 show version and exit
    -s URL --server=URL          API URL
    -t TOKEN --token=TOKEN       API Auth token

    --recipient <recipient>      the recipient of the notification,
                                 must be valid for the notifier chosen
    --title <title>              the title of the notification. [default: You received a buzz]
    --severity <severity>        the severity of the message. [default: info]
                                 One of: 'info', 'success', 'warning', 'failure'
    --attach <file>              a file you want to attach to the notification

    <notifier>                   the notifier you want to use,
                                 you can see the available notifiers using `list` command

    <body>                       Content of the notification,
                                 if not specified read from stdin
Environment variables:
    - BC_API         API URL, overrides command line argument
    - BC_TOKEN       API token, overrides command line argument
"""
from docopt import docopt
import sys
from buzz_client.client import BuzzClient
from scriptonite.configuration import Configuration
from scriptonite.logging import Logger
import logging

log = Logger(format="short", level=logging.INFO)


def main():
    arguments = docopt(__doc__, version="1.0.0")

    print(arguments)

    client_configuration = Configuration()
    client_configuration.from_mapping(
        dict(api=arguments.get('--server'), token=arguments.get('--token')))
    client_configuration.from_environ(prefix="BC")

    client = BuzzClient(client_configuration)

    if arguments.get('version'):
        log.info(f"Server version: {client.api_version}")
        exit(0)

    if arguments.get('list'):
        log.info("Available notifiers")
        log.info("-" * len("Available notifiers"))
        for notifier in client.notifiers:
            log.info(notifier)
        exit(0)

    if arguments.get('send'):
        if arguments.get('<body>'):
            body = [" ".join(arguments.get('<body>'))]  # type: ignore
        else:
            body = []
            for line in sys.stdin:
                body.append(line.rstrip())

        r = client.send(notifier=arguments.get('<notifier>'),  # type: ignore
                        title=arguments.get('--title'),  # type: ignore
                        recipient=arguments.get('--recipient'),  # type: ignore
                        body="\n".join(body),
                        severity=arguments.get('--severity'),  # type: ignore
                        attach=arguments.get('--attach')  # type: ignore
                        )
        log.info(
            f"{r.json().get('detail')} [{r.status_code}]")


if __name__ == "__main__":
    main()
