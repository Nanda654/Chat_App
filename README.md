# Chat_App
chatapp to connect to people with similar interests using Django channels

## Tech Stach: Python,Django

## Getting Started


1. Clone the Chat_App into local device.
```bash
mkdir ~/Dev
cd ~/Dev
git clone https://github.com/Nanda654/Chat_App.git

```

2. Enter the Chat_app and activate the virtual environment .

```bash
python -m venv env
env\scripts\activate
```

3. Open VSCode or any code editor of convenience if needed.
```bash
code .
```

3. install all the requirments from requirements.txt in the chatapp directory
```bash
cd chatapp
pip install -r requirements.txt
```

4. Activate the server
```bash
cd chatapp
python manage.py runserver
```
## Then finally, signup and login to chat

### If you want to add any aditinal interests open djangoshell and add interest objects to the Intersts model.
```bash
python manage.py shell
>>> from chat.models import Interest 
>>> add_interest = Interest.objects.create(name = 'interest_name')
```
