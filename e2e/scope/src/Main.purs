module Main where

import Prelude

import Effect (Effect)
import Effect.Console (log)

f x = \y -> x 

main :: Effect Unit
main = do
  log (f "Hello" "World")
