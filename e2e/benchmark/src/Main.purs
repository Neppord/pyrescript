module Main where

import Prelude

import Effect (Effect)
import Effect.Console (log)
import PureScript.CST (RecoveredParserResult(..), parseModule)

foreign import open :: String -> Effect String

main :: Effect Unit
main = do
  text <- open "src/Main.purs"
  case parseModule text of
    ParseSucceeded _ -> log "parsed succsesfully"
    ParseSucceededWithErrors _ _ -> log "oups"
    ParseFailed _ -> log "oups"
