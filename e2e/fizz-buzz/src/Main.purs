module Main where

import Prelude

import Data.EuclideanRing (mod)
import Data.Show (show)
import Effect (Effect)
import Effect.Console (log)
import Data.Foldable (for_)
import Data.Array ((..))

divisibleBy :: Int -> Int -> Boolean
divisibleBy n d = mod n d == 0

fizzbuzz :: Int -> String
fizzbuzz n =
  let
    divBy = divisibleBy n
  in
    if divBy (3 * 5) then "Fizz" <> "Buzz"
    else if divBy 3 then "Fizz"
    else if divBy 5 then "Buzz"
    else show n

main :: Effect Unit
main = for_ (1 .. 15) \n -> do
    log (fizzbuzz n)
