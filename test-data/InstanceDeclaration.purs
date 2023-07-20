module InstanceDeclaration where

import Data.Show (class Show)

instance Show Int where
    show i = "<Int>"

instance Show Number where show i = "<Number>"
