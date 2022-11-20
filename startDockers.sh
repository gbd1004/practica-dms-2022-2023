#! /bin/bash
if [ -z "$(docker images dms*)" ]

then
	docker-compose -f docker/config/dev.yml build
fi

docker-compose -f docker/config/dev.yml up -d