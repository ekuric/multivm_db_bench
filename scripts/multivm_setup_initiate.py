#!/usr/bin/env python2
# coding: utf-8

# Author: Archit Sharma <archit.py@gmail.com>

import os, sys
from pssh import ParallelSSHClient, utils

# utils.enable_host_logger()

USERNAME='root'
DIRNAME = '/root'
UTIL_NAMES = ['sysbench_utilities.tgz', 'sysbench-0.4.12.tar.gz']
SCRIPT_NAMES = ['automate_sysbench.sh', 'setup_sysbench.sh',
                'multivm_setup_initiate.py', 'start_sysbench_tests.sh']

FILENAMES = SCRIPT_NAMES + UTIL_NAMES


def display_files(client, hosts, msg, files_to_display, target_dir):
    print(msg)
    output = client.run_command('ls -lh ' + os.path.join(target_dir, '{%s}' %
                                                (','.join(files_to_display))))
    client.get_exit_codes(output)
    for host in hosts:
        print("host: %s -- exit_code: %s" %(host, output[host]['exit_code']))
        for line in output[host]['stdout']: print line
        print

def make_executable(client, hosts, target_files, target_dir):
    print("changing mode +x for all scripts..\n")
    output = client.run_command('chmod +x ' + os.path.join(target_dir, '{%s}' %
                                                (','.join(target_files))))
    client.get_exit_codes(output)
    for host in hosts:
        print("host: %s -- exit_code: %s" %(host, output[host]['exit_code']))
        try:
            for line in output[host]['stdout']:
                    print line
        except:
            pass

def copy_files(client, files_to_copy, target_dir):
    print("\ncopying file..\n")
    for filename in files_to_copy:
        client.copy_file('./%s'%(filename),
                        os.path.join(target_dir, '%s' % (filename)))

    client.pool.join()

def delete_files(client, hosts, files_to_delete, target_dir):
    print("\ndeleting file..\n")
    output = client.run_command('rm -f ' + os.path.join(target_dir, '{%s}' %
                                                (','.join(files_to_delete))))
    client.get_exit_codes(output)
    for host in hosts:
        print("host: %s -- exit_code: %s" %(host, output[host]['exit_code']))


if __name__=='__main__':
    hosts = open(sys.argv[1], 'rb').read().splitlines()
    while '' in hosts: hosts.remove('')
    client = ParallelSSHClient(hosts, user=USERNAME)

    display_files(client, hosts, "\noutput BEFORE COPYING files..\n",
                FILENAMES, DIRNAME)
    copy_files(client, FILENAMES, DIRNAME)
    make_executable(client, hosts, SCRIPT_NAMES, DIRNAME)
    display_files(client, hosts, "\noutput AFTER COPYING files..\n",
                FILENAMES, DIRNAME)
    # delete_files(client, hosts, FILENAMES, DIRNAME)
    # display_files(client, hosts, "\noutput AFTER DELETING files..\n",
    #             FILENAMES, DIRNAME)
