+++
title = 'Elf Minder 9000'
date = 2024-11-10T12:19:21+01:00
draft = false
weight = 3
+++

## Objective

> Assist Poinsettia McMittens with playing a game of Elf Minder 9000.

## Hints

| From | Hint |
| ---- | ---- |
| Poinsettia McMittens | Be sure you read the "Help" section thoroughly! In doing so, you will learn how to use the tools necessary to safely guide your elf and collect all the crates. |
| Poinsettia McMittens | Some levels will require you to click and rotate paths in order for your elf to collect all the crates. |
| Poinsettia McMittens | When developing a video game—even a simple one—it's surprisingly easy to overlook an edge case in the game logic, which can lead to unexpected behavior. |

## Solution pr level.

Explanatory comments provided when necessary.

### Sandy Start

![Sandy Start](/images/prologue/elf-minder-9000-sandy-start.png)

### Waves and crates

![Waves and Crates](/images/prologue/elf-minder-9000-waves-and-crates.png)

### Tidal Treasures

![Tidal Treasures](/images/prologue/elf-minder-9000-tidal-treasures.png)

### Dune Dash

In order to solve this, we must turn the trajectory path for the elf once he has gone back into the tunnel, so that on the return he'll hook up to the path leading to the goal flag.

![Dune Dash](/images/prologue/elf-minder-9000-dune-dash.png)

### Coral Cove

![Coral Cove](/images/prologue/elf-minder-9000-coral-cove.png)

### Shell Seekers

![Shell Seekers](/images/prologue/elf-minder-9000-shell-seekers.png)

### Palm Gove Shuffle

Once the elf has gone through the tunnel, we change the trajectory path so upon return the elf will head for the spring instead.

![Palm Grove Shuffle](/images/prologue/elf-minder-9000-palm-grove-shuffle.png)

#### Tropical Tangle

For this level we must change trajectory two times in order to traverse into the goal flag.

![Tropical Tangle](/images/prologue/elf-minder-9000-tropical-tangle.png)

### Crate Caper

In this level we must change the trajectory multiple times. The elf has to be routed to the goal flag and back using multiple routes in order to collect the crates. 

![Crate Caper](/images/prologue/elf-minder-9000-crate-caper.png)

### Shoreline Shuffle

Yet again, this level consists of multiple trajectory path changes in order to collec the crates

![Shoreline Shuffle](/images/prologue/elf-minder-9000-shoreline-shuffle.png)

### Beach Bounty

![Beach Bounty](/images/prologue/elf-minder-9000-beach-bounty.png)

### Driftwood Dunes

This was pretty straight forward, no change of trajectory neeeded

![Driftwood Dunes](/images/prologue/elf-minder-9000-driftwood-dunes.png)

### A real pickle

Stumbled on this part in the HTML source code, apparently it is an editor:

![A real pickle 1](/images/prologue/elf-minder-9000-a-real-pickle-1.png)

Removed the "hidden" stylesheet tag to make it visible:

![A real pickle 2](/images/prologue/elf-minder-9000-a-real-pickle-2.png)

Clicked the "Clear Entities" button, and placed a tunnel at the goal flag: 

![A real pickle 3](/images/prologue/elf-minder-9000-a-real-pickle-3.png)

Then clicked restart:

![A real pickle 4](/images/prologue/elf-minder-9000-a-real-pickle-4.png)

















---

Found this gem in the source code: 

https://hhc24-elfminder.holidayhackchallenge.com/game2.js

```javascript
if (isEditor) {
    adminControls.classList.remove('hidden');
    console.log('⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡');
    console.log('⚡ Hey, I noticed you are in edit mode! Awesome!');
    console.log('⚡ Use the tools to create your own level.');
    console.log('⚡ Level data is saved to a variable called `game.entities`.');
    console.log('⚡ I\'d love to check out your level--');
    console.log('⚡ Email `JSON.stringify(game.entities)` to evan@counterhack.com');
    console.log('⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡');
}
```

## Mapping

Prior to playing this game I spent a lot of time mapping out the technology that controls it. Here are my notes.

### Movement

#### Y-axis

| Position | Value | Content |
| -------- | ----- | ------- |
| game.entities[0][1] | 1 | First dot from upper right corner |
| game.entities[0][1] | 10 | Last dot from upper right corner, max. 10 |


#### X-axis

| Position | Value | Content |
| -------- | ----- | ------- |
| game.entities[0][0] | 1 | First dot from upper left side |
| game.entities[0][0] | 10 | Last dot from upper left side, max. 12 |

### Entities

| Entity | Value | Entity Type | 
| --- | --- | --- |
| game.entities[0][2] | 0 | Start  |
| game.entities[0][2] | 1 | Flag  |
| game.entities[0][2] | 2 | Crate  |
| game.entities[0][2] | 3 | Stone |
| game.entities[0][2] | 4 | Sleepy Crab  |
| game.entities[0][2] | 5 | Sizzling Sand  |
| game.entities[0][2] | 6 | Tunnel  |
| game.entities[0][2] | 7 | Spring  |



```javascript
game.entities.forEach((item) => {
  // Move start flag
  if (item[2] == 0) {
    item[0] = 1;
    item[1] = 1;
  }

  // Move goal flag
  else if (item[2] == 1) {
    item[0] = 1;
    item[1] = 9;
  }

  // Move crates
  else if (item[2] == 2) {
    item[0] = 1;
  }

  // Other things
  else {
    item[1] = 12
  }

});






game.entities.forEach((item) => {
  if (item[2] !== 0 && item[2] !== 1 && item[2] !== 2) {
    item[1] = 12;
  }
});

enable edit mode:
https://hhc24-elfminder.holidayhackchallenge.com/index.html?id=30d23f1c-4d17-4646-8475-f8ed051fbaf2&level=Sandy%20Start&edit=1





```