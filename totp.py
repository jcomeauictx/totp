#!/usr/bin/python3 -OO
'''
code adapted from https://pypi.org/project/pyotp/2.0.1/

under "Time based OTPs"
'''
import sys, netrc, logging  # pylint: disable=multiple-imports
import pyotp

logging.basicConfig(level=logging.DEBUG if __debug__ else logging.INFO)

# python2 compatibility
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = OSError  # pylint: disable=redefined-builtin

def totp(machine):
    '''
    return time-based code for given machine
    '''
    seed = seedword(machine)
    return pyotp.TOTP(seed).now()

def seedword(machine):
    '''
    find seedword stored in .netrc for machine

    add as follows:

    machine secure.login.gov
        login me@my.email.addr
        account MYS33DW0RD
        password MyP4ssW0rd

    (all on one line)
    '''
    seed = None
    try:
        machine, seed, _ = netrc.netrc().authenticators(machine)
        logging.debug('found seed "%s"', seed)
        if not seed:
            raise ValueError('Must have non-empty `account` string')
        return seed
    except (FileNotFoundError, IndexError, ValueError) as problem:
        logging.error('Cannot find seedword for "%s": %s', machine, problem)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error('Usage: %s secure.login.gov', sys.argv[0])
    else:
        print(totp(sys.argv[1]))
