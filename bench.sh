#!/usr/bin/env sh
find e2e/acme/.spago -iname *.purs -exec ./pyrs-c.exe {} \+ >/dev/null

