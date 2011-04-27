
from attest import Tests
from tests.dbgp.socket_ import socktest
from tests.dbgp.dbgpconnection import dbgpcon_test

tests = Tests([
    socktest,
    dbgpcon_test,
])

