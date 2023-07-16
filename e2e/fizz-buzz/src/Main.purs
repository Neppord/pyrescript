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
main = do
    log (fizzbuzz 1)
    log (fizzbuzz 2)
    log (fizzbuzz 3)
    log (fizzbuzz 4)
    log (fizzbuzz 5)
    log (fizzbuzz 6)
    log (fizzbuzz 7)
    log (fizzbuzz 8)
    log (fizzbuzz 9)
    log (fizzbuzz 10)
    log (fizzbuzz 11)
    log (fizzbuzz 12)
    log (fizzbuzz 13)
    log (fizzbuzz 14)
    log (fizzbuzz 15)
