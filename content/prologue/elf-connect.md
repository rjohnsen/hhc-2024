+++
title = 'Elf Connect'
date = 2024-11-10T10:51:56+01:00
draft = false
weight = 2
+++

## Objective

> Help Angel Candysalt connect the dots in a game of connections.

## Hints

| From | Hint |
| ---- | ---- |
| Angel Candysalt | WOW! A high score of 50,000 points! That’s way beyond the limit! With only four rounds and a max of 400 points per round, the top possible score should be 1,600 points. So, how did someone get to 50,000? Something unusual must be happening! If you're curious, you might want to check under the hood. Try opening the browser's developer tools console and looking around—there might even be a variable named 'score' that could give you some insights. Sometimes, games hold secrets for those who dig a little deeper. Give it a shot and see what you can discover! |
| Angel Candysalt | I love brain games! This one is like the New York Times Connections game. Your goal here is to find groups of items that share something in common. Think of each group as having a hidden connection or theme—four items belong together, and there are multiple groups to find! See if you can spot patterns or common threads to make connections. Group all the items correctly to win! |

## Observations

| # | Observation | 
| --- | --- |
| 1 | Inspected network traffic, game is hosted at ```https://hhc24-elfconnect.holidayhackchallenge.com/``` |
| 2 | Playing game through Burpsuite we can get hold of the Javascript controlling the game | 
| 3 | In Javascript, variable "_wordSets_" holds the words |
| 4 | In Javascript, variable "_correctSets_" holds the correct words for each round |
| 5 | Round is controlled by ```https://hhc24-elfconnect.holidayhackchallenge.com/?round=2``` |
| 6 | It appears that "_correctSets_" isn't updated between rounds. Thus, the same positions pr. set is reused. |
| 7 | In Javascript, if we set variable "_score_" to a high number, it reflects in the GUI. |
| 8 | We need to set "_id_" in local storage to beat this game if we load the game in a new window or tab, as evident in code ```localStorage.getItem('id');``` |

## Solution

### Silver

Silver means playing the game using the following cheat sheet (I just pasted everything into ChatGPT and took whatever feedback I got).

#### Round 1

| **Category**                      | **Items**                                       |
|-----------------------------------|------------------------------------------------|
| **Reindeer Team**                 | Blitzen, Comet, Prancer, Vixen                 |
| **Christmas Decorations**         | Lights, Garland, Tinsel, Star                 |
| **Holiday Songs/Singers**         | Crosby, White Christmas, Jingle Bells, Belafonte |
| **Santa's Equipment**             | Sleigh, Bag, Mittens, Gifts                   |

#### Round 2

| **Category**                      | **Items**                                       |
|-----------------------------------|------------------------------------------------|
| **Network Analysis Tools**        | Nmap, Wireshark, netcat, Nessus               |
| **Mobile/Binary Analysis**        | Frida, apktool, Cycript, AppMon               |
| **Web Application Testing**       | burp, OWASP zap, Nikto, wfuzz                 |
| **Post-Exploitation/Red Team**    | Metasploit, Empire, Cobalt Strike, HAVOC      |

#### Round 3

| **Category**                      | **Items**                                       |
|-----------------------------------|------------------------------------------------|
| **Historical/Classical Ciphers**  | Caesar, Scytale, One-time Pad, Ottendorf      |
| **Modern Symmetric Algorithms**   | AES, Blowfish, 3DES, RSA                      |
| **Wireless Security Protocols**   | WPA2, WEP, TKIP, LEAP                         |
| **General Crypto Concepts**       | Symmetric, Asymmetric, hash, hybrid           |

#### Round 4
| **Category**                      | **Items**                                       |
|-----------------------------------|------------------------------------------------|
| **Layer 2 (Data Link) Protocols** | ARP, Ethernet, PPP, IEEE 802.11              |
| **Layer 3 (Network) Protocols**   | IP, ICMP, IGMP, IPX                           |
| **Secure Communication Protocols**| SSH, SSL, TLS, IPSec                          |
| **Application Layer Protocols**   | HTTP, FTP, SMTP, DNS                          |

### Gold

Based on the observation, this appears to be a straight and easy task to solve. Since we found the Javascript controlling the game, and observing what it does, we can create a short and sweet Javascript that simply loops through each sets in wordSets and maps it to the corresponding solution in correctSets. We also make sure to bump the topscore by simply setting it to a huge number to beat this game with gold.

```javascript
function mapWordsByCorrectSets(wordSets, correctSets) {
    let result = {};

    for (let setKey in wordSets) {
        result[setKey] = correctSets.map(indices => 
            indices.map(i => wordSets[setKey][i])
        );
    }

    return result;
}

score = 10000000000000;
console.log(mapWordsByCorrectSets(wordSets, correctSets));
```

#### Applying code

Selecting the right iframe we are going to work in:

![Selecting the correct iframe](/images/prologue/elf-connect-select-iframe.png)

Pasting and running the Javascript code:

![Pasting and running the Javascript code](/images/prologue/elf-connect-pasting-code.png)

Then it is just a matter of selecting the first word set from the GUI and you have beaten the game with a new high score! 

## Javascript controlling the game

This is the Javascript controlling the game and which I used to solve it.

```javascript
let urlParams = new URLSearchParams(window.location.search);
const roundCheck = urlParams.get('round');

if (!roundCheck) {  // If 'round' is absent or has no value
    sessionStorage.clear();
}

// Configuring the Phaser game
const config = {
    type: Phaser.AUTO,
    scale: { // sets the auto scaling of the canvas for all browsers
        mode: Phaser.Scale.FIT,
        parent: 'phaser-example',
        autoCenter: Phaser.Scale.CENTER_BOTH,
        width: 800,
        height: 600
    },
    backgroundColor: '#2fb3fe', // background border color
    scene: {
        preload: preload,
        create: create,
        update: update
    },
    physics: {
        default: 'arcade', //defines game as an arcade type
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    }
};

const game = new Phaser.Game(config);

const wordSets = {
    1: ["Tinsel", "Sleigh", "Belafonte", "Bag", "Comet", "Garland", "Jingle Bells", "Mittens", "Vixen", "Gifts", "Star", "Crosby", "White Christmas", "Prancer", "Lights", "Blitzen"],
    2: ["Nmap", "burp", "Frida", "OWASP Zap", "Metasploit", "netcat", "Cycript", "Nikto", "Cobalt Strike", "wfuzz", "Wireshark", "AppMon", "apktool", "HAVOC", "Nessus", "Empire"],
    3: ["AES", "WEP", "Symmetric", "WPA2", "Caesar", "RSA", "Asymmetric", "TKIP", "One-time Pad", "LEAP", "Blowfish", "hash", "hybrid", "Ottendorf", "3DES", "Scytale"],
    4: ["IGMP", "TLS", "Ethernet", "SSL", "HTTP", "IPX", "PPP", "IPSec", "FTP", "SSH", "IP", "IEEE 802.11", "ARP", "SMTP", "ICMP", "DNS"]
};

let wordBoxes = [];
let selectedBoxes = [];
let correctSets = [
    [0, 5, 10, 14], // Set 1
    [1, 3, 7, 9],   // Set 2
    [2, 6, 11, 12], // Set 3
    [4, 8, 13, 15]  // Set 4
];
let completedSets = [];
let shuffledIndices = [];
let emitter;
let successText;
let successBackground;
let mainScene;
let score = parseInt(sessionStorage.getItem('score') || '0'); // Initialize score
let scoreText;  // Text object for score display
let highScore = 50000;
let highScoreText; // text object for high score
let roundComplete = sessionStorage.getItem('roundComplete');
if (roundComplete == null) {
    roundComplete = 0;
}
// let urlParams = new URLSearchParams(window.location.search);
let round = parseInt(urlParams.get('round') ?? 1, 10); // Default to round 1 if no parameter is set
let words = wordSets[round];


document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        const urlParams = new URLSearchParams(window.location.search);
        const id = urlParams.get('id');

        // Regular expression to validate a UUID v4
        const uuidV4Regex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

        // Check if the id parameter exists and is a valid UUID v4
        if (id && uuidV4Regex.test(id)) {
            localStorage.setItem('id', id);
        } else {
            let id = localStorage.getItem('id');
            if (!id) {
                alert('Invalid id provided in the URL. Please provide a valid ID in order to get completion if you beat this challenge.');
            }
        }

        if (!round) {
            urlParams.set('round', roundComplete++);
            window.location.href = `${window.location.origin}${window.location.pathname}?${urlParams.toString()}`;
        }
    }, 250);
});

const gridCols = 4;
const gridRows = 4;
const boxWidth = 180;
const boxHeight = 120;
const gridXOffset = 50;
const gridYOffset = 50;

function preload() {
    this.load.image('flares', "/static/images/candyCane.png");
    this.load.image('overlay', "/static/images/background.webp");
    this.load.image('landing', "/static/images/landing.png");

    this.load.audio('bzzzt', '/static/audio/bzzzt.wav'); //this.sound.play('bzzzt');
    this.load.audio('click', '/static/audio/click.wav'); //this.sound.play('click');
    this.load.audio('ding', '/static/audio/ding.wav'); //this.sound.play('ding');
    this.load.audio('horaay', '/static/audio/horaay.wav'); //this.sound.play('horaay');
    console.log("Static files loaded");
}

function create() {
    //console.log('round ' + roundComplete);
    //console.log('score ' + score);
    mainScene = this;
    var overlay = this.add.image(400, 300, 'overlay').setDepth(0).setOrigin(0.5, 0.5);
    overlay.setScale(0.5);

    // Add title text (centered horizontally and aligned with the score's y-position)
    titleText = this.add.text(400, 15, 'Elf Connect', {
        fontSize: '30px',
        fill: '#000',  // Black color for the title
        align: 'center'
    });
    titleText.setOrigin(0.5, 0);  // Center the title horizontally on the x-axis

    if (roundComplete == 0) {
        var landing = this.add.image(400, 250, 'landing').setScale(.6).setDepth(2).setOrigin(0.5, 0.5).setInteractive();
        mainScene.input.once('pointerdown', function () {
            landing.destroy();
        })
    }


    shuffledIndices = Phaser.Utils.Array.Shuffle([...Array(16).keys()]);

    for (let i = 0; i < 16; i++) {
        let col = i % gridCols;
        let row = Math.floor(i / gridCols);
        let xPos = gridXOffset + col * boxWidth;
        let yPos = gridYOffset + row * boxHeight;
        let box = this.add.text(xPos, yPos, words[shuffledIndices[i]], {
            fontSize: '20px',
            //backgroundColor: '#0a7e28', // card color unselected
            backgroundColor: '#10ca40', // card color unselected
            color: '#000000', //text color for cards
            padding: { top: 20, left: 10, right: 10, bottom: 20 },
            align: 'center',
            fixedWidth: boxWidth - 20,
            fixedHeight: boxHeight - 20,
            wordWrap: { width: boxWidth - 40, useAdvancedWrap: true }
        }).setInteractive();

        box.index = shuffledIndices[i];
        box.selected = false;
        box.gridPos = i;

        box.on('pointerdown', function () {
            
            if (!this.selected) {
                this.setStyle({ backgroundColor: '#edbb99' }); // card color selected
                this.selected = true;
                selectedBoxes.push(this);
            } else {
                //this.setStyle({ backgroundColor: '#0a7e28' }); // card color unselected
                this.setStyle({ backgroundColor: '#10ca40' }); // card color unselected
                this.selected = false;
                selectedBoxes = selectedBoxes.filter(box => box !== this);
            }

            if (selectedBoxes.length === 4) {
                checkSelectedSet(this.scene);
            } else {
                mainScene.sound.play('click');
            }
        });

        wordBoxes.push(box);
    }

    emitter = this.add.particles(400, 250, 'flares', {
        lifespan: 4000,
        speed: { min: 150, max: 250 },
        scale: { start: 0.8, end: 0 },
        gravityY: 150,
        blendMode: 'ADD',
        emitting: false
    });

    // Add scoreboard text
    scoreText = this.add.text(600, 20, 'Score: ' + score, { fontSize: '20px', fill: '#000000' });
    highScoreText = this.add.text(20, 20, 'High Score: 50000', { fontSize: '20px', fill: '#000' });
}

function update() {
    // Nothing needed in the update loop for this simple game
}

function checkSelectedSet(scene) {
    let selectedIndices = selectedBoxes.map(box => box.index);
    selectedIndices.sort((a, b) => a - b);

    let isCorrectSet = false;
    let matchedSetIndex = -1;

    for (let i = 0; i < correctSets.length; i++) {
        if (JSON.stringify(selectedIndices) === JSON.stringify(correctSets[i])) {
            isCorrectSet = true;
            matchedSetIndex = i;
            break;
        }
    }

    if (isCorrectSet) {
        completedSets.push(matchedSetIndex);
        positionCompletedSets();
        disableCompletedSet(matchedSetIndex); // Disable interaction on the completed set
        shuffleRemainingRows();

        // Update score by 100 points
        score += 100;
        scoreText.setText('Score: ' + score);

        // Add high-score board
        if (score > 50000) {
            highScoreText.setText('High Score: ' + score);
            emitter.explode(20);
            submitAction(2);
            displaySuccessMessage('Great Job Hacker! Elf Connect Complete and Hacked!', function () {

            });
        }

        // If all sets are completed, trigger the fireworks effect
        if (completedSets.length === 4) {
            roundComplete++;
            scene.sound.play('horaay');
            gameStatus();
        } else {
            scene.sound.play('ding');
        }
    } else {
        selectedBoxes.forEach(box => {
            //box.setStyle({ backgroundColor: '#0a7e28' }); // card color unselected original
            box.setStyle({ backgroundColor: '#10ca40' }); // card color unselected
            box.selected = false;
        });
        scene.sound.play('bzzzt');
    }

    selectedBoxes = [];
}

function disableCompletedSet(setIndex) {
    correctSets[setIndex].forEach((wordIndex) => {
        let box = wordBoxes.find(box => box.index === wordIndex);
        if (box) {
            box.disableInteractive(); // Disable interaction on the box
        }
    });
}

function positionCompletedSets() {
    completedSets.forEach((setIndex, completedRowIndex) => {
        let yPos = gridYOffset + completedRowIndex * boxHeight;

        correctSets[setIndex].forEach((wordIndex, boxIndex) => {
            let box = wordBoxes.find(box => box.index === wordIndex);
            let xPos = gridXOffset + boxIndex * boxWidth;
            box.setStyle({
                backgroundColor: '#126079', // completed row color
                color: '#fff' //text color completed row cards
            });
            box.setPosition(xPos, yPos);
        });
    });
}

function shuffleRemainingRows() {
    let remainingBoxes = wordBoxes.filter(box => !completedSets.includes(correctSets.findIndex(set => set.includes(box.index))));
    let shuffledIndices = Phaser.Utils.Array.Shuffle(remainingBoxes.map(box => box.index));

    remainingBoxes.forEach((box, i) => {
        let remainingRowIndex = Math.floor(i / gridCols) + completedSets.length;
        let colIndex = i % gridCols;
        let xPos = gridXOffset + colIndex * boxWidth;
        let yPos = gridYOffset + remainingRowIndex * boxHeight;
        box.index = shuffledIndices[i];
        box.setText(words[shuffledIndices[i]]);
        box.setPosition(xPos, yPos);
        //box.setStyle({ backgroundColor: '#0a7e28' }); // unselected card color
        box.setStyle({ backgroundColor: '#10ca40' }); // unselected card color
    });
}


function gameStatus() {
    //console.log(roundComplete);
    if (roundComplete < 4) {
        emitter.explode(20);
        displaySuccessMessage('Round ' + roundComplete + ' Completed', function () {
            this.sessionStorage.setItem('score', score);
            this.sessionStorage.setItem('roundComplete', roundComplete);
            window.location.href = `${window.location.origin}${window.location.pathname}?round=${roundComplete + 1}`;
        });
    } else {
        emitter.explode(20);
        submitAction(1);
        displaySuccessMessage.call(this, 'Success! You have defeated the Elf Connect!!!!');
    }

}

async function submitAction(answer) {
    //const urlParams = new URLSearchParams(window.location.search);
    //const id = urlParams.get('id');
    //localStorage.setItem('id', id);
    let id = localStorage.getItem('id');
    if (!id) {
        alert('No ID found in localstorage so we could not submit your results');
    }
    const url = `/submit?id=${id}`;
    const data = { answer: answer }; // Send the answer as a JSON object

    //Original
    //const url = '/submit';
    //const data = { answer: answer };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            console.log('Success:', result);
            return true;
        } else {
            console.error('Error:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function displaySuccessMessage(message, callback) {
    if (successText) {
        successText.destroy();
    }
    if (successBackground) {
        successBackground.destroy();
    }

    const padding = 10;
    const textStyle = { fontSize: '24px', fill: '#00FF00', align: 'center' };
    successText = mainScene.add.text(mainScene.cameras.main.centerX, mainScene.cameras.main.centerY, message, textStyle);
    successText.setOrigin(0.5, 0.5);

    const textWidth = successText.width + 2 * padding;
    const textHeight = successText.height + 2 * padding;

    successBackground = mainScene.add.graphics();
    successBackground.fillStyle(0x000000, 0.8);
    successBackground.fillRect(
        mainScene.cameras.main.centerX - textWidth / 2,
        mainScene.cameras.main.centerY - textHeight / 2,
        textWidth,
        textHeight
    );

    mainScene.children.bringToTop(successText);

    setTimeout(() => {
        if (successText) {
            successText.destroy();
            successText = null;
        }
        if (successBackground) {
            successBackground.destroy();
            successBackground = null;
        }
        //console.log(roundComplete)
        if (roundComplete != 4) {
            callback();
        }
    }, 3000);
}
```