# Berlin AI Python

### Getting Started

1. Install python with pip

  ```
    sudo apt-get install python python-dev python-pip
  ```

2. Install virtualenv (optional but recommended)

  ```
  sudo pip install virtualenv
  ```

3. Activate virtualenv
  
  ```
  virtualenv venv
  source venv/bin/activate
  ```

4. Install dependencies

  ```
  [sudo] pip install -r requirements.txt
  ```

### Start Application locally

This command will start your AI locally on port 5000

```
python main.py
```

### Run tests

This command will fake requests to your AI on port 5000. Make sure it is running first.

```
./run_tests.sh
```