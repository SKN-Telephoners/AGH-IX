# AGH-IX

![Logo](https://raw.githubusercontent.com/ddominet/METIS-cluster/master/85414462_pazzddezd_logo.png)

Project AGH-IX goal is to create first in Poland automatic virtual internet exchange point. It will allow it's users to establish BGP peering with themselves directly or via Route-Server. Operations of this IX will be completely automatic, with little to no interference from NOC operator.

## Authors

- [@dobrowolski_dominik](https://github.com/ddominet)
- [@PiotrWodecki](https://github.com/PiotrWodecki)

## Run locally for the first time

1. Clone the project

```bash
  git clone https://github.com/SKN-Telephoners/AGH-IX.git
```

1. Go to the project directory

```bash
  cd AGH-IX
```

1. Create a token in `zerotier.token` file

Init DB, stop the container with `ctrl+c` when the initialization ends
```bash
docker compose run db
```

1. Migrate DB schema
```
docker compose run web python manage.py migrate
```

1. (Optional) Create superuser
```bash
docker compose run web python manage.py createsuperuser
```

1. Start the virtual exchange point
```bash  
  docker compose up
```

## Run locally
```bash
docker compose up
```

## Roadmap

- Testing arouteserver, checking it with bird and figuring out whether it can be easily implemented as a backend to check if asns, ip addresses are correct (RPKI, ROA), and if configuration is easily generated - [✅done]

- Creating backend with the ability to create and check status of vpn sessions zerotier API, Status of both BGP sessions and VPN sessions (bridged together) to be accessible from the frontend - [✅done]
- Frontend Django - [✅done]
- Nice clean website, integrated with a db with the ability to register and login for the IX users. The ability to enter resources ASN, IPs, ability to select session type IPv4, IPV6, IPv4+IPV6. ability to select VPN type (zerotier, gretap, vxlan) If everything checks out, establish and show parameters necessary to establish session, tunnel for the client side.- [✅done]

- Django Admin Panel - [✅done]

- Dockerize App as a set of microservices started with docker-compose - [✅done]

- LookingGlass? - [❌tbd]

- Checking if members adhere to security rules. Netflow? PacketCapture? Detecting port scans? - [❌tbd]

- Notify users by mail if their session is down, if they violate rules - [❌tbd]

## Contributing

Contributions are always welcome!

## Support

For support, email dobrowolski.domino@gmail.com or Piotr.M.Wodecki@gmail.com.

Contact us to get started.

Please adhere to this project's `code of conduct`.

## Acknowledgements

 - [arouteserver](https://github.com/pierky/arouteserver)
 - [ZeroUI](https://github.com/dec0dOS/zero-ui)

## License

[GPL3](https://www.gnu.org/licenses/gpl-3.0.txt)

## Screenshots

![image](https://user-images.githubusercontent.com/44680063/169712695-70326768-c74d-48f6-81e2-3ac5cbe06bba.png)
