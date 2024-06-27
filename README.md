# UIRP-Rivian-R1-Hackathon

<div id="header" align="center">
<h3>
  Hello, this is the Enterprise Hackathon Project for team Rivian R1!
  <img src="https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif" width="30px"/>
</h3>

  <img src="https://media3.giphy.com/media/qY0xYZYRTl0mpS8vbm/giphy.gif" width="100px"/>

---

</div>
Data Acquisition in Rivian Hill Climb

Leveraging Open-Elevations Data for Terrain Accuracy

In our game Rivian Hill Climb, we are leveraging Open-Elevations data to accurately represent the altitude of different points along user-defined paths. This approach enhances the realism of the game and educates players about the unique challenges and strategies involved in driving electric vehicles (EVs) across varying terrains. Understanding how uphill and downhill segments affect battery usage and regeneration is critical for efficient energy management in EVs.

The detailed elevation data allows us to simulate the effect of terrain on the vehicle’s battery life and performance. Players experience how different elevations impact the car’s energy consumption and learn to use features like regenerative braking effectively. This is crucial in promoting the environmental benefits of EVs, demonstrating practical ways to extend battery life and reduce emissions.

Key Feature: Regenerative Braking

	•	Regenerative braking converts the kinetic energy lost during braking into electrical energy, which is then stored in the battery. This process helps to recharge the battery while driving downhill, enhancing the vehicle’s range and efficiency by utilizing energy that would otherwise be wasted.

By integrating Open-Elevations data into our game, we provide an engaging and educational experience that informs players about the advantages and sustainable practices associated with electric vehicle usage. This supports our goal of encouraging environmentally conscious driving habits.

Utilizing EPA Data for CO2 Emissions Analysis

We utilize emissions data from the U.S. Environmental Protection Agency to accurately depict the environmental impact of conventional vehicles (CVs) versus electric vehicles (EVs). Players input details about their current gasoline or diesel vehicle, and the game calculates and displays the CO2 emissions that would be generated on their chosen journey. This data is then contrasted with the significantly lower emissions from driving a Rivian EV on the same route.

This direct comparison serves as a powerful educational tool, visually and quantitatively demonstrating the substantial reduction in CO2 emissions achievable by opting for an EV. Players can see the exact kilograms of CO2 they would save in real-time, making the environmental benefits of EVs tangible and immediate.

By incorporating this data-driven approach, we enlighten players about the positive environmental impact of switching to electric vehicles. This not only enhances their gaming experience but also fosters a deeper understanding of the crucial role EVs play in reducing automotive emissions and combating climate change. We provide a compelling case for the adoption of greener transportation alternatives through this interactive platform.

This Markdown formatting introduces headers, bullet points, and bold text to improve clarity and organization, making the README file easy to navigate and understand.

---

## Prerequisities
To run this game, you need to have Python and Pygame installed on your machine. The other dependencies are listed in dependencies.txt. We recommend you create a python virtual environment (using `conda` or `venv`) for installing packages and playing our game. 

---

## Setting Up Our Game
```bash
# clone the repo
git clone https://github.com/MeanPaper/UIRP-Rivian-R1-Hackathon.git

# go to the project directory
cd UIRP-Rivian-R1-Hackathon

# install dependencies
pip install -r dependencies.txt
```
---

## Running Our Game
```bash
cd src
python game.py
```

---

## Challenges and Innovations
### Real-time Terrain Generation
One of the biggest challenges in developing this game was integrating real-time geographic data to generate the terrain. The game fetches elevation data based on the player's location or specified start and destination points, making each game session unique and geographically accurate.

### Synchronizing Terrain with Car Physics
Ensuring that the terrain works seamlessly with the car's rotation, gravity, and deceleration was particularly challenging. The car needs to interact with the dynamically generated terrain in a realistic manner, which required precise calculations and fine-tuning of the physics engine.

### Leveraging Real-world Data
The game leverages various kinds of real-world data, such as elevation maps, to create a more immersive experience. This involved gathering data from reliable sources over the internet and processing it in real-time, adding a layer of complexity to the game's development.

### Emission saved message 
In the beginning where you put input details about which car you currently own, it extracts the data from the dataset to calculate the total CO2 emission your car would have had if you had travelled with your car rather than using a RIVIAN and dislays the message to the player to make them aware of the impact they are having on the environment. 

### Dynamic Backgrounds
In addition to the terrain, the background changes based on the location data, adding to the realism and providing a unique visual experience for different geographical regions.

---

## Game Controls

### Text Input Controls
Car Type Inputs: 
 'Aston Martin DB11 2017',
 'Aston Martin Rapide S 2017',
 'Aston Martin V12 Vantage S 2017',
 'Aston Martin Vanquish 2017',
 'AUDI A4 2017',
 'AUDI Q5 2017',
 'AUDI RS7 2017',
 'AUDI S5 2017',
 'BENTLEY Continental GT 2017',
 'BMW 230i Convertible 2017',
 'BMW 230i Coupe 2017',
 'BMW 230i xDrive Convertible 2017',
 'BMW 230i xDrive Coupe 2017',
 'BMW 320i 2017',
 'BMW 320i xDrive 2017',
 'BMW 328d 2017',
 'BMW 328d xDrive 2017',
 'BMW 328d xDrive Sports Wagon 2017',
 'BMW 330e 2017',
 'BMW 330i 2017',
 'BMW 330i xDrive 2017',
 'BMW 330i xDrive Gran Turismo 2017',
 'BMW 330i xDrive Sports Wagon 2017',
 'BMW 340i 2017',
 'BMW 340i xDrive 2017',
 'BMW 340i xDrive Gran Turismo 2017',
 'BMW 430i Convertible 2017',
 'BMW 430i Coupe 2017',
 'CHEVROLET COLORADO ZR2 4WD 2018',
 'CHEVROLET CORVETTE 2018',
 'CHEVROLET CRUZE 2018',
 'CHEVROLET EQUINOX 2018',
 'CHEVROLET EQUINOX AWD 2018',
 'CHEVROLET EQUINOX FWD 2018',
 'CHEVROLET IMPALA 2018',
 'CHEVROLET K15 SILVERADO 4WD 2018',
 'CHEVROLET K1500 SUBURBAN 4WD 2018'
 
 & many more

### Start-End Location Sample Inputs:

(Chicago, champaign), (Chicago, Urbana), (Snoquera, Tacoma), (Seattle, Portland)
(any two cities/states/countries with a car traversable path, any coordinates, any pin codes)

### Hill Climb Controls
Press the right arrow key or the 'D' key to move forward.

Press the left arrow or the 'A' key to brake forcefully for regenerating battery while you can.

---

## Link
Here is the link to our video demo:


<a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUabmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA%3D">
    <img src="https://pngfre.com/wp-content/uploads/You-Tube-14.png" alt="YouTube Link" width="70"/>
