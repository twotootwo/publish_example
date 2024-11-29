const button = document.getElementsByClassName('btn')

if(button){
  button.addEventListener("click",()=>{
      window.location.href = "/login/sign-up/"
  });
}