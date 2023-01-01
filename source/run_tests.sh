docker rm api
docker rm tests
docker rmi source_api
docker rmi source_tests
docker compose --profile test up --abort-on-container-exit --exit-code-from tests
