module LetBinding where

import Data.Tuple.Nested ((/\))

a =
    let
        x /\ y = 1 /\ 2
    in x
b = let x /\ y = 1 /\ 2 in x

c = let
        x /\ y = 1 /\ 2
    in x
e =
  let
    x /\ y = 1 /\ 2
    in x