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
