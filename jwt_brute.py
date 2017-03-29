#!/usr/bin/env python

import sys
import jwt
import json
import multiprocessing as mp
from multiprocessing import current_process
import argparse
import Queue
from time import sleep

debug = False
wordlist_q = mp.Manager().Queue()
found = mp.Manager().Queue()

default_keys = ["secret",
                "secret123",
                "use-a-good-secret-here",
                "my_secret",
                "random_secret_key",
                "secret-key",
                "LongAndHardToGuessValueWithSpecialCharacters@^($%*$%",
                "my-firebase-secret"]


def check(token, wordlist_q, found):
    print "[*] Cracking JWT"
    while found.empty() and wordlist_q.empty() is False:
        try:
            candidate = wordlist_q.get()
        except:
            continue
        try:
            if debug:
                print "[*] Trying key: %s" % candidate
            pd = jwt.decode(token, key=candidate)
            print "[!] Found key: %s" % candidate
            found.put(candidate)
        except jwt.DecodeError:
            wordlist_q.task_done()

    return


def mk_queue(wordlist, q):
    print "[*] Loading wordlist"
    with open(wordlist, 'rb') as fin:
        for key in default_keys:
            q.put(key)

        for line in fin:
            q.put(line.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jwt', '-j', type=str, help='JWT to brute force', required=True)
    ap.add_argument('--wordlist', '-w', type=str, help='Wordlist', required=True)
    ap.add_argument('--threads', '-t', type=str, help='Processing threads', default=mp.cpu_count())
    args = ap.parse_args()

    token = args.jwt
    header, payload, signature = token.split('.')

    mk_queue(args.wordlist, wordlist_q)
    print "Loaded %i words" % wordlist_q.qsize()
    processes = [mp.Process(target=check, args=(token, wordlist_q, found)) for i in range(args.threads)]

    for proc in processes:
        proc.start()

    mk_queue(args.wordlist, wordlist_q)

    for proc in processes:
        proc.join()


if __name__ == '__main__':
    main()
