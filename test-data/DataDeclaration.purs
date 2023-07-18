module DataDeclaration where

data Choice a
    = None
    | One a
    | More a (Choice a)