+++
title = 'Elf Minder 9000'
date = 2024-11-10T12:19:21+01:00
draft = true
weight = 3
+++




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