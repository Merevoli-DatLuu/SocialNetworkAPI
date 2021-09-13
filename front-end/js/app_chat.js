$(document).ready(init);

const DEFAULT_AVATAR = "img/profile-photos/1.png"

function init(){
    $('#demo-nifty-settings').remove()
    access_token = localStorage.getItem("access_token");
    if (!access_token){
        window.location.replace("./login.html");
    }

    axios.get(`http://127.0.0.1:8000/api/v1/user/check_auth`, {
        headers: {
            'Authorization': `Bearer ${access_token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {})
    .catch(e => window.location.replace("./login.html"))

    scroll_obj = document.querySelectorAll('.nano,.has-scrollbar')[2]
    scroll_obj.className = "chat-scroll"
    scroll_obj.setAttribute("id", "scroll-chat");
    scroll_obj.style.height=""
    cano_content_full = document.getElementById("nano-content-full")
    cano_content_full.style['margin-right']=0
    cano_content_full.style['right']=0
    document.getElementsByClassName("nano-slider")[2].style['height']='0'
}

