# Surface table — TASK-260929-1w99it tools-exact-integer-argument-adapter

| Row | Invariant | Attack families |
|---|---|---|
| text grammar | Accept only integral JSON numeric lexemes that fit the destination type; accepted values equal the exact integer; everything else is refused with a serde-shaped error | numeric-looking scalars (fractions, rounded fractions 1.0000000000000001 / 9007199254740991.5, -0.0, exponents 6e4 / 6.0e4 / 1e20, huge integers beyond 2^53 and beyond u64::MAX); strings, booleans, null for non-Option fields; negative values into unsigned targets; size limits (1e999999999, 1e-999999999, very long digit strings) without unbounded allocation or time; duplicate keys in the containing struct |

```surface-table
{"rows": ["text grammar"]}
```
