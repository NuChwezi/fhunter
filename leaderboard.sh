#!/usr/bin/sh
ssh pharaoh "psql fhunter postgres -c 'select ip ,score from fhunter_hits where score > 0 order by score desc limit 10'"
