module ForeignDeclaration where

import Effect (Effect)

foreign import function :: Int -> Int
foreign import effectful :: Int -> (Effect Int)