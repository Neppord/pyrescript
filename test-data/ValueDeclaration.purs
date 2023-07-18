module Main where

import Prelude

import Effect (Effect)
import Effect.Console (log)

main :: Effect Unit
main = log "hello world!"

for_all :: forall a. a -> a
for_all a = a

needs_name :: forall r. {name :: String | r} -> String
needs_name r = r.a
layout1 ::
  Int
layout1 =
  1
layout2
  :: Int
layout2
  = 1
layout3
  =
  1