python -m pip install --upgrade pip
pip install -e .[test]
npm install -g @mermaid-js/mermaid-cli
playwright install --with-deps

# pytest tests/ --doctest-modules --cov=./metagpt/ --cov-report=xml:cov.xml --cov-report=html:htmlcov --durations=20
  #coverage report -m