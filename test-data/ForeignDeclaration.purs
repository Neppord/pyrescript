module ForeignDeclaration where

import Effect (Effect)

foreign import function :: Int -> Int
foreign import effectful :: Int -> (Effect Int)
foreign import record :: { age :: Int }
foreign import user :: { age :: Int, name :: String }
foreign import empty :: {}