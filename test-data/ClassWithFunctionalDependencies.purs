module ClassWithFunctionalDependencies where

class A m x | m -> x where
    go :: m -> x