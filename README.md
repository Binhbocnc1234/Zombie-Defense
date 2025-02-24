
Welcome to Zombie Defense  
game made by team 2 in club MKDC  

Demo link: https://youtu.be/6Fjceax26ug. Have fun playing :D  

**Player:**  
    *Fire rate:
-Unit: Pixel per frame. For example: "arrow speed equal to 14" means that arrow can travel 14 pixel after one frame  
Limit arrow speed: min 7, max 14    
Initialy, arrow speed is zero! When the player is charging, the arrow speed will be stacked 0.13 per frame  
That means the player needs 14 / 0.13 = 107 frames for the bow to be fully charged
Gravity is an acceleration vector(0.2 pixel per frame) affects on the motion of arrow  
    *Damage:  Formula: 40 + Arrow speed*(100/23)  
    *Health:  default is 15. Some levels is different    
	**Enemies**  
|Unit      	| Health| Speed |          Special abilities	        |
|-----------|------ |-------|-----------------------------------	|
|Zombie	   	|170	|	|				        |
|Bucket Zombie	|700	|	|				        |
|Bat	   	|400	|	|Flying, sometimes it holds other enemy |
|Werewolf  	|400	|	|					|
|Destroyer   	|1200	|	|Explode and spawn enemies when he died, Number of enemies: [1, 3], Destroyer can spawn itself!! with lower chance	|

**Upgrades:**  
Damage up: +18% damage per upgrade. Max 8  
Fire rate up: +16% fire rate and +0.8 arrow speed per upgrade(Extra arrow's speed dont affect arrow's damage). Max 5  
Shadow arrow: Help player shoot multiple arrows. The total damage of shadow arrows increases by 21% after each upgrade  
