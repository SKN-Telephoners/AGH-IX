# AGH-IX

![Logo](https://raw.githubusercontent.com/ddominet/METIS-cluster/master/85414462_pazzddezd_logo.png)

Project AGH-IX goal is to create first in Poland automatic virtual internet exchange point. It will allow it's users to establish BGP peering with themselves directly or via Route-Server. Operations of this IX will be completely automatic, with little to no interference from NOC operator.

## Authors

- [@dobrowolski_dominik](https://github.com/ddominet)
- [@PiotrWodecki](https://github.com/PiotrWodecki)


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
 - [Django](https://github.com/django/django)
## License

[GPL3](https://www.gnu.org/licenses/gpl-3.0.txt)


## Tech Stack

**Server:** Python, Django

## Run Locally for the first time

Clone the project

```bash
  git clone https://github.com/SKN-Telephoners/AGH-IX.git
```

Go to the project directory

```bash
  cd AGH-IX
```

Init DB, stop the container with `ctrl+c` when the initialization ends
```bash
docker compose run db
```

Migrate DB schema
```
docker compose run web python manage.py migrate
```

(Optional) Create superuser
```bash
docker compose run web python manage.py createsuperuser
```

Start the virtual exchange point
```bash  
  docker compose up
```

## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)



## Task 1 (group of 3 people)
- **REQUIREMENTS** to run: docker, docker-compose
- Create AGH-IX Server instance, use command in **Run Localy** section and configure it to run properly
- Have two of your teammates establish connection with IX and test connection between them via ping
- send screenshot of the working ping between devices

## Task 2
- Due to security concerns you want to add additional capabilities to IX you want to establish blacklist for devices in our IXP
- Create a place in webgui where you can add devices to blacklist. It should be accessible **only by superuser**
- How you do this is up to you. Only front-end implementation is required
- send screenshot of your blacklist form
- send screenshot of the superuser check in your code

## Task 3
- With newly created web gui feature you want to create logic behind this blacklist. The blacklist should be saved to the DB
- Implement logic - prevent adding hosts that are present on the blacklist **and** deauthorize existing hosts
- see **/core/zerotier.py** for deauthorization
- remember to migrate your db with `docker compose run web python manage.py makemigrations` and `docker compose run web python manage.py migrate` after adding new fields in models.py
- send screnshots of your code
