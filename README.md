
# Foodstagram

Week 9 Project for MLH Production Engineering Fellowship!

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/varsharathore16"><img src="https://github.com/varsharathore16.png" width="100px;" alt=""/><br /><sub><b>Varsha Rathore</b></sub></a><br /><a href="#code-varsharathore16" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/cccswann"><img src="https://github.com/cccswann.png" width="100px;" alt=""/><br /><sub><b>Ciara (CiCi) Swann</b></sub></a><br /><a href="#design-cccswann" title="Design">🎨</a></td>
    <td align="center"><a href="https://github.com/stcwang"><img src="https://github.com/stcwang.png" width="100px;" alt=""/><br /><sub><b>Stephanie Wang</b></sub></a><br /><a href="#code-stcwang" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/Lanc33llis"><img src="https://github.com/Lanc33llis.png" width="100px;" alt=""/><br /><sub><b>Lance Ellis</b></sub></a><br /><a href="#content-Lanc33llis" title="Content">🖋</a></td>
  </tr>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
 


## Description

Foodstagram is a site where you can share your favorite food photos. After users create an account or log into previously existing ones, they are directed to the home page. Take a look at the most recently posted photos from all users on the home page, or view a specific user's posts on their profile page. 

There are login and register pages in addition to the basic html webpage to give users the accessibility to own accounts. Automation is another backbone of this project as there is CI/CD integration, monitoring, and deployment on AWS. The site will be responsive very soon.

Our site can be accessed at [foodstagram.tech](https://foodstagram.tech).


## Installation

Make sure you have python3 and pip installed.

cd into the backend. Create and activate virtual environment using virtualenv:

```bash
cd backend
python -m venv python3-virtualenv
source python3-virtualenv/bin/activate
```


Use the package manager pip to install all dependencies:

```bash
pip install -r requirements.txt
```


## Usage

Start flask development server:

```bash
export FLASK_ENV=development
flask run
```

or use vsc debugger by pressing `F5`.

