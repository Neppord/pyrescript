module ClassDeclaration where

class Const f where
    value :: f -> Int

class Const f <= MyConst f where
    my_value :: f -> Int