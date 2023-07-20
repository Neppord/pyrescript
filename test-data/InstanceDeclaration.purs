module InstanceDeclaration where

import Data.Show (class Show)
import Data.Show (class Show) as Show

instance Show Int where
    show i = "<Int>"

instance Show Number where show i = "<Number>"
instance Show.Show Number where show i = "<Number>"


{- TODO: connect where with a
instance A where
  a = do
    [1]
    where
    x = 1
-}