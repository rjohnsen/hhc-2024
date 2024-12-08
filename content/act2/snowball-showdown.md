+++
title = 'Snowball Showdown'
date = 2024-11-23T13:18:46+01:00
draft = false
weight = 4
+++

## Objective 

> Wombley has recruited many elves to his side for the great snowball fight we are about to wage. Please help us defeat him by hitting him with more snowballs than he does to us.

## Solution

### Bronze

Once loading the game, we get presented with a loading screen detailing how to play the game: 

![Loading screen](/images/act2/act2-snowball-showdown-1.png)

And this is the general game area: 

![Game area](/images/act2/act2-snowball-showdown-2.png)

By inspecting the GET parameter in URL, I found this: 

```html
&singlePlayer=false
````

Setting it to true and reload the game:

```html
&singlePlayer=true
````

{{% notice note %}}
I will be using this "singlePlayer" hack throughout the game
{{% /notice %}}

Then I inspected ```https://hhc24-snowballshowdown.holidayhackchallenge.com/js/phaser-snowball-game.js``` and found some interesting references:

```javascript
...
create() {
    this.setupWebSocket();
    mainScene = this;
    if (this.isFirefox) {
        console.error("Firefox detected, please use Chrome or Safari for best experience!");
        this.add.text(5, GAME_HEIGHT - 5, "  Runs best in\nChrome or Safari!", { fontSize: '25px', fill: '#fff', fontFamily: 'monospace', stroke: '#000000', strokeThickness: 8 }).setOrigin(0, 1).setDepth(10);
    }
    this.snowBallBlastRadius = 24;
    this.onlyMoveHorizontally = true;
    this.projectiles = this.physics.add.group();
    this.elves = [];
    this.setupBackgroundImages();
    this.setResetDestructibleScenery();
...
```

Apparently the ```elves``` is an array holding a list of elves. Perhaps I can make life easier by disabling the elves? There's a reference to variable ```mainScene```, which seems to contain the game. Poking around inspecting the values of it, I found a reference to _Alabaster_ and the scale of him. My main goal was then to set his scale to something small in hope he wouldn't get hit as hard: 

```javascript
mainScene.elves = []
mainScene.alabaster._scaleX = 0.1
mainScene.alabaster._scaleY = 0.1
````

![Bronze winning screen](/images/act2/act2-snowball-showdown-3.png)

Apparantly this was not the correct solution, only earning me a bronze completion status

### Silver

Circling back to this code I wanted to try to manipulate the ```snowBallBlastRadius``` variable, and possibly find something else that could help me out as well:

```javascript
...
create() {
    this.setupWebSocket();
    mainScene = this;
    if (this.isFirefox) {
        console.error("Firefox detected, please use Chrome or Safari for best experience!");
        this.add.text(5, GAME_HEIGHT - 5, "  Runs best in\nChrome or Safari!", { fontSize: '25px', fill: '#fff', fontFamily: 'monospace', stroke: '#000000', strokeThickness: 8 }).setOrigin(0, 1).setDepth(10);
    }
    this.snowBallBlastRadius = 24;
    this.onlyMoveHorizontally = true;
    this.projectiles = this.physics.add.group();
    this.elves = [];
    this.setupBackgroundImages();
    this.setResetDestructibleScenery();
...
```

Looking further into the same Javascript where I found the code above, I found a reference to ``throwRateOfFire````:

```javascript
class SnowBallGame extends Phaser.Scene {
    constructor() {
        super({ key: "game" });
        this.hasBgDebug = typeof window.bgDebug !== 'undefined'
        this.groundOffset = groundOffset;
        this.yellowTint = 0xffeb99;
        this.blueTint = 0x99ddff;
        this.snowballLiveTime = 12000;
        this.healingTerrain = true;
        this.terrainHealDelay = 15000;
        this.elfGroundOffset = GAME_HEIGHT - 115;
        this.wombleyXLocation = GAME_WIDTH - 40;
        this.alabasterXLocation = 40;
        this.playerMoveSpeed = 150;
        this.lastTimePlayerArrowsFromUpdate = 0
        this.lastTimePlayerArrowsFromUpdateDelay = 20
        this.percentageShotPower = 0;
        this.alabasterElvesThrowDelayMin = 1500;
        this.alabasterElvesThrowDelayMax = 2500;
        this.wombleyElvesThrowDelayMin = 1500;
        this.wombleyElvesThrowDelayMax = 2500;
        this.wombleyElvesIncompacitateTime = 5000;
        this.alabasterElvesIncompacitateTime = 5000;
        this.playerIncompacitateTime = 5000;
        this.throwSpeed = 1000;
        this.throwRateOfFire = 1000;
```

In Console in Edge, I set the following (I tend to set matching values it appears):

```javascript
mainScene.throwRateOfFire = 1000
mainScene.snowBallBlastRadius = 1000
```

This resultet in quite a rapid firerate and a greater blastradius making it easier to defeat Wombly. Just had to blow the dividing iceberg to smitherines once and awhile until victory:

![Bronze silver screen](/images/act2/act2-snowball-showdown-4.png)

### Gold

During the conversation with Dusty Giftwrap he mentions a secret weapon - a bomb:

> Hi there! I'm Dusty Giftwrap, back from the battlefield! I'm mostly here for the snowball fights!
> 
> But I also don't want Santa angry at us, you wouldn't like him when he's angry. His face becomes as red as his hat! So I guess I'm rooting for Alabaster.
> 
> Alabaster Snowball seems to be having quite a pickle with Wombley Cube. We need your wizardry.
> 
> Take down Wombley the usual way with a friend, or try a different strategy by tweaking client-side values for an extra edge.
> 
> Alternatively, we've got a secret weapon - a giant snow bomb - but we can't remember where we put it or how to launch it.
> 
> Adjust the right elements and victory for Alabaster can be secured with more subtlety. Intriguing, right?
> 
> Raring to go? Terrific! Here's a real brain tickler. Navigator of chaos or maestro of subtlety, which will you be? Either way, remember our objective: bring victory to Alabaster.
> 
>Confidence! Wit! We've got what it takes. Team up with a friend or find a way to go solo - no matter how, let's end this conflict and take down Wombley!

Kinda bored with reading Javascript, I decided to download the ```https://hhc24-snowballshowdown.holidayhackchallenge.com/js/phaser-snowball-game.js``` file, then uploading it to ChatGPT asking by this prompt: 

> Is there anything in this piece of code that could refer to a bomb? 

Sure enough, ChatGPT suggested the following (amongst a bunch of others):

> "MOASB" Functionality:
>
> There is a function (this.moasb) related to sending a message with the type "moasb", which might refer to an in-game mechanic potentially tied to "Mother of All > Snowballs," a playful analogy to a powerful bomb.

Okay. Looking further into the Javascript file, I find this web socket call: 

```javascript
this.moasb = () => { this.ws.sendMessage({ type: 'moasb' }) }
```

I decided to rewrite it and send it off using the Console in Edge: 

```javascript
mainScene.ws.sendMessage({"type":"moasb"});
```

And then an ironbird appeared:

![MOASB incoming](/images/act2/act2-snowball-showdown-5.png)

Success!

![Gold winning screen](/images/act2/act2-snowball-showdown-6.png)