var htmltext =
  '<div class="container" style="font-family:Helvetica; font-weight: 500;">' +
  '<div class="row">' +
  '<div id="Smallchat">' +
  '<div class="Layout Layout-open Layout-expand Layout-right" style="background-color: darkorange;color: rgb(255, 255, 255);opacity: 5;border-radius: 10px;">' +
  '<div class="Messenger_messenger">' +
  '<div class="Messenger_header" style=" color: rgb(255, 255, 255); background-color: darkorange;">' +
  '<div id="dd" class="wrapper-dropdown-3" tabindex="1">' +
  '<span>Language</span>' +
  '<ul class="dropdown">' +
  '<li>' +
  '<a href="#" name="lang" id="en" value="en">English</a>' +
  '</li>' +
  '<li>' +
  '<a href="#" name="lang" id="hi" value="hi">हिन्दी</a>' +
  '</li>' +
  '<li>' +
  '<a href="#" name="lang" id="pa" value="pa">ਪੰਜਾਬੀ</a>' +
  '</li>' +
  '<li>' +
  '<a href="#" name="lang" id="mr" value="mr">मराठी</a>' +
  '</li>' +
  '</ul>' +
  '</div>' +
  '<span class="chat_close_icon" style=" color:white;margin-right: 5px;float:right;margin-top: 5px;">' +
  '<i class="material-icons" aria-hidden="true">close</i>' +
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
  "</div>" +
  "</div>" +
  "</div>" +
  "</div>" +
  '<div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-animation="true" data-delay="8000">' +
  '<div class="toast-header">' +
  '<strong style="font-size: 20px;">Hey there 👋</strong>' +
  '</div>' +
  '</div>' +
  '<img class="iconic chat_on" src="https://unpkg.com/aarogyabot@4.1.1/dist/img/prahari.png">' +
  "</div>" +
  "</div>" +
  "</div>";
document.body.innerHTML += htmltext;

setTimeout(function () {
  $('.toast').fadeOut('fast');
}, 10000);

var pop = "https://unpkg.com/aarogyabot@4.1.1/dist/sounds/pop2.mp3";
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
var language = "en";
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

$(document).ready(function () {
  $("#en").click(function () {
    language = "en";
    $("#chats").empty();
    executedgreetings = false;
    greetings();
  });
  $("#hi").click(function () {
    language = "hi";
    $("#chats").empty();
    executedgreetings = false;
    greetings();
  });
  $("#pa").click(function () {
    language = "pa";
    $("#chats").empty();
    executedgreetings = false;
    greetings();
  });
  $("#mr").click(function () {
    language = "mr";
    $("#chats").empty();
    executedgreetings = false;
    greetings();
  });
});

var fetchdata = function (endpoint, data) {
  console.log(endpoint);
  addtyping();
  fetch("http://praharibot.herokuapp.com/" + endpoint, {
    // fetch("http://127.0.0.1:5000/" + endpoint, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Methods": "*",
      },
      method: "POST",
      body: JSON.stringify({
        text: data,
        lang: language,
      }),
    })
    .then(function (response) {
      return response.json();
    })
    .then(function (myJson) {
      removetyping();
      setBotResponse(myJson["data"]);
      if (endpoint == "track") {
        if (language == "en") {
          setBotResponse("For more info type the state -");
        } else if (language == "hi") {
          setBotResponse("अधिक जानकारी के लिए राज्य टाइप करें -");
        } else if (language == "pa") {
          setBotResponse("ਵਧੇਰੇ ਜਾਣਕਾਰੀ ਲਈ ਰਾਜ ਟਾਈਪ ਕਰੋ -");
        } else if (language == "mr") {
          setBotResponse("अधिक माहितीसाठी राज्य टाइप करा -");
        }
      } else {

        if (endpoint != "chat") {
          continuebuttons();
          if (myJson["res"]) {
            endpoint = "chat";
          }
        }
      }
    });
};

$(document.body).on("click", "button", function () {
  if (this.id == "yes") {
    endpoint = "chat";
    initbuttons(language);
  }
  if (this.id == "no") {
    endpoint = "chat";
    if (language == "en") {
      setBotResponse("Thank you for you time! Gudbye!");
    } else if (language == "hi") {
      setBotResponse("आपके समय के लिए धन्यवाद! अलविदा!");
    } else if (language == "pa") {
      setBotResponse("ਤੁਹਾਡੇ ਸਮੇਂ ਲਈ ਧੰਨਵਾਦ! ਗੁਡਬੇ!");
    } else if (language == "mr") {
      setBotResponse("आपण वेळ दिल्याबद्दल धन्यवाद! गुडबाय!");
    }
  }
  if (this.id == "track") {
    endpoint = "track";
    fetchdata(endpoint, this.id);
    endpoint = "trackstate";
  }
  if (this.id == "hosp") {
    endpoint = "hosp";
    setTimeout(function () {
      if (language == "en") {
        setBotResponse("Please type the state -");
      } else if (language == "hi") {
        setBotResponse("कृपया राज्य लिखें -");
      } else if (language == "pa") {
        setBotResponse("ਕਿਰਪਾ ਕਰਕੇ ਰਾਜ ਟਾਈਪ ਕਰੋ -");
      } else if (language == "mr") {
        setBotResponse("कृपया राज्य टाइप करा -");
      }
    }, 600);
  }
  if (this.id == "lines") {
    endpoint = "lines";
    setTimeout(function () {
      if (language == "en") {
        setBotResponse("Please type the state -");
      } else if (language == "hi") {
        setBotResponse("कृपया राज्य लिखें -");
      } else if (language == "pa") {
        setBotResponse("ਕਿਰਪਾ ਕਰਕੇ ਰਾਜ ਟਾਈਪ ਕਰੋ -");
      } else if (language == "mr") {
        setBotResponse("कृपया राज्य टाइप करा -");
      }
    }, 600);
  }
  if (this.id == "prec") {
    endpoint = "prec";
    fetchdata(endpoint, this.id);
  }
  scrollToBottomOfResults();
});

$(document).ready(function () {
  $("#mymessage").on("keyup keypress", function (e) {
    var keyCode = e.keyCode || e.which;
    var text = $("#mymessage").val();
    if (keyCode === 13) {
      if (text == "" || $.trim(text) == "") {
        e.preventDefault();
        return false;
      } else {
        e.preventDefault();
        setUserResponse(text);
        $("#mymessage").blur();
        fetchdata(endpoint, text);
        return false;
      }
    }
  });
  $("#sendbutton").on("click", function (e) {
    var text = $("#mymessage").val();
    if (text == "" || $.trim(text) == "") {
      e.preventDefault();
      return false;
    } else {
      e.preventDefault();
      setUserResponse(text);
      $("#mymessage").blur();
      fetchdata(endpoint, text);
      return false;
    }
  });
});

$(document).ready(function () {
  $(".chat_on").click(function () {
    $(".Layout").toggle();
    $(".chat_on").hide(300);
    greetings();
  });
  $(".chat_close_icon").click(function () {
    $(".Layout").hide();
    $(".chat_on").show(300);
  });
});

var greetings = (function () {
  return function () {
    if (!executedgreetings) {
      executedgreetings = true;
      setTimeout(function () {
        if (language == "en") {
          setBotResponse("Hey, I am Prahari Bot.<br>How can I help U?");
        } else if (language == "hi") {
          setBotResponse(
            "हैलो, मैं प्रहरी बॉट हूं। मैं आपकी कैसे मदद कर सकता हूं?"
          );
        } else if (language == "pa") {
          setBotResponse(
            "ਹੇ, ਮੈਂ ਪ੍ਰਹਾਰੀ ਬੋਟ ਹਾਂ. ਮੈਂ ਤੁਹਾਡੀ ਕਿਵੇਂ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ?"
          );
        } else if (language == "mr") {
          setBotResponse("अहो, मी प्रहारी बोट आहे. मी यूला कशी मदत करू?");
        }
        initbuttons(language);
      }, 600);
      scrollToBottomOfResults();
    }
  };
})();

function continuebuttons() {
  if (language == "en") {
    var msg =
      '<p class="botMsg">' +
      "Do you want to Continue?" +
      '<div class="bts">' +
      '<button type="button" class="prahaributton" id="yes" style="margin-top:2px;">Yes</button>' +
      '<button type="button" class="prahaributton" id="no" style="margin-top:2px;">No</button>' +
      "</div>" +
      '<div class="clearfix"></div>';
  } else if (language == "hi") {
    var msg =
      '<p class="botMsg">' +
      "क्या आप जारी रखना चाहते हैं?" +
      '<div class="bts">' +
      '<button type="button" class="prahaributton" id="yes" style="margin-top:2px;">हाँ</button>' +
      '<button type="button" class="prahaributton" id="no" style="margin-top:2px;">नहीं</button>' +
      "</div>" +
      '<div class="clearfix"></div>';
  } else if (language == "pa") {
    var msg =
      '<p class="botMsg">' +
      "ਕੀ ਤੁਸੀਂ ਜਾਰੀ ਰੱਖਣਾ ਚਾਹੁੰਦੇ ਹੋ?" +
      '<div class="bts">' +
      '<button type="button" class="prahaributton" id="yes" style="margin-top:2px;">ਹਾਂ</button>' +
      '<button type="button" class="prahaributton" id="no" style="margin-top:2px;">ਨਹੀਂ</button>' +
      "</div>" +
      '<div class="clearfix"></div>';
  } else if (language == "mr") {
    var msg =
      '<p class="botMsg">' +
      "आपण सुरू ठेवू इच्छिता?" +
      '<div class="bts">' +
      '<button type="button" class="prahaributton" id="yes" style="margin-top:2px;">होय</button>' +
      '<button type="button" class="prahaributton" id="no" style="margin-top:2px;">नाही</button>' +
      "</div>" +
      '<div class="clearfix"></div>';
  }
  setTimeout(function () {
    setBotResponseWithoutAvatar(msg);
  }, 600);
  endpoint = "chat";
  scrollToBottomOfResults();
}

function initbuttons(language) {
  if (language == "en") {
    var buttons =
      '<div class="bts">' +
      '<button type="button" class="prahaributton" id="track" style="margin-top:2px;">Track Cases</button>' +
      '<button type="button" class="prahaributton" id="hosp" style="margin-top:2px;">Nearby Hospitals</button>' +
      '<button type="button" class="prahaributton" id="lines" style="margin-top:2px;">State Helplines</button>' +
      '<button type="button" class="prahaributton" id="prec" style="margin-top:2px;">Precautions</button>' +
      "</div>";
  } else if (language == "hi") {
    var buttons =
      '<div class="bts">' +
      '<button type="button" class="prahaributton" id="track" style="margin-top:2px;">मामलों का ट्रैक नं</button>' +
      '<button type="button" class="prahaributton" id="hosp" style="margin-top:2px;">आसपास के अस्पताल</button>' +
      '<button type="button" class="prahaributton" id="lines" style="margin-top:2px;">राज्य के हेल्पलाइन</button>' +
      '<button type="button" class="prahaributton" id="prec" style="margin-top:2px;">एहतियात</button>' +
      "</div>";
  } else if (language == "pa") {
    var buttons =
      '<div class="bts">' +
      '<button type="button" class="prahaributton" id="track" style="margin-top:2px;">ਟਰੈਕ ਕੇਸ</button>' +
      '<button type="button" class="prahaributton" id="hosp" style="margin-top:2px;">ਨੇੜਲੇ ਹਸਪਤਾਲ</button>' +
      '<button type="button" class="prahaributton" id="lines" style="margin-top:2px;">ਸਟੇਟ ਹੈਲਪਲਾਈਨਜ</button>' +
      '<button type="button" class="prahaributton" id="prec" style="margin-top:2px;">ਸਾਵਧਾਨੀਆਂ</button>' +
      "</div>";
  } else if (language == "mr") {
    var buttons =
      '<div class="bts">' +
      '<button type="button" class="prahaributton" id="track" style="margin-top:2px;">प्रकरणे मागोवा घ्या</button>' +
      '<button type="button" class="prahaributton" id="hosp" style="margin-top:2px;">जवळपास रुग्णालये</button>' +
      '<button type="button" class="prahaributton" id="lines" style="margin-top:2px;">राज्य हेल्पलाइन</button>' +
      '<button type="button" class="prahaributton" id="prec" style="margin-top:2px;">सावधगिरी</button>' +
      "</div>";
  }
  setTimeout(function () {
    setBotResponseWithoutAvatar(buttons);
  }, 600);
  scrollToBottomOfResults();
}

function setBotResponseWithoutAvatar(val) {
  var UserResponse = val + ' </p><div id="clearfixwithoutavatar"></div>';
  $(UserResponse).appendTo(".chats").hide().fadeIn(1000);
  $("#mymessage").val("");
  scrollToBottomOfResults();
}

function setUserResponse(val) {
  var UserResponse =
    '<img class="userAvatar" src="https://unpkg.com/aarogyabot@4.1.1/dist/img/impatient.svg"><p class="userMsg">' +
    val +
    ' </p><div class="clearfix"></div>';
  $(UserResponse).appendTo(".chats").hide().fadeIn(1000);
  $("#mymessage").val("");
  scrollToBottomOfResults();
}

function setBotResponse(val) {
  var BotResponse =
    '<img class="botAvatar" src="https://unpkg.com/aarogyabot@4.1.1/dist/img/prahari.png" style="margin-top:5px;"><p class="botMsg">' +
    val +
    '</p><div class="clearfix"></div>';
  $(BotResponse).appendTo(".chats").hide().fadeIn(1000);
  sound.play();
  scrollToBottomOfResults();
}

// dropdown

function DropDown(el) {
  this.dd = el;
  this.placeholder = this.dd.children("span");
  this.opts = this.dd.find("ul.dropdown > li");
  this.val = "";
  this.index = -1;
  this.initEvents();
}
DropDown.prototype = {
  initEvents: function () {
    var obj = this;

    obj.dd.on("click", function (event) {
      $(this).toggleClass("active");
      return false;
    });

    obj.opts.on("click", function () {
      var opt = $(this);
      obj.val = opt.text();
      obj.index = opt.index();
      obj.placeholder.text(obj.val);
    });
  },
  getValue: function () {
    return this.val;
  },
  getIndex: function () {
    return this.index;
  },
};

$(function () {
  var dd = new DropDown($("#dd"));
  $(document).click(function () {
    $(".wrapper-dropdown-3").removeClass("active");
  });
});