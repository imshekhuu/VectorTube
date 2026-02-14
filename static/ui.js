function toggleSidebar(){
    document.getElementById("sidebar").classList.toggle("collapsed");
}

function sendMessage(){

    const input=document.getElementById("messageInput");
    if(!input.value) return;

    addMessage(input.value,"user");

    const typing=addMessage("Thinking","bot typing");

    setTimeout(()=>{
        typing.classList.remove("typing");
        typing.innerText="Your Flask/Django RAG streaming answer goes here.";
    },900);

    input.value="";
}

function addMessage(text,role){
    const div=document.createElement("div");
    div.className=`msg ${role}`;
    div.innerText=text;

    const box=document.getElementById("chatBox");
    box.appendChild(div);
    box.scrollTop=box.scrollHeight;

    return div;
}
