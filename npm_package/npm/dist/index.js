var htmltext =
  '<div class="container" style="font-family:Helvetica; font-weight: 500;">' +
  '<div class="row">' +
  '<div id="Smallchat">' +
  '<div class="Layout Layout-open Layout-expand Layout-right" style="background-color: #3F51B5;color: rgb(255, 255, 255);opacity: 5;border-radius: 10px;">' +
  '<div class="Messenger_messenger">' +
  '<div class="Messenger_header" style=" color: rgb(255, 255, 255); background-color: #800000">' +
  '<div class="Messenger_prompt" styel="color:white";>How can we help you?</div>' +
  '<span class="chat_close_icon" style=" color:white;margin-right: 5px;float:right;margin-top: 5px;">' +
  '<i class="material-icons" style="margin-right:2px;" id="refresh">refresh</i>' +
  '<i class="material-icons" aria-hidden="true" id="closeit">close</i>' +
  "</span>" +
  "</div>" +
  '<div class="Messenger_content" id="chatcontainer">' +
  '<div class="Messages chats" id="chats">' +
  '<div class="clearfix"></div>' +
  "</div>" +
  '<div class="Input Input-blank">' +
  "<form>" +
  '<input type="text" id="mymessage" class="Input_field" placeholder="Ask me anything!" style="height: 20px;"></input>' +
  '<button id="sendbutton" class="Input_button Input_button-send" type="submit">' +
  '<div class="Icon" style="width: 18px; height: 18px;">' +
  '<svg width="57px" height="54px" viewBox="1496 193 57 54" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="width: 18px; height: 18px;">' +
  '<g id="Group-9-Copy-3" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" transform="translate(1523.000000, 220.000000) rotate(-270.000000) translate(-1523.000000, -220.000000) translate(1499.000000, 193.000000)">' +
  '<path d="M5.42994667,44.5306122 L16.5955554,44.5306122 L21.049938,20.423658 C21.6518463,17.1661523 26.3121212,17.1441362 26.9447801,20.3958097 L31.6405465,44.5306122 L42.5313185,44.5306122 L23.9806326,7.0871633 L5.42994667,44.5306122 Z M22.0420732,48.0757124 C21.779222,49.4982538 20.5386331,50.5306122 19.0920112,50.5306122 L1.59009899,50.5306122 C-1.20169244,50.5306122 -2.87079654,47.7697069 -1.64625638,45.2980459 L20.8461928,-0.101616237 C22.1967178,-2.8275701 25.7710778,-2.81438868 27.1150723,-0.101616237 L49.6075215,45.2980459 C50.8414042,47.7885641 49.1422456,50.5306122 46.3613062,50.5306122 L29.1679835,50.5306122 C27.7320366,50.5306122 26.4974445,49.5130766 26.2232033,48.1035608 L24.0760553,37.0678766 L22.0420732,48.0757124 Z" id="sendicon" fill="#96AAB4" fill-rule="nonzero"></path>' +
  "</g>" +
  "</svg>" +
  "</div>" +
  "</button>" +
  "</form>" +
  '<hr style="width:100%;color:grey;background-color: grey;border: 1px solid white;opacity: 0.5;">' +
  '<p class="love" style="line-height: 8px;">Created with <span style="color:red;">❤</span>&nbsp;&nbsp;by <a href="https://analyticware.in/" style="text-decoration:none;color:blue;">AnalyticWare</a></p>' +
  "</div>" +
  "</div>" +
  "</div>" +
  "</div>" +
  '<div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-animation="true" data-delay="8000">' +
  '<div class="toast-header">' +
  '<strong style="font-size: 20px;">Hey there 👋</strong>' +
  '</div>' +
  '</div>' +
  '<div class="chat_on">' +
  '<img class="iconic" src="https://unpkg.com/thaparbot@latest/dist/img/bot.png">' +
  '</div>' +
  "</div>" +
  "</div>" +
  "</div>";
document.body.innerHTML += htmltext;

setTimeout(function () {
  $('.toast').fadeOut('fast');
}, 5000);

var fb = "https://www.facebook.com/officialTIET/";
var pop = "https://unpkg.com/thaparbot@latest/dist/sounds/pop2.mp3";
var sound = new Howl({
  src: [pop],
  volume: 0.5,
});


function scrollToBottomOfResults() {
  var terminalResultsDiv = document.getElementById("chats");
  terminalResultsDiv.scrollTop = terminalResultsDiv.scrollHeight;
  var terminalContDiv = document.getElementById("chatcontainer");
  terminalContDiv.scrollTop = terminalContDiv.scrollHeight;
}

var endpoint = "chat";
var executedgreetings = false;

var addtyping = function () {
  var typing =
    '<div id="typingind" class="typingIndicatorContainer">' +
    ' <div class="typingIndicatorBubble">' +
    '<div class="typingIndicatorBubbleDot"></div>' +
    '<div class="typingIndicatorBubbleDot"></div>' +
    '<div class="typingIndicatorBubbleDot"></div>' +
    "</div>" +
    "</div>";
  setBotResponseWithoutAvatar(typing);
};
var removetyping = function () {
  $("#typingind").remove();
  $("#clearfixwithoutavatar").remove();
};

// open/close/refresh
$(document).ready(function () {
  $("#refresh").click(function () {
    $("#chats").empty();
    executedgreetings = false;
    greetings();
  });
  $(".chat_on").click(function () {
    $(".Layout").toggle();
    $(".chat_on").hide(300);
    greetings();
  });
  $("#closeit").click(function () {
    $(".Layout").hide();
    $(".chat_on").show(300);
  });
  $("#enter").click(function () {
    $(".Layout").toggle();
    $(".chat_on").hide(300);
    greetings();
  });
});

var allpar = '<div class="bts"><button type="button" class="longbutton btn-block" id="admission" style="width:92%;">Admissions</button><button type="button" class="longbutton btn-block" id="placement" style="width:92%;">Placement Sessions</button><button type="button" class="regularbutton btn-block" id="scholarship" >Scholarships</button><button type="button" class="regularbutton btn-block" id="campus" >Campus Life</button><button type="button" class="regularbutton btn-block" id="hostel" >Hostels</button><button type="button" class="regularbutton btn-block" id="library" >Library</button><button type="button" class="regularbutton btn-block" id="reach" >How To Reach</button><button type="button" class="regularbutton btn-block" id="contact" >Contact Us</button><button type="button" class="regularbutton btn-block" id="chat" >Chat</button><button type="button" class="regularbutton btn-block" id="exit">Exit</button></div>';

var allstud = '<div class="bts"><button type="button" class="regularbutton btn-block" id="timetable">TimeTable</button><button type="button" class="regularbutton btn-block" id="webkiosk" >Webkiosk</button><button type="button" class="regularbutton btn-block" id="notification" >Notifications</button><button type="button" class="regularbutton btn-block" id="extra" >Extra</button><button type="button" class="regularbutton btn-block" id="chat" >Chat</button><button type="button" class="regularbutton btn-block" id="exit">Exit</button></div>';

var parcont = '<div class="bts"><button type="button" class="regularbutton" id="generalparent">General</button><button type="button" class="regularbutton" id="chat">Chat</button><a href="https://www.facebook.com/officialTIET/"><button type="button" class="longbutton" id="fb" style="width:92%;">Connect on Facebook</button></a></div>';

var studcont = '<div class="bts"><button type="button" class="regularbutton" id="generalstudent" >General</button><button type="button" class="regularbutton" id="chat" >Chat</button><a href="https://www.facebook.com/officialTIET/"><button type="button" class="longbutton" id="fb" style="width:92%;">Connect on Facebook</button></a></div>';

// fetch & set
var fetchdata = function (endpoint, id, entity) {
  addtyping();
  fetch("http://8c1461559d60.ngrok.io/" + endpoint, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Methods": "*",
      },
      method: "POST",
      body: JSON.stringify({
        text: id,
      }),
    })
    .then(function (response) {
      return response.json();
    })
    .then(function (myJson) {
      if (entity == 'student') {
        setBotResponse(myJson["data"], 'student');
      } else if (entity == 'parent') {
        setBotResponse(myJson["data"], 'parent');
      } else if (entity == 'else') {
        setBotResponseWithButtons(parcont);
      } else {
        setBotResponse(myJson["data"]);
      }
    });
};


// buttonsresponse
$(document.body).on("click", "button", function () {
  if (this.id == "generalstudent") {
    addtyping();
    setBotResponseWithButtons(allstud);
  }
  if (this.id == "chat") {
    addtyping();
    setBotResponse('Hello 👋, I am your assistant. I am here to help you in case of any queries!');
    setBotResponse('You can ask me about Placements  , Admissions , Fees , Scholarship , Labs , Marking Scheme , College Reopening etc. 😄');
  }
  if (this.id == "generalparent") {
    addtyping();
    setBotResponseWithButtons(allpar);
  }
  if (
    this.id == "placement" ||
    this.id == "admission" ||
    this.id == "contact" ||
    this.id == "campus" ||
    this.id == "scholarship" ||
    this.id == "hostel" ||
    this.id == "library" ||
    this.id == "reach" ||
    this.id == "programme"
  ) {
    fetchdata('chat', this.id, 'parent');
  }
  if (
    this.id == "timetable" ||
    this.id == "webkiosk" ||
    this.id == "extra" ||
    this.id == "notification"
  ) {
    scrollToBottomOfResults();
    fetchdata('chat', this.id, 'student');
  }
  if (this.id == "yespar") {
    addtyping();
    setBotResponseWithButtons(parcont);
  }
  if (this.id == "yesstu") {
    addtyping();
    setBotResponseWithButtons(studcont);
  }
  if (this.id == "no" || this.id == "exit") {
    addtyping();
    setBotResponse('Thank You for using our service!');
  }
  if (this.id == "parents") {
    addtyping();
    setTimeout(function () {
      setBotResponse('Welcome Mam/Sir. <br> Thapar Institute of Engineering and Technology Welcomes you <br> Can we get your Email Id please?');
    }, 2000);
  }
  if (this.id == "students") {
    addtyping();
    setTimeout(function () {
      // setBotResponse('For Students');
      setBotResponseWithButtons(allstud);
    }, 2000);
  }
});

$(document).ready(function () {
  $("#mymessage").on("keyup keypress", function (e) {
    var keyCode = e.keyCode || e.which;
    var text = $("#mymessage").val();
    text = text.replace("<", " ");
    text = text.replace(">", " ");
    text = text.replace("alert", " ");
    text = text.replace("script", " ");
    if (keyCode === 13) {
      if (text == "" || $.trim(text) == "") {
        e.preventDefault();
        return false;
      } else {
        e.preventDefault();
        var re = /(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))/;
        if (re.test(text)) {
          setUserResponse(text);
          $("#mymessage").blur();
          fetchdata('email', text, 'else');
          return false;
        } else {
          setUserResponse(text);
          $("#mymessage").blur();
          fetchdata('chat', text, 'bot');
          return false;
        }
      }
    }
  });
  $("#sendbutton").on("click", function (e) {
    var text = $("#mymessage").val();    
    text = text.replace("<", " ");
    text = text.replace(">", " ");
    text = text.replace("alert", " ");
    text = text.replace("script", " ");
    if (text == "" || $.trim(text) == "") {
      e.preventDefault();
      return false;
    } else {
      e.preventDefault();
      var re = /(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))/;
      if (re.test(text)) {
        setUserResponse(text);
        $("#mymessage").blur();
        fetchdata('email', text, 'else');
        return false;
      } else {
        setUserResponse(text);
        $("#mymessage").blur();
        fetchdata('chat', text, 'bot');
        return false;
      }
    }
  });
});

var greetings = (function () {
  return function () {
    if (!executedgreetings) {
      executedgreetings = true;
      setTimeout(function () {
        setBotResponse('Hello , Welcome to Thapar Institute of Engineering and Technology Chat Support.<br> We are here to help you for all your queries 😇');
      }, 500);
      setTimeout(function () {
        setBotResponseWithoutAvatar('<div class="bts"><button type="button" class="longbutton" id="parents">Parents Section</button><button type="button" class="longbutton" id="students">Students Section</button></div>');
      }, 500);
      scrollToBottomOfResults();
    }
  };
})();

function setUserResponse(val) {
  var UserResponse =
    '<img class="userAvatar" src=' +
    "https://unpkg.com/thaparbot@latest/dist/img/man.png" +
    '><p class="userMsg">' +
    val +
    ' </p><div class="clearfix"></div>';
  $(UserResponse).appendTo(".chats").show("slow");
  $("#mymessage").val("");
  scrollToBottomOfResults();
}

function setBotResponse(val, extra) {
  removetyping();
  var BotResponse =
    '<img class="botAvatar" src="https://unpkg.com/thaparbot@latest/dist/img/bot.png"><p class="botMsg">' +
    val +
    '</p><div class="clearfix"></div>';
  $(BotResponse).appendTo(".chats").hide().fadeIn(1000);
  if (extra == 'parent') {
    setBotResponse('Do you want to Continue?');
    setBotResponseWithoutAvatar('<div class="bts"><button type="button" class="regularbutton" id="yespar">Yes</button><button type="button" class="regularbutton" id="no">No</button></div>');
  } else if (extra == 'student') {
    setBotResponse('Do you want to Continue?');
    setBotResponseWithoutAvatar('<div class="bts"><button type="button" class="regularbutton" id="yesstu">Yes</button><button type="button" class="regularbutton" id="no">No</button></div>');
  }
  $("#mymessage").val("");
  sound.play();
  scrollToBottomOfResults();
}


function setBotResponseWithoutAvatar(val) {
  removetyping();
  var botResponse = val + '<div id="clearfixwithoutavatar"></div>';
  $(botResponse).appendTo(".chats").hide().fadeIn(1000);
  $("#mymessage").val("");
  sound.play();
  scrollToBottomOfResults();
}

function setBotResponseWithButtons(val) {
  removetyping();
  var botResponse = '<img class="botAvatar" src="https://unpkg.com/thaparbot@latest/dist/img/bot.png">' + val + '<div id="clearfixwithoutavatar"></div>';
  $(botResponse).appendTo(".chats").hide().fadeIn(1000);
  $("#mymessage").val("");
  sound.play();
  scrollToBottomOfResults();
}
