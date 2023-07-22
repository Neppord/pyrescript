module Main where

import Prelude

import Effect (Effect)
import Effect.Console (log)

data Box a = Box a

main :: Effect Unit
main = do
  let
    box = Box "Hello world!"
    Box hello_world = box
  log hello_world
