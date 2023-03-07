#!/usr/bin/env python3
# URLS_FILE must contain collection repo URLS, one per line
# ./gen_dashboard.py REPO_URLS_FILE DASHBOARD_FILE.md

import sys

#BADGE_TEMPLATE = '[![[%s](%s)](%s/workflows/Plugins%%20CI/badge.svg?event=push)]\n'
BADGE_TEMPLATE = '[![%s](%s/workflows/Plugins%%20CI/badge.svg?event=push)]\n'


def check_arg_num():
    if len(sys.argv) != 3:
        print('Use: ./gen_dashboard.py REPO_URLS_FILE DASHBOARD_FILE.md')
        sys.exit(1)


def generate_dashboard(url_file, dashboard_file):
    for url in url_file:
        url = url.rstrip('\n')
        name = ('/').join(url.split('/')[-2:])
        dashboard_file.write(BADGE_TEMPLATE % (name, url))


def main():
    check_arg_num()

    # Open files
    url_file = open(sys.argv[1], 'r')
    dashboard_file = open(sys.argv[2], 'w')

    # Generate the dashboard
    generate_dashboard(url_file, dashboard_file)

    # Clean up and exit
    url_file.close()
    dashboard_file.close()

    sys.exit(0)


if __name__ == '__main__':
    main()
