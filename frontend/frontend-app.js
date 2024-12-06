'use strict';
const map = L.map('map').setView([55, 24.963], 2.5);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 15,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
//display map DONT TOUCH!

const marker = L.marker([60.3172, 24.963301]).addTo(map);
function closePopup(evt){dialog.close()}
document.querySelector('span').addEventListener('click',closePopup);
const dialog=document.querySelector('dialog');
const aside=document.querySelector('.container aside');
const container =document.querySelector('.container');
const mainMenu=document.querySelector('.main-menu');
async function loadSave(player_id){
  const response = await fetch(`/loadSave/${player_id}`);
  return await response.json();
}
async function leadLeaderboard(player_id){
  let name=prompt('What do you want to be saved as')
  let difficulty=prompt('Enter a number for difficulty(1-3)(the higher the number the harder the game is)')
  const response = await fetch(`/loadLeaderboard/${name}/${difficulty},${player_id}`);
  return await response.json();
}
async function newGame(){
  let name=prompt('What do you want to be saved as')
  let difficulty=prompt('Enter a number for difficulty(1-3)(the higher the number the harder the game is)')
  const response = await fetch (`mainGame/${name}/${difficulty}`)
  return await response.json();
}
function displayPlayer(data){
  data.forEach((playerInfo)=>{
    let stuff=document.createElement('p')
    stuff.innerText=data.playerInfo
    aside.appendChild(stuff);
  })
}
async function mainScreen(option){
  if(option==='leaderboard'||option=== 'personal'){
  const response = await fetch(`http://127.0.0.1:8000/mainScreen/${option}`);
  const data = await response.json();
    if(option==='leaderboard'){
      dialog.innerHTML='';
      for(let i=0; i<data.content.length;i++){
        let item=document.createElement('div');
        let name=document.createElement('p');name.innerText=data.content[i][0];
        let score=document.createElement('p');score.innerText=data.content[i][1];
        let list=document.createElement('p');list.innerText=data.content[i][2];
        item.appendChild(name);item.appendChild(score);item.appendChild(list);
        dialog.appendChild(item);
      dialog.showModal()
      }
    } else if (option=== 'personal') {
      dialog.innerHTML = '';
      for (let i = 0; i < Object.keys(data.content).length; i++) {
        let item = document.createElement('div')
        let content = document.createElement('p');
        content.innerText = data.content[i + 1][0] + ' | Difficulty:' +
            data.content[i + 1][1] + ' | Balance: ' + data.content[i + 1][2] +
            ' | Airports Left:' + Object.keys(data.content[i + 1][3]).length +
            ' | Fuel:' + data.content[i + 1][5] + ' | Hints:' +
            data.content[i + 1][6] + ' | CO2:' + data.content[i + 1][7];
        item.appendChild(content);
        dialog.appendChild(item)
      }
      dialog.showModal()
    }
  } else if (option=== 'newGame'){
    displayPlayer(newGame());
  }
}


//for main menu showing and hiding toggle style between class .screen; same for gameplay screen
//3 button on main menu for each function, add event listener on each button, once game start toggle .screen style for both container and mainmenu
//place nodes on maps, target is circle, current position is marker
//player info is in aside
//shops button, hints and quit game is in header
//further implementation asking group member