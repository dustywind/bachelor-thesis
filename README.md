
# bachelor-thesis
bachelor-thesis

# Description
This project aims to create an recommendation engine based on the [Rocchio algorithm](https://en.wikipedia.org/wiki/Rocchio_algorithm).

In order to do so, we have to build a database of stuff (like products), create vectors that represent the stuff and build another vector that resembles a potential customer.

# Install
1. To install the project simply clone this repo (git clone https://dustywind/bachelor-thesis)
2. cd bachelor-thesis/impl
3. sudo bash ./deploy.sh

Following programms are required:
- python3 (it _MUST_ be python 3.4 or higher)
- bottlepy (for python3)
- nodejs

# Execution
To run the web-server one has to start two programs
- execute bachelor-thesis/impl/run.sh
- run "npm start" in bachelor-thesis/impl/onlineshop/

# Used technologies
A short list of thechnologies used in this project:

## General
- [git (obviously)](https://git-scm.com)

## docs
- Makefile
- LaTeX
- [dia](https://wiki.gnome.org/Apps/Dia/)
- [Inkscape](https://inkscape.org/en/)

## impl

### Recommender library
- [python 3](https://python.org)
- [sqlite](https://sqlite.org)
- [bottle](http://bottlepy.org/docs/dev/index.html)
- [Sphinx](http://sphinx-doc.org)

### Online shop
- [node.js](https://nodejs.org)
- [express](http://expressjs.com)
- [jade](http://jade-lang.com)
- [jQuery](https://jquery.com)

