
item2=JSON.parse(localStorage.getItem('cart'))
item3=localStorage.getItem('cart')
document.cookie = `cart=${item3}`;
function update(a,b){
var productid=parseInt(a);
var action=b;
if(user !== 'AnonymousUser'){
url="/updateitem?productid=" + productid + '&action=' + action;
var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
          window.location.reload();
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();}

if(user == 'AnonymousUser')
{
console.log('Not authenticated user')
anonymous(productid,action);
}
else{
  console.log('authenticated User')
}
}
//your cart functionality starts here:
function anonymous(productid,action){
a=productid
b=action
item=JSON.parse(localStorage.getItem('cart'))
if(item == undefined){
dict={};
dict[a]=1;
// alert(dict[a]);
localStorage.setItem('cart',JSON.stringify(dict))
}
else{
  dict2=JSON.parse(localStorage.getItem('cart'))
   if(dict2[a]==null ){
     dict2[a]=1;
   }
  else if(dict2[a]!==null  && action=='add')
  {
  dict2[a]=dict2[a]+1;
  window.location.reload();
 }
 else if(dict2[a]!== null && action=='remove')
{
  dict2[a]=dict2[a]-1;
 }
 if(dict2[a]<= 0){
 delete dict2[a]
 }
  localStorage.setItem('cart',JSON.stringify(dict2))
}
item2=JSON.parse(localStorage.getItem('cart'))
inner1=Object.values(item2)
inner2=inner1.reduce((a, b) => a + b, 0)
document.getElementById('cart-total').innerHTML=inner2;
item3=localStorage.getItem('cart')
document.cookie = `cart=${item3}`;

window.location.reload();




}
