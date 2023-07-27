module Main where

import Prelude

import Effect (Effect)
import Effect.Console (log)
import Data.Either (Either(..))
import Data.Maybe (Maybe(..))
import Data.Array.NonEmpty.Internal (NonEmptyArray(NonEmptyArray))
data Box a = Box a

main :: Effect Unit
main = log case Box true of
  Right true -> case Just (NonEmptyArray [Just "Success"]) of
    Nothing -> "Failed inner"
    Just (NonEmptyArray [Just str]) -> str
    _ -> "Unknown failure"
  _ -> "Failed"
