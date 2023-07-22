module Main where

import Prelude

import Effect (Effect)
import Effect.Console (log)

main :: Effect Unit
main = log case 42 of
    n 
        | n == 30 -> "What"
        | otherwise -> "Hello world!"

