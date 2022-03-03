# openstack_admin
Openstack Administrator, You can reset status instance when there are some error on instance or hang process


# api Address

#### address api
```
http://{{ip}}:8586/v1/server/reset_status
http://{{ip}}:8586/v1/server/reset_states_active

{

"server":{
"instance_id":"bb79ac6f-9a49-4543-a326-9853e8320d59"

}

}

```

# API's
```
# When Mysql DOWN
http://IP:8586/v1/server/{REGION}_up?key={REGION}_1&status=down
# When Mysql UP
http://IP:8586/v1/server/{REGION}_up?key={REGION}_1&status=up
```

# Monitoring LifeCycle
![test drawio](https://user-images.githubusercontent.com/90821955/150669768-8d26baf5-ced5-472f-946f-0e42720cc35a.png)
