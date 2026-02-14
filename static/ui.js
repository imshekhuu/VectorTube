function toggleSidebar(){
 const sb=document.getElementById("sidebar");
 if(sb) sb.classList.toggle("collapsed");
}

const input=document.getElementById("messageInput");

if(input){

 input.addEventListener("keydown",e=>{
  if(e.key==="Enter" && !e.shiftKey){
   e.preventDefault();
   sendMessage();
  }
 });

 input.addEventListener("input",()=>{
  input.style.height="auto";
  input.style.height=input.scrollHeight+"px";
 });
}

function sendMessage(){

 if(!input.value) return;

 addMessage(input.value,"user");

 const typing=addMessage("","bot typing");
 typing.innerHTML="<span></span><span></span><span></span>";

 setTimeout(()=>{
  typing.classList.remove("typing");
  typing.innerText="Your Flask/Django RAG streaming answer goes here.";
 },900);

 input.value="";
}

function addMessage(text,role){

 const wrapper=document.createElement("div");
 wrapper.className=`msg ${role}`;

 const avatar=document.createElement("div");
 avatar.className="avatar";
 avatar.innerText=role==="user"?"U":"AI";

 const content=document.createElement("div");
 content.className="msg-content";
 content.innerText=text;

 const time=document.createElement("div");
 time.className="copy";
 time.innerText=new Date().toLocaleTimeString();
 time.onclick=()=>navigator.clipboard.writeText(text);

 content.appendChild(time);

 wrapper.appendChild(avatar);
 wrapper.appendChild(content);

 const box=document.getElementById("chatBox");
 box.appendChild(wrapper);
 box.scrollTop=box.scrollHeight;

 return content;
}
