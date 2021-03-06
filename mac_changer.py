#!/usr/bin/env python3

from subprocess import call, check_output
import optparse  # Allow creating arguments alongside the script
import re


def print_banner():
    print("""
            ##     ##    ###     ######
            ###   ###   ## ##   ##    ##
            #### ####  ##   ##  ##
            ## ### ## ##     ## ##
            ##     ## ######### ##
            ##     ## ##     ## ##    ##
            ##     ## ##     ##  ######
               ###    ########  ########  ########  ########  ######   ######
              ## ##   ##     ## ##     ## ##     ## ##       ##    ## ##    ##
             ##   ##  ##     ## ##     ## ##     ## ##       ##       ##
            ##     ## ##     ## ##     ## ########  ######    ######   ######
            ######### ##     ## ##     ## ##   ##   ##             ##       ##
            ##     ## ##     ## ##     ## ##    ##  ##       ##    ## ##    ##
            ##     ## ########  ########  ##     ## ########  ######   ######
             ######  ##     ##    ###    ##    ##  ######   ######## ########
            ##    ## ##     ##   ## ##   ###   ## ##    ##  ##       ##     ##
            ##       ##     ##  ##   ##  ####  ## ##        ##       ##     ##
            ##       ######### ##     ## ## ## ## ##   #### ######   ########
            ##       ##     ## ######### ##  #### ##    ##  ##       ##   ##
            ##    ## ##     ## ##     ## ##   ### ##    ##  ##       ##    ##
             ######  ##     ## ##     ## ##    ##  ######   ######## ##     ##
         """
          )


def init_banner():
    print_banner()
    options = get_arguments()
    change_mac_address(options)
    get_current_mac(options)


def get_arguments():
    option_parser = optparse.OptionParser()

    option_parser.add_option('-i', '--interface', dest='network_interface',
                             help='Interface to change its MAC Address')

    option_parser.add_option('-m', '--mac', dest='new_mac_address',
                             help='New MAC Address')

    (options, _) = option_parser.parse_args()

    if not options.network_interface:
        option_parser.error(
            '[-] Please, specify an interface, use --help for more details')

    if not options.new_mac_address:
        option_parser.error(
            '[-] Please, specify a MAC Address, use --help for more details')

    return options


def change_mac_address(options):
    new_mac = options.new_mac_address
    network_interface = options.network_interface

    print('[+] Changing the MAC Address to {}....'.format(new_mac))

    call(['ifconfig', network_interface, 'down'])
    call(['ifconfig', network_interface, 'hw', 'ether', new_mac])
    call(['ifconfig', network_interface, 'up'])

    print('[+] MAC Address changed!')


def get_current_mac(options):

    ifconfig_result = check_output(['ifconfig', options.interface])
    mac_address_search_result = re.search(
        r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result)

    if mac_address_search_result:
        print(mac_address_search_result.group(0))
    else:
        print('[-] Could not read the MAC Address.')


init_banner()
