# json2gostruct

json2struct reads a json file and attempts to generate sensible structs
for the go language. When dealing with unfamiliar APIs that produce deeply
nested responses, defining a data structure to unmarshal the response into is
really a nuisance. Ideally, this script will provide reasonably named structs
that require minimal tweaking for use in go source code.

If executed as main, json2gostruct will read from stdin and write to stdout for
pipelining.

Basic usage:

```
chmod +x json2gostruct.py

curl "http://some.api" | ./json2gostruct.py >> my_structs.go
```

There are a couple sticking points:

1. Arrays with nested data don't have their own structs. I would like to fix this, so make PR or issue if you know what to do.
2. The core function operates on recursion, so you could overflow your stack if you have outrageous nesting depth in the json to parse.