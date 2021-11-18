#!/bin/bash
cd frontend && yarn run build
cd ../server && flask run