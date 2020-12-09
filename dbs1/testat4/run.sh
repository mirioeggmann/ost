#!/bin/bash
psql -U postgres -v ON_ERROR_STOP=on -f 0_runAllScripts.sql

