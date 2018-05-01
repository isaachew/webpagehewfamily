var tab = 0;
function flip(num) {
    $(".tab").css("display","none")
    $("#tab" + num).css("display", "table")
    document.cookie = 'tab=' + num;
    tab=num;
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function update() {
    var date = new Date();
    var _myOffset = 8 * 60 * 60000;
    var _userOffset = date.getTimezoneOffset() * 60000;
    var t = new Date(date.getTime() + _myOffset - _userOffset);
    $("age").each(function(k) {
        var a = $(this),
            are = /(0?[1-9]|[12][0-9]|3[01])(\/|\\)(0?[1-9]|1[012])\2((?:[1-9](?:[0-9]+)*)|0)(?:\s*)(BC|AD)?/i,
            n = are.exec(a.attr("date"));
        if (a.attr("date")) {
            var o = new Date(n[4], n[3], n[1]);
            a.text(Math.floor((t.valueOf() - o.valueOf()) /31536000000));
        }
    })
    $("lnk").each(function(k) { $(this).click(function() { flip($(this).attr("tab")) }) });
    addSW()
}
function postMessage(n){
    try{
        navigator.serviceWorker.controller.postMessage(n)
    }catch(e){console.log("Error: "+e)}
}
function getmodal(ins,clickResponse=function(){}) {
    div=$("<div id='modal'></div>")
    inner=$('<div id="innermodal"><div style="right:0;top:0;color:gray">🞫</div></div>')
    inner.children().click(function(){$(this.parentElement.parentElement).remove();clickResponse()})
    inner.append($("<spacer>&nbsp;</spacer>"+ins))
    div.append(inner)
	$("#content-wrapper").append(div)
}
function addSW() {
    console.log(window.Notification)
    function f(){
        n=getCookie("notification")
        if(!n){
            document.cookie="notification=true"
            getmodal("Click the gray 🞫 to allow notifications. <button onclick=\"$(this.parentElement.parentElement).remove()\">Deny</button>",function(){window.Notification.requestPermission().then(function(v){
                if(v==="denied"||v==="default"){
                    console.log("No notifications. Posting message")
                    postMessage({"notifications":false})
                }
                else
                {
                    postMessage({"notifications":true})
                }
            })})
        }
    }
    if ("serviceWorker" in navigator) {
        d=navigator.serviceWorker.register('/servw.js',{scope:"/"}).then(function(r) {
            console.log("%cService worker successful: "+r,"color:green")
            if(navigator.onLine){r.update()}
            r.addEventListener('updatefound', function() {
                var serv=r.installing
                console.log("%cNew service worker: "+serv,"color:blue")
            })
            if('SyncManager' in window){
                navigator.serviceWorker.ready.then(function(swRegistration) {
                    return swRegistration.sync.register('website_sync');
                })
            }
            f()
        }).catch(function(r) {
            console.log("%cService worker failed: "+r,"color:red")})
    }
}