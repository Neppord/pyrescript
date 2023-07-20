module ClassDeclaration where

class Const :: Type
class Const f where
    value :: f -> Int

class Const f <= MyConst f where
    my_value :: f -> Int

class Const f <= OtherConst f

class Const f <= SimpleConst f where my_value :: f -> Int
