module Main where

import Prelude

import Effect (Effect)
import Effect.Console (log)

foreign import hello_world :: String

main :: Effect Unit
main = do
  log hello_world
