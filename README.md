<h1 align="center">

Welcome to DRF Images Api 👋

</h1>
<p>
<img alt="Version" src="https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000" />
<a href="https://github.com/patpio/drf_images_api/blob/master/readme.md" target="_blank"><img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" /></a>
<a href="https://github.com/patpio/drf_images_api/graphs/commit-activity" target="_blank"><img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" /></a>
<a href="https://github.com/patpio/drf_images_api/blob/master/LICENSE" target="_blank"><img alt="License:Beerware" src="https://img.shields.io/badge/License-Beerware-yellow.svg" /></a>

</p>

> REST API for storing and resizing images.
### 🏠 [Homepage](https://github.com/patpio/drf_images_api/blob/master/readme.md)
### ✨ [Demo](https://drf-images-api.herokuapp.com)
## Install
```sh
Requirements:
- Docker
- Docker-Compose
- Python 3.9

Make sure you have Docker and Docker-Compose installed on your device.
Rename and refill envs files (.env.db.dev-default => .env.db.dev and .env.dev-default => .env.dev).

For development app run command in your terminal:
docker-compose -f docker-compose.dev.yaml up --build

```

## Usage
```sh
API requires authentication, except for the expiring links.

You can log in as admin:
Admin panel: 'http://0.0.0.0:8000/admin/'

Swagger: 'http://0.0.0.0:8000/swagger/'
Redoc: 'http://0.0.0.0:8000/redoc/'

You can add fake initial data to your database:
docker-compose -f docker-compose.dev.yaml exec backend python manage.py runscript users_factory
docker-compose -f docker-compose.dev.yaml exec backend python manage.py runscript imagers_factory

Image list and create: 'http://0.0.0.0:8000/api/v1/images'
Thumbnails create: 'http://0.0.0.0:8000/api/v1/thumbnails'
Thumbnails list for given image: 'http://0.0.0.0:8000/api/v1/thumbnails/<image_id>'
Expiring link create: 'http://0.0.0.0:8000/api/v1/link'

Performance:
- Easy horizontal scaling using container orchestration (f.e. Kubernetes)
- We use Redis for caching
- We create thumbnails on demand

```

![coverage](./coverage_report.png "coverage")

## Run tests
```sh
docker-compose -f docker-compose.dev.yaml exec backend pytest

```

## Author
👤 **Patrick Piotrowski**

* GitHub: https://github.com/patpio
* LinkedIn: https://www.linkedin.com/in/patrick-piotrowski-359437209
* CodeWars: https://www.codewars.com/users/pat_pi




## Show your support
Give a ⭐️ if this project helped you!
## Credits
**[Markdown Readme Generator](https://github.com/pedroermarinho/markdown-readme-generator)**
## 📝 License

Copyright © 2021 [Patrick Piotrowski](https://github.com/patpio ).<br/>
This project is [Beerware](https://github.com/patpio/drf_images_api/blob/master/LICENSE) licensed.

---
_This README was created with the [markdown-readme-generator](https://github.com/pedroermarinho/markdown-readme-generator)_