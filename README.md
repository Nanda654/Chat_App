# Chat_App
chatapp to connect to people with similar interests using Django channels

## Tech Stach: Python,Django

## Getting Started


1. Clone the Chat_App into local device.
```bash
mkdir ~/Dev
cd ~/Dev
git clone https://github.com/Nanda654/Chat_App.git
cd Chatapp
```

2. Open VSCode
```bash
code .
```
3. Enter the Chat_app and activate the virtual environment .

```bash
cd chat_Apppython3.9 -m venv .
django_env\scripts\activate
```
Use `.\venv\Scripts\activate` if on **Windows.**

4. Enter chatapp and activate the server
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
