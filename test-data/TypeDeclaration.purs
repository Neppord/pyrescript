module TypeDeclaration where

import Data.Maybe (Maybe) as Maybe

type User = Int
type Nodes a = Array a
type Point = (x :: Int, y :: Int)
type Layout =
  { x :: Int
  , y :: Int
  }

type X = Maybe.Maybe