module Do where

x = do
    let x = 1
    [1]

y =
    [ do
        [1]
    ]

layout = do
  [1]
  where
  x= 1

g b = do
    if b then [1]
    else [2]
