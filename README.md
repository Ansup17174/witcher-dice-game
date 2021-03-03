<h3>WebSocket based online dice game, inspired by The Witcher's dice game.</h3>

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
<pre>$ python -m pip install -r requirements.txt</pre>
<pre>$ cd ..</pre>

5. Run api:
<pre>$ uvicorn api.main:app --env-file api/.env</pre>

6: Run client:
<pre>$ cd client</pre>
<pre>$ npm start</pre>
