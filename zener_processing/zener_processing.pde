import oscP5.*;
import netP5.*;
String thirdValue; 
OscP5 oscP5;
NetAddress myRemoteLocation;
PFont f;
PImage circle, cross, square, star, wave;

void setup() {
  size(800, 800);
  frameRate(25);
  oscP5 = new OscP5(this,12000);
  myRemoteLocation = new NetAddress("127.0.0.1",12000);
  f = createFont("ubuntu.ttf", 48);
  textFont(f);
  
  circle = loadImage("circle.png");
  cross = loadImage("cross.png");
  square = loadImage("square.png");
  star = loadImage("star.png");
  wave = loadImage("wave.png");
}

void draw(){
  background(255); 
  textAlign(CENTER);
  textSize(80);
  imageMode(CENTER);
  if(thirdValue != null){
    if(thirdValue.equals("circle")){
      image(circle, 400, 400, 200, 200);
    }
    else if(thirdValue.equals("crosses")){
      image(cross, 400, 400, 200, 200);
    }
    else if(thirdValue.equals("squares")){
      image(square, 400, 400, 200, 200);
    }
    else if(thirdValue.equals("stars")){
      image(star, 400, 400, 200, 200);
    }
    else if(thirdValue.equals("waves")){
      image(wave, 400, 400, 200, 200);
    }
  }
}

void oscEvent(OscMessage theOscMessage) {  
  if(theOscMessage.checkAddrPattern("/filter")==true) {
    thirdValue = theOscMessage.get(0).stringValue();
    println(" values:"+ thirdValue);
    return;
  } 
  println("### received an osc message. with address pattern "+theOscMessage.addrPattern());
}