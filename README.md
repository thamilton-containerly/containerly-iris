# iris

Insert service description below.

## Payload

base64 encoded payload

```json
{
	"sepal_length_cm": 2,
	"sepal_width_cm": 4,
	"petal_length_cm": 4,
	"petal_width_cm": 2
}
```

## Commands

[Local] Send message with grpcurl
```shell
echo '{"message": "eyJzZXBhbF9sZW5ndGhfY20iOiAyLCAic2VwYWxfd2lkdGhfY20iOiA0LCAicGV0YWxfbGVuZ3RoX2NtIjogNCwgInBldGFsX3dpZHRoX2NtIjogMn0="}' | grpcurl -plaintext -d @ localhost:50051 containerly.Runtime/Service
```

[Dev] Build service
```shell
docker build -t iris .
```

[Dev] Run service server
```shell
docker run -p 50051:50051 iris serve
```

[Dev] Run service client
```shell
docker run iris client --host=localhost --port=50051 --payload='{"sepal_length_cm": 2,"sepal_width_cm": 4,"petal_length_cm": 4,"petal_width_cm": 2}'
```

[Prod] Build service
```shell
./script/build
```

[Prod] Push service
```shell
./script/push
```

[Prod] Deploy service
```shell
./script/deploy
```

[Prod] Send message with docker
```shell
docker run iris client --host=iris.containerly.io --port=443 --payload='{"sepal_length_cm": 2,"sepal_width_cm": 4,"petal_length_cm": 4,"petal_width_cm": 2}' --insecure=False
```

[Prod] Send message with grpcurl
```shell
echo '{"message": "eyJzZXBhbF9sZW5ndGhfY20iOiAyLCAic2VwYWxfd2lkdGhfY20iOiA0LCAicGV0YWxfbGVuZ3RoX2NtIjogNCwgInBldGFsX3dpZHRoX2NtIjogMn0="}' | grpcurl -d @ iris.containerly.io:443 containerly.Runtime/Service
```