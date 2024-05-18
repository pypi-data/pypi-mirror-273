AppcustomHook = '''import "./App.css";
import useCustomHook from "./useCustomHook";

function App() {
  const [count, { increment, decrement, reset }] = useCustomHook(0);
  return (
    <div className="container">
      <div>
        <h1 className="count">{count}</h1>
      </div>

      <div className="buttons">
        <button className="button" id="increment" onClick={increment}>
          Increment
        </button>
        <button className="button" id="decrement" onClick={decrement}>
          Decrement
        </button>
        <button className="button" id="reset" onClick={reset}>
          Reset
        </button>
      </div>
    </div>
  );
}

export default App;
'''

bgchange_onhover = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Change colour</title>
    <style>
      #box {
        width: 500px;
        height: 500px;
        background-color: blue;
      }

      body {
        justify-content: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 50px;
      }
    </style>
  </head>
  <body>
    <h1>Change colour when mouse enters</h1>

    <div id="box">Box</div>
    <script>
      var box = document.querySelector("#box");

      box.addEventListener("mouseenter", onmouseenter);

      function onmouseenter(e) {
        e.target.style.backgroundColor = "red";
      }

      box.addEventListener("mouseleave", function (e) {
        e.target.style.backgroundColor = "blue";
      });
    </script>
  </body>
</html>
'''

bgcolor_change = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Change Background Color</title>
    <style>
        /* Internal CSS */
        button {
            padding: 10px 20px;
            background-color: #4CAF50; /* Green */
            border: none;
            color: white;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        }

        button:hover {
            background-color: #45a049; /* Darker Green */
        }
    </style>
  </head>
  <body>
    <button id="changeColorButton">Change Background Color</button>

    <script>
      const changeColorButton = document.getElementById("changeColorButton");

      changeColorButton.addEventListener("click", function () {
        // Generate a random hexadecimal color
        const randomColor =
          "#" + Math.floor(Math.random() * 16777215).toString(16);

        // Change the background color of the body
        document.body.style.backgroundColor = randomColor;
      });
    </script>
  </body>
</html>
'''

calculator = '''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculator</title>
    <style>
        .container {
            display: grid;
            gap: 1rem;
        }

        .container button {
            font-size: 4rem;
            width: 100px;
        }

        .box {
            text-align: center;
            padding: 6rem;

        }

        #ans {
            font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
            font-size: 2rem;
        }

        .adding,
        .subtraction,
        .mul,
        .divide {
            background-color: yellow;
        }

        .equals {
            background-color: aliceblue;
        }

        .C {
            background-color: orange;
        }

        button:hover {
            opacity: 70%;
        }
    </style>
</head>

<body>
    <div class="box">
        <div class="container">
            <div class="high">
                <input id="ans" readonly></p>
            </div>
            <div class="top">
                <button onclick="display('7')">7</button>
                <button onclick='display("8")'>8</button>
                <button onclick='display("9")'>9</button>
                <button class="adding" onclick="display('+')">+</button>
            </div>
            <div class="mid">
                <button onclick='display("4")'>4</button>
                <button onclick='display("5")'>5</button>
                <button onclick='display("6")'>6</button>
                <button class="subtraction" onclick="display('-')">-</button>
            </div>
            <div class="bottom">
                <button onclick='display("1")'>1</button>
                <button onclick='display("2")'>2</button>
                <button onclick='display("3")'>3</button>
                <button class="mul" onclick="display('*')">*</button>
            </div>
            <div class="lower">
                <button onclick='display("0")'>0</button>
                <button onclick='clearinput()' class="C">C</button>
                <button class="equals" onclick="calculate()">=</button>
                <button class="divide" onclick="display('/')">/</button>
            </div>
        </div>
    </div>

    <script>
        const ans = document.getElementById('ans')
        function display(input) {
            ans.value += input
        }
        function clearinput() {
            ans.value = '';
        }

        function calculate() {
            try {
                ans.value = eval(ans.value)
            }
            catch {
                ans.value = "Error"
            }
        }

    </script>
</body>

</html>'''

card = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Responsive Cards</title>

    <style>
      *{
        box-sizing: border-box;
        font-family: sans-serif;
      }

      .container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 100px;
      }

      .card {
        width: 325px;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0px 2px 4px rgb(223, 223, 223);
        margin: 20px;
      }

      .card img {
        width: 100%;
        height: auto;
      }

      .content {
        padding: 10px;
      }

      .content h2 {
        font-size: 28px;
        margin-bottom: 8px;
      }
      .content p {
        font-size: 15px;
        line-height: 1.3;
      }

      .btn {
        font-size: 35px;
        display: inline-block;
        padding-left: 20px;
        padding-right: 20px;
        padding-top: 5px;
        padding-bottom: 5px;
        background-color: #d1c7c7;
        text-decoration: none;
        border-radius: 4px;
        margin-top: 16px;
        color: green;
      }
      
    </style>
  </head>

  <body>
    <div class="container">

        <div class="card">
            <img src="images/bg.jpg" alt="Image 1">
            <div class="content">
                <h2>Image 1</h2>
                <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum, amet.</p>
                <a href="#" class="btn">Buy</a>
            </div>
        </div>

        <div class="card">
            <img src="images/bg1.jpg" alt="Image 1">
            <div class="content">
                <h2>Image 1</h2>
                <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum, amet.</p>
                <a href="#" class="btn">Buy</a>
            </div>
        </div>

        <div class="card">
            <img src="images/bg2.jpg" alt="Image 1">
            <div class="content">
                <h2>Image 1</h2>
                <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum, amet.</p>
                <a href="#" class="btn">Buy</a>
            </div>
        </div>


      </div>
    </div>
  </body>
</html>
'''

Card = '''import React from "react";
import image1 from "./asset/bg.jpg";
import image2 from "./asset/bg1.jpg";
import image3 from "./asset/bg2.jpg";

const Card = () => {
  return (
    <div>
      <style>
        {`
          * {
            box-sizing: border-box;
            font-family: sans-serif;
          }

          .container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 100px;
          }

          .card {
            width: 325px;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0px 2px 4px rgb(223, 223, 223);
            margin: 20px;
          }

          .card img {
            width: 100%;
            height: auto;
          }

          .content {
            padding: 10px;
          }

          .content h2 {
            font-size: 28px;
            margin-bottom: 8px;
          }

          .content p {
            font-size: 15px;
            line-height: 1.3;
          }

          .btn {
            font-size: 35px;
            display: inline-block;
            padding-left: 20px;
            padding-right: 20px;
            padding-top: 5px;
            padding-bottom: 5px;
            background-color: #d1c7c7;
            text-decoration: none;
            border-radius: 4px;
            margin-top: 16px;
            color: green;
          }
        `}
      </style>
      <div className="container">
        <div className="card">
          <img src={image1} alt="Image 1" />
          <div className="content">
            <h2>Image 1</h2>
            <p>
              Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum,
              amet.
            </p>
            <a href="#" className="btn">
              Buy
            </a>
          </div>
        </div>

        <div className="card">
          <img src={image2} alt="Image 1" />
          <div className="content">
            <h2>Image 1</h2>
            <p>
              Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum,
              amet.
            </p>
            <a href="#" className="btn">
              Buy
            </a>
          </div>
        </div>

        <div className="card">
          <img src={image3} alt="Image 1" />
          <div className="content">
            <h2>Image 1</h2>
            <p>
              Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum,
              amet.
            </p>
            <a href="#" className="btn">
              Buy
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Card;
'''

confirmation = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Appointment Confirmation</title>
  </head>
  <body>
    <h1>Appointment Confirmation</h1>
    <pre id="appointmentDetails"></pre>

    <script>
      const appointmentDetails = localStorage.getItem("appointmentDetails");
      document.getElementById("appointmentDetails").textContent =
        appointmentDetails;
    </script>
  </body>
</html>
'''

Counter = '''import { useState } from 'react'

const Card = () => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <style>
        {`
          #root {
            max-width: 1280px;
            margin: 0 auto;
            padding: 2rem;
            text-align: center;
          }

          .card {
            padding: 2em;
            gap: 2em;
          }

          button{
            margin: 20px;
            font-size: 25px;
            border-radius: 8px;
            border: 1px solid transparent;
            padding: 0.6em 1.2em;
            cursor: pointer;
            font-weight: 500;
          }
        `}
      </style>
      <h1>Counter app</h1>
      <h2>count is {count}</h2>
      <div className="card">
        <button className="inc" onClick={() => setCount((count) => count + 1)}>
          increment
        </button>
        <button className="dec" onClick={() => setCount((count) => count - 1)}>
          decrement
        </button>
        <button className="reset" onClick={() => setCount((count) => 0)}>
          reset
        </button>
      </div>
    </div>
  );
};

export default Card;
'''

customHooks = '''import { useState } from "react";

const useCustomHook = (initialCount) => {
  const [count, setCount] = useState(initialCount);
  const increment = () => setCount((prevCount) => prevCount + 1);
  const decrement = () => setCount(count - 1);
  const reset = () => setCount(0);
  return [count, { increment, decrement, reset }];
};

export default useCustomHook;
'''

dropdown = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Dropdown Menu</title>
    <style>
      .dropdown {
        position: relative;
        display: inline-block;
      }

      .dropdown-content a {
        color: black;
        padding: 12px 16px;
        display: block;
      }
    </style>
  </head>
  <body>
    <div class="dropdown">
      <button class="dropbtn" onclick="toggleDropdown()">Dropdown</button>
      <div class="dropdown-content" id="dropdownContent">
        <a href="#">Option 1</a>
        <a href="#">Option 2</a>
        <a href="#">Option 3</a>
      </div>
    </div>

    <script>
      function toggleDropdown() {
        var dropdownContent = document.getElementById("dropdownContent");
        if (dropdownContent.style.display === "block") {
          dropdownContent.style.display = "none";
        } else {
          dropdownContent.style.display = "block";
        }
      }
    </script>
  </body>
</html>
'''

form_validation = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Doctor Appointment Form</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f9f9f9;
      }
      form {
        max-width: 400px;
        margin: 20px auto;
        padding: 20px;
        background-color: #fff;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
      }

      input, select {
        width: 100%;
        padding: 8px;
        margin: 5px 0;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
      }
      button {
        width: 100%;
        padding: 10px;
        background-color: #007bff;
        color: #fff;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
      }
      button:hover {
        background-color: #0056b3;
      }
    </style>
  </head>
  
  <body>
    <form id="appointmentForm" onsubmit="return validateForm()">
      <input type="text" id="name" placeholder="Your Name" required />
      <input type="email" id="email" placeholder="Your Email" required />
      <input type="date" id="date" required />
      <input type="time" id="time" required />
      <select id="service" required>
        <option value="">Select Service</option>
        <option value="Consultation">Consultation</option>
        <option value="Check-up">Check-up</option>
        <option value="Procedure">Procedure</option>
      </select>
      <label for="payment">Payment Method:</label>
      <input type="checkbox" id="onlinePayment" value="Online" /> Online
      <input type="checkbox" id="offlinePayment" value="Offline" /> Offline
      <button type="submit">Book Appointment</button>
    </form>

    <script>
      function validateForm() {
        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const date = document.getElementById("date").value;
        const time = document.getElementById("time").value;
        const service = document.getElementById("service").value;
        const onlinePayment = document.getElementById("onlinePayment").checked;
        const offlinePayment =
          document.getElementById("offlinePayment").checked;

        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (
          name === "" ||
          email === "" ||
          date === "" ||
          time === "" ||
          service === "" ||
          (!onlinePayment && !offlinePayment)
        ) {
          alert("Please fill in all fields.");
          return false;
        }

        if (!email.match(emailPattern)) {
          alert("Please enter a valid email address.");
          return false;
        }

        const appointmentDetails = `
        Name: ${name}
        Email: ${email}
        Date: ${date}
        Time: ${time}
        Service: ${service}
        Payment Method: ${onlinePayment ? "Online" : "Offline"}
    `;

        localStorage.setItem("appointmentDetails", appointmentDetails);
        window.location.href = "confirmation.html";
        return false;
      }
    </script>
  </body>
</html>'''

guess = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div class="container">
      <h1>Guess the correct number between 1 to 10</h1>
      <label for="number">Number</label>
      <input type="number" id="number" />
      <button onclick="check()">Check</button>
    </div>

    <div class="msg"></div>

    <script>
      var random = Math.floor(Math.random() * 10);

      function check() {
        num = document.querySelector("#number").value;
        console.log(random);
        msg = document.querySelector(".msg");
        console.log(num);
        if (parseInt(num) === random) {
          msg.innerHTML = "Good Work";
        } else {
          msg.innerHTML = "Not matched";
        }
        document.querySelector("#number").value = "";
      }
    </script>
  </body>
</html>
'''

image_carousel = '''<!DOCTYPE html>
<html>
  <head>
    <title>Carousel</title>
  </head>

  <body>
    <div style="display: flex; flex-direction: column; padding: 20px">
      <img src="images/bg.jpg" id="image" width="500px" />
      <div
        style="
          display: block;
          justify-content: space-between;
          font-size: larger;
        "
      >
        <button
          id="left"
          style="margin-right: 390px; font-size: large; margin-top: 20px"
        >
          Left
        </button>
        <button id="right" style="font-size: large; margin-top: 20px">
          Right
        </button>
      </div>
    </div>
  </body>
  
  <script>
    image = document.getElementById("image");
    let array = ["images/bg.jpg", "images/bg1.jpg", "images/bg2.jpg"];
    
    document.getElementById("right").addEventListener("click", () => {
      const url = image.src;
      imageIndex = 0;
      const lastIndex = url.lastIndexOf("/");
      const fileName = url.substring(lastIndex + 1);
      for (let i = 0; i < array.length; i++) {
        if (array[i] == fileName) {
          imageIndex = i;
        }
      }
      imageIndex = (imageIndex + 1) % array.length;
      image.src = array[imageIndex];
    });
    document.getElementById("left").addEventListener("click", () => {
      const url = image.src;
      imageIndex = 0;
      const lastIndex = url.lastIndexOf("/");
      const fileName = url.substring(lastIndex + 1);
      for (let i = 0; i < array.length; i++) {
        if (array[i] == fileName) {
          imageIndex = i;
        }
      }
      if (imageIndex == 0) {
        imageIndex = array.length - 1; 
        image.src = array[imageIndex];
      } else {
        imageIndex = (imageIndex - 1) % array.length;
        image.src = array[imageIndex];
      }
    });
  </script>
</html>
'''

image_gallery = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Image Gallery</title>
    <style>
      .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: #f0f0f0;
      }

      .gallery {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(3, 1fr);
        grid-gap: 20px;
      }

      .gallery img {
        width: 100%;
        height: auto;
        object-fit: cover;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
        cursor: pointer;
      }

      .gallery img:hover {
        transform: scale(1.05);
      }

      .modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.7);
        z-index: 1;
        overflow: auto;
        display: flex;
        justify-content: center;
        align-items: center;
      }

      .modal-content {
        max-width: 100%;
        max-height: 100%;
      }

      .modal-content img {
        width: 100%;
        height: 100%;
        object-fit: contain;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="gallery">
        <img src="images/bg.jpg" alt="Image 1" onclick="openModal(this.src)" />
        <img src="images/bg1.jpg" alt="Image 2" onclick="openModal(this.src)" />
        <img src="images/bg2.jpg" alt="Image 3" onclick="openModal(this.src)" />
      </div>
    </div>

    <div id="myModal" class="modal" onclick="closeModal()">
      <span class="close">&times;</span>
      <img class="modal-content" id="modalImg" />
    </div>

    <script>
      function openModal(src) {
        var modal = document.getElementById("myModal");
        var modalImg = document.getElementById("modalImg");
        modal.style.display = "flex";
        modalImg.src = src;
      }

      function closeModal() {
        var modal = document.getElementById("myModal");
        modal.style.display = "none";
      }
    </script>
  </body>
</html>
'''

index = '''//Basic types

let id: number =5
let company: string = "Web dev"
let x:any = 'Hello'

let ids:number[] = [1,2,3,4,5]
let arr: any[] = [1,true,"Hello"]

//Tuple
let person : [number,string,boolean] = [1,'jash',true]

let employee : [number,string][]

employee = [
    [1,'jash'],
    [2,'John']
]

//UNION

let pid:number|string 
pid='22'

//Enum

enum Direction{
    up=1,down,right,left
}

console.log(Direction.up)

//Object

type User = {
    id:number,name:string
}

const user: User ={
    id:1,
    name:"jash"
}

//Type Assertion
let cid: any =2
let customerId = cid as number

//Functions
function add(x:number,y:number) :number
{
    return x+y
}

console.log(add(1,2))

function log(message:string | number) : void {
    console.log(message)
}

//Interfaces
interface UserInterface {
    id: number,
    name: string,
    age?:number
}

const User1: UserInterface = {
    id: 2,
    name: "jash"
}

User1.id = 5

type point = number | string
const p1: point = 1


interface Mathfunc{
    (x:number, y:number): number
}

const addition: Mathfunc = (x: number, y:number) => x+y     //basicalyy yeh dono interface h like java same 
const subtraction: Mathfunc = (x: number, y:number) => x-y    

//Classes

class Person{
    id: number  //public,private,protected ...java jaisa daal sakte h id ya kisike b aage
    name: string

    constructor(id: number, name:string)
    {
        this.id = id
        this.name = name
    }
}

const jash = new Person(1,'jash parmar')
console.log(jash)

jash.id=5
console.log(jash)

//extend class
class Employee extends Person{
    position:string

    constructor(id:number, name:string, position:string)
    {
        super(id,name)
        this.position=position
    }
}

const emp = new Employee(3,'David','Webdev')
console.log(emp.name)
console.log(emp.position)'''

largest = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Largest integer</title>
  </head>
  <body>
    <div class="container">
      <h2>Display largest</h2>
      <input id="num1" type="number" />
      <input id="num2" type="number" />
      <button value="submit" class="btn">Submit</button>
      <div class="msg"></div>
    </div>
    <script>
      const btn = document.querySelector(".btn");
      const msg = document.querySelector(".msg");

      btn.addEventListener("click", onsubmit);

      function onsubmit(e) {
        e.preventDefault();
        const num1 = document.querySelector("#num1").value;
        const num2 = document.querySelector("#num2").value;
        const ans = num1 > num2 ? num1 : num2;
        console.log(ans);
        msg.innerHTML = ans;
      }
    </script>
  </body>
</html>
'''

lazy_loader = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lazy Loading</title>
</head>
<body>

    <div class="container">

        <img src="images/bg.jpg" alt="" loading="lazy">
        <img src="images/bg1.jpg" alt="" loading="lazy">
        <img src="images/bg2.jpg" alt="" loading="lazy">
        <img src="images/bg.jpg" alt="" loading="lazy">
        <img src="images/bg1.jpg" alt="" loading="lazy">
        <img src="images/bg2.jpg" alt="" loading="lazy">
        <img src="images/bg.jpg" alt="" loading="lazy">
        <img src="images/bg1.jpg" alt="" loading="lazy">
        <img src="images/bg2.jpg" alt="" loading="lazy">
        <img src="images/bg.jpg" alt="" loading="lazy">
        <img src="images/bg1.jpg" alt="" loading="lazy">
        <img src="images/bg2.jpg" alt="" loading="lazy">
        <img src="images/bg.jpg" alt="" loading="lazy">
        <img src="images/bg1.jpg" alt="" loading="lazy">
        <img src="images/bg2.jpg" alt="" loading="lazy">
        <img src="images/bg.jpg" alt="" loading="lazy">
        <img src="images/bg1.jpg" alt="" loading="lazy">
        <img src="images/bg2.jpg" alt="" loading="lazy">
        <img src="images/bg.jpg" alt="" loading="lazy">
        <img src="images/bg1.jpg" alt="" loading="lazy">
        <img src="images/bg2.jpg" alt="" loading="lazy">
        <img src="images/bg.jpg" alt="" loading="lazy">
        <img src="images/bg1.jpg" alt="" loading="lazy">
        <img src="images/bg2.jpg" alt="" loading="lazy">
        <img src="images/bg.jpg" alt="" loading="lazy">
        <img src="images/bg1.jpg" alt="" loading="lazy">
        <img src="images/bg2.jpg" alt="" loading="lazy">
        <img src="images/bg.jpg" alt="" loading="lazy">
        <img src="images/bg1.jpg" alt="" loading="lazy">
        <img src="images/bg2.jpg" alt="" loading="lazy">
        <img src="images/bg.jpg" alt="" loading="lazy">
        <img src="images/bg1.jpg" alt="" loading="lazy">
        <img src="images/bg2.jpg" alt="" loading="lazy">
        <img src="images/bg.jpg" alt="" loading="lazy">
        <img src="images/bg1.jpg" alt="" loading="lazy">
        <img src="images/bg2.jpg" alt="" loading="lazy">

    </div>
    
</body>
</html>'''

loops = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Loop</title>
  </head>
  <body>
    <div class="container">
      <div class="msg"></div>
    </div>
    <script>
      message = document.querySelector(".msg");
      message.innerHTML = "submitted";

      msg = "";
      for (i = 0; i < 16; i++) {
        if (i % 2 == 0) {
          msg += `${i} is even <br>`;
        } else {
          msg += `${i} is odd <br>`;
        }
      }
      message.innerHTML = msg;
    </script>
  </body>
</html>
'''

navbar = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Navbar with Hover Effects</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        font-size: 40px;
      }
      nav {
        background-color: #333;
        display: flex;
        justify-content: center;
      }
      ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        display: flex;
      }
      li {
        margin: 0 10px;
      }
      a {
        color: #fff;
        text-decoration: none;
        padding: 10px 15px;
        transition: background-color 0.3s;
        position: relative; /* Ensure position relative for dropdown */
      }
      a:hover {
        background-color: #555;
      }
      /* Dropdown Button */
      .dropbtn {
        background-color: #333333;
        color: white;
        /* padding: 16px; */
        font-size: 40px;
        border: none;
      }

      /* The container <div> - needed to position the dropdown content */
      .dropdown {
        position: relative;
        display: inline-block;
      }

      /* Dropdown Content (Hidden by Default) */
      .dropdown-content {
        display: none;
        position: absolute;
        background-color: #f1f1f1;
        min-width: 160px;
        box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
        z-index: 1;
      }

      /* Links inside the dropdown */
      .dropdown-content a {
        color: black;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
      }

      /* Change color of dropdown links on hover */
      .dropdown-content a:hover {
        background-color: #ddd;
      }

      /* Show the dropdown menu on hover */
      .dropdown:hover .dropdown-content {
        display: block;
      }

      /* Change the background color of the dropdown button when the dropdown content is shown */
      .dropdown:hover .dropbtn {
        background-color: #333333;
      }
    </style>
  </head>
  <body>
    <nav>
      <ul>
        <li><a href="#">Home</a></li>
        <li><a href="#">About</a></li>
        <li></li>
        <li><a href="#">Contact</a></li>
        <div class="dropdown">
          <button class="dropbtn">Dropdown</button>
          <div class="dropdown-content">
            <a href="#">Link 1</a>
            <a href="#">Link 2</a>
            <a href="#">Link 3</a>
          </div>
        </div>
      </ul>
    </nav>
  </body>
</html>
'''

num_product_sign = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sign</title>
  </head>
  <body>
    <div class="container">
      <input id="num1" type="number" />
      <input id="num2" type="number" />
      <input id="num3" type="number" />
      <button value="submit" class="btn">Submit</button>
      <div class="msg"></div>
    </div>

    <script>
      const btn = document.querySelector(".btn");

      btn.addEventListener("click", onsubmit);

      function onsubmit(e) {
        e.preventDefault();
        const num1 = document.querySelector("#num1").value;
        const num2 = document.querySelector("#num2").value;
        const num3 = document.querySelector("#num3").value;
        const ans = num1 * num2 * num3;
        console.log(ans);
        if (ans < 0) {
          alert("-");
        } else {
          alert("+");
        }
      }
    </script>
  </body>
</html>
'''

recommendation = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>

  </head>
  <body>
    <div class="container">
      <div class="wrapper">
        <input
          type="text"
          name="search"
          id="search"
          placeholder="Type to search"
          autocomplete="chrome-off"
        />
        <button id="addButton"><i class="fa fa-plus"></i></button>
        <div class="results">
          <ul></ul>
        </div>
      </div>
    </div>

    <script>
      let searchable = [
        "Elastic",
        "PHP",
        "Something about CSS",
        "How to code",
        "JavaScript",
        "Coding",
        "Some other item",
        "hey",

      ];

      const searchInput = document.getElementById("search");
      const addButton = document.getElementById("addButton");
      const searchWrapper = document.querySelector(".wrapper");
      const resultsWrapper = document.querySelector(".results");

      searchInput.addEventListener("keyup", () => {
        let results = [];
        let input = searchInput.value;
        if (input.length) {
          results = searchable.filter((item) => {
            return item.toLowerCase().includes(input.toLowerCase());
          });
        }
        renderResults(results);
      });

      addButton.addEventListener("click", () => {
        const newItem = prompt("Enter a new item to add:");
        if (newItem) {
          searchable.push(newItem);
        }
      });

      function renderResults(results) {
        if (!results.length) {
          return searchWrapper.classList.remove("show");
        }

        const content = results
          .map((item) => {
            return `<li>${item}</li>`;
          })
          .join("");

        searchWrapper.classList.add("show");
        resultsWrapper.innerHTML = `<ul>${content}</ul>`;
      }
      
    </script>
  </body>
</html>
'''

scroll_alert = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Scroll Alert</title>

    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        font-size: 8em;
      }

      .container {
        width: 100%;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
      }

      h1 {
        margin-bottom: 20px;
      }

      #content {
        width: 80%;
        max-height: 300px;
        overflow-y: scroll;
        border: 1px solid #ccc;
        padding: 10px;
      }

      #content p {
        margin: 0 0 10px 0;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Scroll Down</h1>
      <div id="content">
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam
          consectetur reprehenderit velit repudiandae veritatis eum, veniam
          reiciendis dolore nemo, error quaerat vero, quae eius. Non voluptas
          neque earum illo vel!. Lorem ipsum dolor, sit amet consectetur
          adipisicing elit. Eveniet, quod officiis. Repudiandae perferendis
          fugit alias quos a quia aut, tenetur corrupti quisquam, officiis odio
          porro, tempore iste est adipisci unde?. Lorem ipsum dolor sit amet
          consectetur adipisicing elit. Soluta ipsa rerum, impedit ab eos quas
          ipsum neque totam ut labore quis tempora nulla repellendus. Sunt non
          molestias dicta dolorum fuga.
        </p>
      </div>
    </div>

    <script>
      document
        .getElementById("content")
        .addEventListener("scroll", function () {
          var content = document.getElementById("content");
          if (content.scrollHeight - content.scrollTop === content.clientHeight) {
            alert("Reached end of content!");
          }
        });
    </script>
  </body>
</html>
'''

shopping_cart = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shopping Cart</title>
    <style>
        .cart {
            border: 1px solid #ccc;
            padding: 10px;
            width: 300px;
        }
        .cart-item {
            margin-bottom: 10px;
        }
        .cart-item button {
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <h1>Shopping Cart</h1>
    <div class="cart">
        <h2>Cart Items:</h2>
        <ul id="cart-items"></ul>
    </div>

    <h2>Available Items:</h2>
    <ul id="available-items">
        <li>
            <span>Item 1</span>
            <button onclick="addItem('Item 1')">Add to Cart</button>
        </li>
        <li>
            <span>Item 2</span>
            <button onclick="addItem('Item 2')">Add to Cart</button>
        </li>
        <li>
            <span>Item 3</span>
            <button onclick="addItem('Item 3')">Add to Cart</button>
        </li>
    </ul>

    <script>
        let cartItems = [];

        function addItem(itemName) {
            const cartItem = document.createElement('li');
            cartItem.className = 'cart-item';
            cartItem.textContent = itemName;
            const removeButton = document.createElement('button');
            removeButton.textContent = 'Remove';
            removeButton.onclick = () => removeItem(itemName, cartItem);
            cartItem.appendChild(removeButton);
            document.getElementById('cart-items').appendChild(cartItem);
            cartItems.push(itemName);
        }

        function removeItem(itemName, cartItem) {
            const cartItemsList = document.getElementById('cart-items');
            cartItemsList.removeChild(cartItem);
            const index = cartItems.indexOf(itemName);
            if (index > -1) {
                cartItems.splice(index, 1);
            }
        }
    </script>
</body>
</html>'''

temp_convertor = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <h1>Temp In Celcius</h1>
    <label>Input : </label>
    <input type="number" id="number" />
    <button id="btn" onclick="tempCon()">Convert</button>
    <p id="result"></p>

    <script>
      function tempCon() {
        var number = document.getElementById("number").value;
        var result = document.getElementById("result");
        console.log(number);
        var celcius = (9 * number) / 5 + 32;
        result.innerHTML = `${celcius} F`;
      }
    </script>
  </body>
</html>
'''

todo = '''import React, { useState } from 'react';
import './App.css';

function App() {
  const [todo, setTodo] = useState('');
  const [todoList, setTodoList] = useState([]);

  const handleInputChange = (event) => {
    setTodo(event.target.value);
  };

  const handleAddTodo = () => {
    if (todo.trim() !== '') {
      setTodoList([...todoList, { id: Date.now(), text: todo }]);
      setTodo('');
    }
  };

  const handleDeleteTodo = (id) => {
    const updatedTodoList = todoList.filter((todo) => todo.id !== id);
    setTodoList(updatedTodoList);
  };

  return (
    <>
      <h1>Todo List</h1>
      <label htmlFor="todoInput">Enter todo:</label>
      <input
        type="text"
        id="todoInput"
        value={todo}
        onChange={handleInputChange}
      />
      <button onClick={handleAddTodo}>Add Todo</button>
      <ul>
        {todoList.map((item) => (
          <li key={item.id}>
            {item.text}
            <button onClick={() => handleDeleteTodo(item.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </>
  );
}

export default App;'''

toolTip = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tooltip Example</title>
  <link rel="stylesheet" href="styles.css"> <!-- Include your CSS file -->
</head>
<body>
  <div class="tooltip">
    Hover over me
    <span class="tooltiptext">This is a tooltip</span>
  </div>
</body>
</html>
'''

webdev_exp = {
    "AppcustomHook.js" : AppcustomHook,
    "bgchange_onhover.html" : bgchange_onhover,
    "bgcolor_change.html" : bgcolor_change,
    "calculator.html" : calculator,
    "Card.js" : Card,
    "card.html" : card,
    "confirmation.html" : confirmation,
    "Counter.js" : Counter,
    "customHooks.js" : customHooks,
    "dropdown.html" : dropdown,
    "form_validation.html" : form_validation,
    "guess.html" : guess,
    "image_carousel.html" : image_carousel,
    "image_gallery.html" : image_gallery,
    "index.ts" : index,
    "largest.html" : largest,
    "lazy_loader.html" : lazy_loader,
    "loops.html" : loops,
    "navbar.html" : navbar,
    "num_product_sign.html" : num_product_sign,
    "recommendation.html" : recommendation,
    "scroll_alert.html" : scroll_alert,
    "shopping_cart.html" : shopping_cart,
    "temp_convertor.html" : temp_convertor,
    "todo.js" : todo,
    "toolTip.html" : toolTip
}

def webdev_():
    for filename, content in webdev_exp.items():
        print(filename)
    exp = input("Enter Code : ")
    with open(exp, 'w') as file:
        file.write(webdev_exp[exp])