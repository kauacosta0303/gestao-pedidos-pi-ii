const form=document.querySelector('#pedido-form');
if(form){
 const itens=[];const lista=document.querySelector('#itens');const mensagem=document.querySelector('#mensagem');
 document.querySelector('#adicionar').addEventListener('click',()=>{
  const seletor=document.querySelector('#produto');const quantidade=Number(document.querySelector('#quantidade').value);
  if(!seletor.value||!Number.isInteger(quantidade)||quantidade<1){mensagem.textContent='Selecione um produto e quantidade válida.';return;}
  itens.push({produto:Number(seletor.value),quantidade});
  const li=document.createElement('li');li.textContent=`${seletor.selectedOptions[0].text} — Quantidade: ${quantidade}`;lista.appendChild(li);mensagem.textContent='';
 });
 form.addEventListener('submit',async(e)=>{
  e.preventDefault();if(!itens.length){mensagem.textContent='Adicione pelo menos um produto.';return;}
  try{const res=await fetch(form.dataset.url,{method:'POST',headers:{'Content-Type':'application/json','X-CSRFToken':form.querySelector('[name=csrfmiddlewaretoken]').value},body:JSON.stringify({cliente:document.querySelector('#cliente').value,itens})});const data=await res.json();if(!res.ok)throw Error(data.erro||'Falha ao registrar pedido.');window.location.reload();}
  catch(err){mensagem.textContent=err.message;}
 });
}
