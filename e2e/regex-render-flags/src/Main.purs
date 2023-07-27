module Main where

import Prelude

import Data.String.Regex.Flags (noFlags)
import Data.String.Regex (renderFlags)
import Effect (Effect)
import Effect.Console (log)

main :: Effect Unit
main = log $ renderFlags noFlags
