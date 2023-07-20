module CaseExpression where

import Data.Maybe (Maybe(..))

x = case _ of
    0 -> 0
    _ -> 1


y =
  case _ of
    Just 1 -> 1
    Just _ -> 1 -- comment
    Nothing -> 0