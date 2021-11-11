# Backend Server API Docs

## Crime Data (From Crime Data Explorer (CDE))
Get number of crimes committed in an ORI with a date range:
`/crimedata/api/{ORI}/{fromDate}{toDate}`

## Geocoding API (From MapQuest)
Get longitude and latitude from location:
`/geocoding/api/{location}`

## Safe Living Score

Get the safe living score for an area: `/safelivingscore/api/{lon}/{lat}/{radius}`

Get the crime score for an ORI: `/safelivingscore/api/{ORI}`

## Amenities API
Get a list of shopping places in an area: `/amenities/api/{lon}/{lat}/{radius}`

## Transportation Scores
Get the walk score for an area: `/transportation/api/walkscore/{lon}/{lat}`