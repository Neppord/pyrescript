#!/usr/bin/env sh
find e2e/acme/.spago -iname *.purs -exec ../pypy2.7-v7.3.12-win64/pypy ./pyrs.py {} \+ >/dev/null