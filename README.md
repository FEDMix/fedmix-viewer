# fedmix-viewer
Frontend and Backend code to run the application with docker-compose

## Local Installation
```
$ git clone https://github.com/FEDMix/fedmix-viewer.git
$ cd fedmix-viewer
$ make install
```

Make a data dir and copy the data_artificial into it
```
$ cd fedmix-viewer/backend
$ mkdir data
$ cd data
$ cp -r YOUR_DATA .
```
Take the manifest.json from the FedMix sharepoint and replace the manifest in the data dir with that

## Run
```
$ make serve
```

# Contributing

If you want to contribute to the development of fedmix-backend,
have a look at the [contribution guidelines](CONTRIBUTING.rst).

## Development Installation
Installing in development mode allows your changes to the backend to be immediately available
upon restarting the backend
```
$ git clone https://github.com/FEDMix/fedmix-viewer.git
$ cd fedmix-viewer
$ make install-dev
```

# License

Copyright (c) 2020, Netherlands eScience Center

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
