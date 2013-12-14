[ -d ./virtualenv ] || (
  virtualenv --distribute ./virtualenv && \
  source ./virtualenv/bin/activate && \
  pip install -r requirements.txt
)

source ./virtualenv/bin/activate

npm install
export PATH=$PWD/node_modules/.bin:$PATH
