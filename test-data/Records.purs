module Records where

import Prelude

identifier x  =  { x }

get_type { "type" : x } = x