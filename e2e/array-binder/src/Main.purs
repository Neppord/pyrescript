module Main where

import Prelude

import Effect (Effect)
import Effect.Console (log)

main :: Effect Unit
main = log case [ "Hello world!" ] of
  [ str ] -> str
  _ -> "Error"

