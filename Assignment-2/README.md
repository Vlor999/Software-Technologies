# GraphWalker User Guide

GraphWalker is a tool for model-based testing that allows you to create, validate, and generate test paths from graphical models.

## Installation

### Download GraphWalker

Download the required JAR files:

**GraphWalker CLI**:
```bash
# Using curl
curl -L -O https://github.com/GraphWalker/graphwalker-project/releases/download/4.3.3/graphwalker-cli-4.3.3.jar

# Using wget
wget https://github.com/GraphWalker/graphwalker-project/releases/download/4.3.3/graphwalker-cli-4.3.3.jar
```

**GraphWalker Studio**:
```bash
# Using curl
curl -L -O https://github.com/GraphWalker/graphwalker-project/releases/download/4.3.3/graphwalker-studio-4.3.3.jar

# Using wget
wget https://github.com/GraphWalker/graphwalker-project/releases/download/4.3.3/graphwalker-studio-4.3.3.jar
```

If you don't have wget installed:
```bash
# MacOS
brew install wget

# Linux
apt-get install wget
```

## Using GraphWalker Studio

### Launch GraphWalker Studio

Before launching take care that the `java` version that you are using is `java` **11**. To do so :
```bash
java --version
``` 
if it return : `java 11.X.Y` then everything is good. Otherwise you have to download it : 
```bash
brew install openjdk@11 # For macOS
## You may need for macOS to use this command to link it : 
sudo ln -sfn /opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-11.jdk
# or
sudo apt install openjdk-11-jdk # For Linux
```
To be sure everything works properly you can verify that all the versions are here with  : 
```bash 
/usr/libexec/java_home -V
```
Then you'll see something like : 
```bash
Matching Java Virtual Machines (2):
    23.0.1 (arm64) "Oracle Corporation" - "Java SE 23.0.1" /Library/Java/JavaVirtualMachines/jdk-23.0.1.jdk/Contents/Home
    11.0.27 (arm64) "Homebrew" - "OpenJDK 11.0.27" /opt/homebrew/Cellar/openjdk@11/11.0.27/libexec/openjdk.jdk/Contents/Home
/Library/Java/JavaVirtualMachines/jdk-23.0.1.jdk/Contents/Home
```

Then you have to temporarily activate the **11** verison of `java` : 
```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11) # macOS
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 # Linux
# Then for both : 
export PATH=$JAVA_HOME/bin:$PATH
```

Start the GraphWalker Studio server:
```bash
java -jar graphwalker-studio-4.3.3.jar
```

Open GraphWalker Studio in your web browser:
```bash
# The default URL is:
open http://localhost:9090/studio.html  # For macOS
# or
firefox http://localhost:9090/studio.html  # For Linux
```

### Creating a Model

1. **Create an empty model**:
   * Click the **+** button to open a new model editor view

2. **Create a vertex (node)**:
   * Press the `v` key on your keyboard
   * Click the left mouse button anywhere on the editor canvas

3. **Create an edge (connection)**:
   * Press the `e` key on your keyboard
   * Click and hold on the first vertex
   * Drag to the second vertex and release

4. **Set the start element**:
   * Open the side bar
   * Click on any element (vertex or edge)
   * Check the "Start element" checkbox

5. **Save your model**:
   * Click the Save button on the left sidebar

## Model Validation and Testing

### Validate a Model

To check if your model is valid:
```bash
java -jar graphwalker-cli-4.3.3.jar validate --path your_model.graphml
```

### Generate Test Paths

To generate test paths from your model:
```bash
java -jar graphwalker-cli-4.3.3.jar generate --path your_model.graphml "random(edge_coverage(100))"
```

## Additional Resources

Official GraphWalker website:
```bash
open https://graphwalker.github.io/
# or
firefox https://graphwalker.github.io/
```

The website contains comprehensive documentation, tutorials, and examples to help you make the most of GraphWalker.
