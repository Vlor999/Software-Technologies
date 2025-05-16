# Commands

## Website :
The website for all main informations :
<pre>
```bash
open https://graphwalker.github.io/
# or : 
firefox https://graphwalker.github.io/
```
</pre>

## Download the jar files : 
For the `CLI` file :
<pre>
```bash
curl -L -O https://github.com/GraphWalker/graphwalker-project/releases/download/4.3.3/graphwalker-cli-4.3.3.jar
# or
wget https://github.com/GraphWalker/graphwalker-project/releases/download/4.3.3/graphwalker-cli-4.3.3.jar
```
</pre>

For the `Studio` version :
<pre>
```bash
curl -L -O https://github.com/GraphWalker/graphwalker-project/releases/download/4.3.3/graphwalker-studio-4.3.3.jar
# or 
wget https://github.com/GraphWalker/graphwalker-project/releases/download/4.3.3/graphwalker-studio-4.3.3.jar
```
</pre>

### Installation wget : 
<pre>
```bash
# MacOs : 
brew install wget

# Linux : 
sudo apt-get install wget # sudo may not be necessary
```
</pre>

## To launch to visualizer : 
<pre>
```bash
java -jar graphwalker-studio-4.3.3.jar
```
</pre>
Then you'll have infirmations about wich local server is available to launch the application into your browser.
<pre>
```bash
# Exemple : 
open http://127.0.0.1:9090 
# Or : 
firefox http://127.0.0.1:9090 
```
</pre>

## To validate a model :

<pre>
```bash
java -jar GraphWalker-4.3.3.jar validate --path your_model.graphml
```
</pre>

## Genration of path : 

<pre>
```bash
java -jar GraphWalker-4.3.3.jar generate --path your_model.graphml "random(edge_coverage(100))"
```
</pre>

