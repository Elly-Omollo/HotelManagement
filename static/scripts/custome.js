const wrapper = document.querySelector('.wrapper');
const loginlink = document.querySelector('.login-link');
const registerlink = document.querySelector('.register-link');
const loginbt = document.querySelector('.btnlogin-popup');
const iconClose = document.querySelector('#close');



registerlink.addEventListener('click',(event) => {
    event.preventDefault();
    wrapper.classList.add('active');
});

// registerlink.addEventListener('click', (event) => {
//     event.preventDefault();
//     wrapper.classList.add('active');
//  });

loginlink.addEventListener('click', (event)=>{
    event.preventDefault();
    wrapper.classList.remove('active');
});


loginbt.addEventListener('click', ()=>{
    wrapper.classList.add('active-poppup');
});


// iconClose.addEventListener('click', ()=>{
//     wrapper.classList.remove('active-poppup');
// });


function updateRoom(){
    $.ajax({
        url: "/update_room_status/",
        type:"GET",
        success: function(data){
            console.log("Booking Confirmed");
        },
       
    });
}
setInterval(makeAjaxCall, 86400000);


