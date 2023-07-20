module Records where

import Prelude

identifier x = { x }

get_type { "type": x } = x

r :: forall r. { | r } -> Int
r x = 1