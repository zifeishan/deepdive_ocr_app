Safe copy ignoring errors
====

-- e.g.

COPY country FROM '/data/gpdb/country_data' 
 WITH DELIMITER '|' LOG ERRORS INTO err_country 
 SEGMENT REJECT LIMIT 100 ROWS;

-- Document:
--   http://media.gpadmin.me/wp-content/uploads/2012/11/GPDBAGuide.pdf
-- page 100

-- in gp, add:


LOG ERRORS INTO err_country 
SEGMENT REJECT LIMIT 10 ROWS;

-- Error table preserving:

CREATE TABLE err (cmdtime timestamp with time zone, relname text, filename text, linenum integer, bytenum integer, errmsg text, rawdata text, rawbytes bytea)


-- Result:

1-gram:

24183334 -> 24359392

2-gram:

~300,000,000 -> ? 563,297,697
                  556,969,069 (why? madmax4)
