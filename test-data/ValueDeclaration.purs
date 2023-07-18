module Main where

import Prelude

import Effect (Effect)
import Effect.Console (log)

main :: Effect Unit
main = log "hello world!"

for_all :: forall a. a -> a
for_all a = a

needs_name :: {name :: String} -> String
needs_name r = r.a