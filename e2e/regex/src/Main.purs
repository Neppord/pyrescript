module Main where

import Data.String.Regex
import Prelude

import Data.Either (Either(..))
import Data.Maybe (Maybe(..))
import Data.String.Regex.Flags (noFlags)
import Effect (Effect)
import Effect.Console (log)
import Data.Array.NonEmpty.Internal (NonEmptyArray(NonEmptyArray))

main :: Effect Unit
main = log case regex "hello world" noFlags of
  Right re -> case match re "I said: hello world" of
    Nothing -> "Diddnt match anything"
    Just (NonEmptyArray [Just str]) -> "success! matched: " <> str
    _ -> "Unknown failure"
  Left reason -> "Failed: " <> reason
