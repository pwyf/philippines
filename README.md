Philippines projects browser
============================

Small Flask / Frozen-Flask app to show projects in the Philippines.

AGPL v3.0 Licensed

License: AGPL v3.0
==================

Copyright (C) 2013 Mark Brough, Publish What You Fund

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Install instructions

1. Clone the repository:

        git clone git@github.com:markbrough/philippines.git

2. Change into the directory and create a `virtualenv`:

        cd philippines
        virtualenv ./pyenv
        source ./pyenv/bin/activate

3. Install requirements:

        pip install -r requirements.txt

4. Run the server to check you're happy with everything:

        python philippines.py

5. Once you're happy, build the static site:

        python philippines.py build
