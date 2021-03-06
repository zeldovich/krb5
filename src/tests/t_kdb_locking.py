#!/usr/bin/python

# This is a regression test for
# https://bugzilla.redhat.com/show_bug.cgi?id=586032 .
#
# We start a KDC, remove the kadm5 lock file, use the KDC, re-create the
# kadm5 lock file, and use kadmin.local.  The kinit should fail, and the
# kadmin.local should succeed.


import os

from k5test import *

p = 'foo'
realm = K5Realm(create_user=False)
realm.addprinc(p, p)

kadm5_lock = os.path.join(realm.testdir, 'db.kadm5.lock')
if not os.path.exists(kadm5_lock):
    fail('kadm5 lock file not created: ' + kadm5_lock)
os.unlink(kadm5_lock)

output = realm.kinit(p, p, [], expected_code=1)
if 'A service is not available' not in output:
    fail('krb5kdc should have returned service not available error')

f = open(kadm5_lock, 'w')
f.close()

output = realm.run_kadminl('modprinc -allow_tix ' + p)
if 'Cannot lock database' in output:
    fail('krb5kdc still holds a lock on the principal db')

success('KDB locking tests')
