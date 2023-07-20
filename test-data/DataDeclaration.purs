module DataDeclaration where

data Choice a
    = None
    | One a
    | More a (Choice a)

data Aggregate (fields :: Row Type) = Count input
