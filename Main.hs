
{-# LANGUAGE OverloadedStrings #-}

import Control.Applicative
import qualified Data.ByteString.Lazy as BL
import qualified Data.ByteString.Char8 as C
import Data.Csv
import Data.Char
import qualified Data.Vector as V

data Person = Person
    { volgnummer :: !String
    , uitvoeringsdatum :: !String
    , valutadatum :: !String
    , bedrag :: !String
    , valutaRekening :: !String
    , tegenpartij :: !String
    , details :: !String
    , rekeningnummer :: !String
    }

instance FromNamedRecord Person where
    parseNamedRecord r = Person <$> r .: "Volgnummer" <*> r .: "Uitvoeringsdatum" <*> r .: "Valutadatum" <*> r .: "Bedrag" <*> r .: "Valuta rekening" <*> r .: "TEGENPARTIJ VAN DE VERRICHTING" <*> r .: "Details" <*> r .: "Rekeningnummer"

myOptions = defaultDecodeOptions {
      decDelimiter = fromIntegral (ord ';')
    }

main :: IO ()
main = do
    csvData <- BL.readFile "BE03001625311384-20200712.csv"
    case decodeByNameWith myOptions csvData of
        Left err -> putStrLn err
        Right (_, v) -> V.forM_ v $ \ p ->
            putStrLn $ volgnummer p ++ " heeft bedrag " ++ show (bedrag p) ++ " dollars"