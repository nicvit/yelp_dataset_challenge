
//DOCUMENT STARTS
$(document).ready(function (){
    console.log("Document is Ready!");
    web_socket = new WebSocket("ws://localhost:8888/ws");
    web_socket.onopen = function() {
        appendLogMessage("socket opened");
        //message = createMessageWithType("Greeting", "Hello World!!");
        //sendMessageHandler(message)
    };
    web_socket.onmessage = function (evt) {
        console.log(evt.data);
        var message = JSON.parse(evt.data);
        var type = message.MSG_TYPE;
        if (type === MSG_TYPE_BROADCAST) {
            appendLogMessage(message.content);
        } else if (type === MSG_TYPE_VIS) {
            images = message.items;
            reloadImageScreen();
        }
    };

    var logScreen = $('<div id="console">');
    var textView = $('<p id="logScreen">');
    textView.text("Test Console Log...");
    logScreen.append(textView);
    containers.logScreen = logScreen;
    containers.imageScreen = $('<div class="imageContainer" id="imageScreen">');

    $('button[id!="clearLogButton"]').click(buttonDidClick);
    $('#clearLogButton').click(clearLogMessage);

    $("input[type=radio]").change(function() {
       displayMode = $(this).val();
       updateMainScreen();
    });

    $("input[type=radio]").each(function() {
        $(this).prop("checked", $(this).val() === displayMode);
    });

    updateMainScreen();
});


/*
    GLOBAL STRING VARIBLES
*/
var web_socket = undefined;
var MSG_TYPE = 'MSG_TYPE'
var MSG_TYPE_IMPORT = "import";
var MSG_TYPE_NLP = "nlp";
var MSG_TYPE_VIS = "visualise";
var MSG_TYPE_BROADCAST = "broadcast";
var Message = {
    MSG_TYPE: "",
    content: undefined
};

var DisplayType = {
    log: 'log',
    image: 'image'
};
var displayMode = DisplayType.log;

var containers = {
    logScreen: undefined,
    imageScreen: undefined
};

var images = [];

/**
*  This is Message Handler
*
*/
function sendMessageHandler(msgObj) {
    var jsonMessage = JSON.stringify(msgObj);
    web_socket.send(jsonMessage);
    appendLogMessage("Send message: " + jsonMessage + " to server.");
}

function createMessageWithType(type, content) {
    var newMsg = Object.create(Message);
    newMsg.MSG_TYPE = type;
    newMsg.content = content;
    return newMsg;
}

/**
    Private Methods
*/

function updateMainScreen() {
    var mainScreen = $("#mainScreen");
    mainScreen.empty();

    if (displayMode === DisplayType.log) {
        mainScreen.append(containers.logScreen);
        var height = parseInt($('#logScreen').height());
        height += '';
        $('#console').animate({scrollTop: height});
    } else if (displayMode === DisplayType.image) {
        mainScreen.append(containers.imageScreen);
    }
}

function reloadImageScreen() {
    var imageScreen = containers.imageScreen;
    imageScreen.empty();

    imageArr = [];
    for(var i = 0; i < images.length; i++) {
        var imageContent = images[i];
        var imageElement = $('<img class="outputImage" />');
        var imageSource = "data:image/";
        imageSource = imageSource + imageContent.file_extension + ';base64, ' + imageContent.content;
        imageElement.attr("src", imageSource);
        imageElement.attr("id", imageContent.file_name);

        imageArr.push(imageElement);
    }

    imageScreen.append(imageArr);
}

/**
    Event Listeners
*/
function buttonDidClick() {
    console.log("Button: " + $(this).attr("id"));
    var buttonId = $(this).attr("id");
    var message = undefined;
    if (buttonId === 'importButton') {
        message = createMessageWithType(MSG_TYPE_IMPORT, "");
    } else if (buttonId === 'NLPButton') {
        message = createMessageWithType(MSG_TYPE_NLP, "");
    } else if (buttonId === 'visualiseButton') {
        message = createMessageWithType(MSG_TYPE_VIS, "");
    }

    if (message != undefined) {
        sendMessageHandler(message);
    }
}

function appendLogMessage(log) {
    var logScreen = $('#logScreen');
    var oldStr = logScreen.html();
    var newStr = oldStr + '<br>' + log;
    logScreen.html(newStr);

    var height = parseInt($('#logScreen').height());
    height += '';
    $('#console').animate({scrollTop: height});
}

function clearLogMessage() {
    var logScreen = $('#logScreen');
    logScreen.html("");
}