<h3>WebSocket based online dice game, inspired by The Witcher's dice game.</h3>
Client written in React.
API written in FastAPI with SQLAlchemy ORM.

How to run locally:

1. Clone the project:
<pre>$ git clone https://github.com/Ansup17174/witcher-dice-game.git</pre>
<pre>$ cd witcher-dice-game</pre>


2. Configuration:
  - set properites in api/.env
  - set properties in client/.env

3. Install client dependencies:
<pre>$ cd client</pre>
<pre>$ npm install</pre>
<pre>$ cd ..</pre>

4. Install api dependencies:
<pre>$ cd api</pre>
Create virtual env
<pre>$ python -m venv env</pre>
Activate venv
On windows:
<pre>\> ./env/Scripts/activate.bat</pre>
On Linux/MacOS:
<pre>$ source env/Scripts/activate</pre>
Install dependencies:
<pre>$ python -m pip install -r requirements.txt</pre>
<pre>$ cd ..</pre>

5. Run api:
<pre>$ uvicorn api.main:app --env-file api/.env</pre>

6: Run client:
<pre>$ cd client</pre>
<pre>$ npm start</pre>
