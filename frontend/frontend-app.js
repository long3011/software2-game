'use strict';
const map = L.map('map').setView([55, 24.963], 2.5);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 15,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
//display map DONT TOUCH!

//Because of how js behave, i have to merge manu function together
//I apologize to anyone in the future that have to work on this code

let marker = L.marker([60.3172, 24.963301]).addTo(map);
function closePopup(evt){dialog.close()}
let span1 =document.getElementById('close_modal');
span1.addEventListener('click',closePopup);
const dialog=document.querySelector('dialog');
const aside=document.querySelector('.container aside');
const header=document.querySelector('header');
const container =document.querySelector('.container');
const mainMenu=document.querySelector('.mainMenu');
const hintButton=document.getElementById('hintshop');
const fuelButton=document.getElementById('fuel');
const useHintButton=document.getElementById('hint');
const quit =document.getElementById('quit');
const planeSound=new Audio('airplane sound.mp3')
let circle= {}
async function loadSave(player_id){
  mainMenu.classList.toggle('no_screen')
  header.classList.toggle('no_screen')
  container.classList.toggle('no_screen');
  dialog.close()
  const response = await fetch(`http://127.0.0.1:8000/loadSave/${player_id}`);
  const data=await response.json();
  let airports
  for(let playerInfo in data){
    let thing=document.createElement('p')
    thing.id='property'
    let stuff=document.createElement('p')
    stuff.id=playerInfo
    if (playerInfo==='Airports'){
      thing.innerText='Airports left:'
      stuff.innerText=Object.keys(data[playerInfo]).length
      airports=data[playerInfo]
    } else {
      thing.innerText=playerInfo+':'
      stuff.innerText=data[playerInfo]
    }
    aside.appendChild(thing)
    aside.appendChild(stuff);
}
  for(let airport in airports){
      let coords=[airports[airport][3],airports[airport][4]]
      circle[airport] = L.circle(coords, {
      color: 'red',
      fillColor: '#f03',
      fillOpacity: 0.5,
      radius: 1000
      }).addTo(map);
      circle[airport].on('click', function(){flyDestination(airport,coords,circle)});
  }}
async function loadLeaderboard(player_id){
  let difficulty=0
  let name=player_id;
  while(difficulty>3||difficulty<1) {
    name = prompt('What do you want to be saved as')
    difficulty = prompt(
        'Enter a number for difficulty(1-3)(the higher the number the harder the game is)')
    if(name===null||difficulty===null){
      return
    }
  }
  header.classList.toggle('no_screen')
  container.classList.toggle('no_screen');
  dialog.close()
  mainMenu.classList.toggle('no_screen')
  const response = await fetch(
        `http://127.0.0.1:8000/loadLeaderboard/${name}/${difficulty}/${player_id}`);
  const data=await response.json()
  let airports
  for(let playerInfo in data){
    let thing=document.createElement('p')
    thing.id='property'
    let stuff=document.createElement('p')
    stuff.id=playerInfo
    if (playerInfo==='Airports'){
      thing.innerText='Airports left:'
      stuff.innerText=Object.keys(data[playerInfo]).length
      airports=data[playerInfo]
    } else {
      thing.innerText=playerInfo+':'
      stuff.innerText=data[playerInfo]
    }
    aside.appendChild(thing)
    aside.appendChild(stuff);
}for(let airport in airports){
    let coords=[airports[airport][3],airports[airport][4]]
    circle[airport] = L.circle(coords, {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.5,
    radius: 1000
    }).addTo(map);
    circle[airport].on('click', function(){flyDestination(airport,coords,circle)});
  }}
async function newGame(){
  let difficulty=0
  let name='New player';
  while(difficulty>3||difficulty<1) {
    name = prompt('What do you want to be saved as')
    difficulty = prompt(
        'Enter a number for difficulty(1-3)(the higher the number the harder the game is)')
    if(name===null||difficulty===null){
      return
    }
  }
  mainMenu.classList.toggle('no_screen')
  header.classList.toggle('no_screen')
  container.classList.toggle('no_screen');
  const response = await fetch(
        `http://127.0.0.1:8000/mainGame/${name}/${difficulty}`);
  const data= await response.json()
  let airports
  for(let playerInfo in data){
    let thing=document.createElement('p')
    thing.id='property'
    let stuff=document.createElement('p')
    stuff.id=playerInfo
    if (playerInfo==='Airports'){
      thing.innerText='Airports left:'
      stuff.innerText=Object.keys(data[playerInfo]).length
      airports=data[playerInfo]
    } else {
      thing.innerText=playerInfo+':'
      stuff.innerText=data[playerInfo]
    }
    aside.appendChild(thing)
    aside.appendChild(stuff);
}
  for(let airport in airports){
    let coords=[airports[airport][3],airports[airport][4]]
    circle[airport] = L.circle(coords, {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.5,
    radius: 3000
    }).addTo(map);
    circle[airport].on('click', function(){flyDestination(airport,coords,)});
  }}
function flyDestination(airport_id,coords){
  marker.remove();
  marker = L.marker(coords).addTo(map);
  circle[airport_id].remove();
  flyTo(airport_id);
}
async function mainScreen(option){
  if(option==='leaderboard'||option=== 'personal'){
  const response = await fetch(`http://127.0.0.1:8000/mainScreen/${option}`);
  const data = await response.json();
    if(option=== 'leaderboard'){
      dialog.innerHTML='';
      dialog.appendChild(span1);
      for(let i=0; i<data.content.length;i++){
        let item=document.createElement('div');
        let name=document.createElement('p');name.innerText=data.content[i][0];
        let score=document.createElement('p');score.innerText=data.content[i][1];
        let list=document.createElement('p');list.innerText=data.content[i][2];
        item.appendChild(name);item.appendChild(score);item.appendChild(list);
        item.addEventListener('click',()=>{loadLeaderboard(i+1)})
        dialog.appendChild(item);
      dialog.showModal()
      }
    } else if (option=== 'personal') {
      dialog.innerHTML = '';
      dialog.appendChild(span1);
      for (let i = 0; i < Object.keys(data.content).length; i++) {
        let item = document.createElement('div')
        let content = document.createElement('p');
        content.innerText = data.content[i + 1][0] + ' | Difficulty:' +
            data.content[i + 1][1] + ' | Balance: ' + data.content[i + 1][2] +
            ' | Airports Left:' + Object.keys(data.content[i + 1][3]).length +
            ' | Fuel:' + data.content[i + 1][5] + ' | Hints:' +
            data.content[i + 1][6] + ' | CO2:' + data.content[i + 1][7];
        item.appendChild(content);
        item.addEventListener('click', function(){loadSave(i+1); })
        dialog.appendChild(item)
      }
      dialog.showModal()
    }
  } else if (option=== 'newGame'){
    newGame();
  }
}
async function flyTo(airport_id){
  let points=document.querySelector('#Points');
  let remaining = document.querySelector('#Airports');
  let fuel =document.querySelector('#Fuel');
  let co2=document.querySelector('#Co2')
  let response=await fetch (`http://127.0.0.1:8000/flyTo/${airport_id}`)
  let data=await response.json()
  planeSound.play()
  fuel.innerText=data['Fuel'];
  if (parseInt(data['Fuel'])<0){lost()}
  else {
    remaining.innerText = data['Remaining'];
    if (parseInt(data['Remaining']) === 0) {won()}
    else {
      alert(`You flew ${data['Distance']}km`)
      points.innerText = data['Points'];
      co2.innerText = data['Co2']
    }
  }
}
async function shop(item) {
  let balance = document.querySelector('#Money');
  let fuel = document.querySelector('#Fuel');
  let hints = document.querySelector('#Hints');
  let response = await fetch(`http://127.0.0.1:8000/shop/${item}`)
  let data = await response.json();
  alert(`You have purchased ${item}`)
  balance.innerText = data['balance'];fuel.innerText=data['fuel'];hints.innerText=data['hints']
}
async function hint(){
  let response=await fetch ('http://127.0.0.1:8000/hint')
  let data= await response.json()
  let hints = document.querySelector('#Hints');
  if(parseInt(hints.innerText)>0) {
    hints.innerText = data['hints']
    circle[data['nearest']].setStyle({color: 'blue'})
  } else {
    alert('You dont have any hints left')
  }
}
async function stop(status){
  let response = await fetch(`http://127.0.0.1:8000/quit/${status}`)
  let data = await response.json();
  console.log(data)
  marker.remove();
  marker= L.marker([60.3172, 24.963301]).addTo(map);
  aside.innerHTML=''
  mainMenu.classList.toggle('no_screen')
  container.classList.toggle('no_screen')
  header.classList.toggle('no_screen')
}
function quiting(evt){
  if(confirm('Are you sure')){
    if(confirm('Do you want to save')){
      dialog.innerHTML = '';
      dialog.appendChild(span1);
      const personal=document.createElement('div');personal.addEventListener('click', function(){stop('personal');dialog.close()});
      personal.innerText='Save to play later'
      personal.id='personal'
      const leaderboard =document.createElement('div');leaderboard.addEventListener('click',function(){stop('leaderboard');dialog.close()})
      leaderboard.innerText='Save to leaderboard'
      leaderboard.id='leaderboard'
      dialog.appendChild(personal);dialog.appendChild(leaderboard);
      dialog.showModal()
    } else {
      stop('somethingcausethisdontmatter')
    }
  }
}
function lost(){
    alert('You ran out of fuel')
    marker.remove();
    marker= L.marker([60.3172, 24.963301]).addTo(map);
    aside.innerHTML=''
    mainMenu.classList.toggle('no_screen')
    container.classList.toggle('no_screen')
    header.classList.toggle('no_screen')
}
function won(){
    alert('Congratulations! You have travelled to all the airports')
    if(confirm('Do you want to be saved to the leaderboard?')){
      stop('leaderboard')
    }
    marker.remove();
    marker= L.marker([60.3172, 24.963301]).addTo(map);
    aside.innerHTML=''
    mainMenu.classList.toggle('no_screen')
    container.classList.toggle('no_screen')
    header.classList.toggle('no_screen')
}

container.classList.toggle('no_screen')
header.classList.toggle('no_screen')
document.getElementById('newGame').addEventListener('click', function(){mainScreen('newGame')});
document.getElementById('saves').addEventListener('click', function(){mainScreen('personal')});
document.getElementById('leaderboard').addEventListener('click', function(){mainScreen('leaderboard')});
hintButton.addEventListener('click', function(){shop('hints')});
fuelButton.addEventListener('click',function(){shop('fuel')});
quit.addEventListener('click', quiting);
useHintButton.addEventListener('click',hint)

//make difficulty into a pop-up dialog
//make everything pretty
//make saves to have only 3 slots, and each slots is consistent
//further implementation asking group member