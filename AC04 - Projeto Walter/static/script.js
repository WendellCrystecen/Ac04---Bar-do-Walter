
function verifSelect(val){
   if(val == "cartao")
       cartaoTrigger();
}

function cartaoTrigger(){
    displayEventBlock("part0");
    setTimeout(  ()=>{
        displayEventBlock("part1");
        document.getElementById("msg").innerText = "Aguardando pagamento.";
        setTimeout( ()=> {
            displayEventNone("part1");

        }, 1500);
    }, 0);
    setTimeout(  ()=>{
        displayEventBlock("part2");
        document.getElementById("msg").innerText = "Aguardando pagamento..";
        setTimeout( ()=>{
            displayEventNone("part2");

        }, 1500);
    }, 1500);
    setTimeout( ()=>{
        displayEventBlock("part3");
        document.getElementById("msg").innerText = "Aguardando pagamento...";
        setTimeout( ()=>{
            displayEventNone("part3");

        }, 1500);
    }, 3000);
    setTimeout(  ()=>{
        displayEventBlock("part4");
        document.getElementById("msg").innerText = "Pagamento Concluido !";
        setTimeout( ()=>{
            displayEventNone("part4");

        }, 1999);
    }, 4500);
    setTimeout( ()=> displayEventNone("part0"),5500);
}

function displayEventBlock(id)
{
   document.getElementById(id).style.display = "block";
   document.getElementById(id).style.fontSize = "15px";
   document.getElementById(id).style.alignContent = "Bottom";
}
function displayEventNone(id)
{
   document.getElementById(id).style.display = "none";
}
